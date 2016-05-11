"""
Generate Python source code: random function calls with random arguments.
Use "python" command line program.

Interresting modules: all modules written in C or having some code written
in C, see Modules/*.c in Python source code.
"""
from sys import executable

#--- User options ----
PYTHON = executable
FILENAMES = ("/etc/issue", "/bin/ls")
SKIP_PRIVATE = True
PARSE_PROTOTYPE = True
DEBUG = False

# Functions and methods blacklist. Format:
#     module name => function names
# and module name:class name => method names
CTYPES = set((
    # Read/write arbitrary memory
    'PyObj_FromPtr', 'string_at', 'wstring_at',
    'call_function', 'call_cdeclfunction',
    'Py_INCREF', 'Py_DECREF',
    'dlsym', 'dlclose',

    '_string_at_addr', '_wstring_at_addr',
))

BLACKLIST = {
    # Dangerous module: ctypes
    'ctypes': CTYPES,
    '_ctypes': CTYPES,

    # Eat lot of CPU with large arguments
    'itertools': set(("tee",)),
    'math': set(("factorial",)),
    'operator': set(("pow",)),

    # Sleep
    'time': set(("sleep",)),
    'select': set(("epoll", "poll",)),
    'signal': set(("pause",)),

    # FIXME: test _sre.compile()
    '_sre': set(("compile",)),

    # set_authorizer: invalid callback
    '_sqlite3:Connection': set(("set_authorizer",)),

    # Connection(2392139129).poll() write in arbitrary memory
    '_multiprocessing:Connection': set(("poll",)),

    'posix': set((
        # exit python
        "_exit", "abort",
        # truncate file, remove directory, remove file
        "ftruncate", "rmdir", "unlink",
        # kill a process or ALL processes!
        "kill", "killpg",
        # wait process exit
        "wait", "waitpid",
    )),
}

if DEBUG:
    NB_CALL = 1
    NB_METHOD = 1
    NB_CLASS = 5
else:
    NB_CALL = 30
    NB_METHOD = 10
    NB_CLASS = 10
MAX_ARG = 6
MAX_VAR_ARG = 5

def setupProject(project):
    for filename in FILENAMES:
        if path_exists(filename):
            continue
        raise ValueError("File doesn't exist: %s! Fix FILENAMES constant" % filename)

    module_name = project.application().getInputFilename('Module name (use "ALL" to test all modules)')

    project.error("Use python interpreter: %s" % PYTHON)
    project.error("Use filenames: %s" % ', '.join(FILENAMES))

    source = PythonSource(project, module_name)
    process = PythonProcess(project, [PYTHON, '-u', '<source.py>'], timeout=10.0, stdin='null')
    WatchProcess(process, exitcode_score=0)

    stdout = WatchStdout(process)
    stdout.max_nb_line = (1000, 1.0)

    # Disable dummy error messages
    stdout.words = {
        'oops': 0.30,
        'bug': 0.30,
        'memory': 0.40,
        'overflow': 0.40,
        'fatal': 1.0,
        'assert': 1.0,
        'assertion': 1.0,
        'critical': 1.0,
        'panic': 1.0,
        'glibc detected': 1.0,
        'segfault': 1.0,
        'segmentation fault': 1.0,
    }

    # PyPy messages
    stdout.addRegex("Fatal RPython error", 1.0)

    if DEBUG:
        stdout.show_matching = True
        stdout.show_not_matching = True

USER_CLASS = 'FuzzingUserClass'
USER_OBJECT = 'fuzzing_user_object'

METHODS_NB_ARG = {
    '__str__': 0,
    '__repr__': 0,
    '__hash__': 0,
    '__reduce__': 0,
    '__delattr__': 1,
    '__getattribute__': 1,
    '__getitem__': 1,
    '__getslice__': 2,
    '__reduce_ex__': (0, 1),
    '__getstate__': 0,
    '__setattr__': 2,
    '__setstate__': 1,
}


from os.path import exists as path_exists
from fusil.process.watch import WatchProcess
from types import FunctionType, BuiltinFunctionType
from random import choice, randint
from fusil.bytes_generator import (
    IntegerGenerator, BytesGenerator, UnsignedGenerator, UnixPathGenerator,
    LETTERS, DECIMAL_DIGITS)
from fusil.process.stdout import WatchStdout
from fusil.project_agent import ProjectAgent
from fusil.process.create import CreateProcess
from inspect import ismethoddescriptor
from fusil.fuzzer.python import parseDocumentation
from ptrace.os_tools import RUNNING_PYPY

class PythonFuzzerError(Exception):
    pass

class PythonSource(ProjectAgent):
    def __init__(self, project, module_name):
        ProjectAgent.__init__(self, project, "python_source")
        if module_name != "ALL":
            self.modules = [module_name]
        else:
            self.modules = list(MODULES)

    def loadModule(self, module_name):
        self.module_name = module_name
        self.module = __import__(self.module_name)
        for name in self.module_name.split(".")[1:]:
            self.module = getattr(self.module, name)
        try:
            self.warning("Module filename: %s" % self.module.__file__)
        except AttributeError:
            pass
        self.write = WritePythonCode(self.filename, self.module, self.module_name)

    def on_session_start(self):
        session_dir = self.project().session.directory
        self.filename = session_dir.uniqueFilename('source.py')

        while self.modules:
            name = choice(self.modules)
            self.error("Test module %s" % name)
            try:
                self.loadModule(name)
                break
            except ImportError, err:
                self.error("IMPORT ERROR! %s" % err)
                self.modules.remove(name)
            except PythonFuzzerError, err:
                self.error("FUZZER ERROR! %s" % err)
                self.modules.remove(name)
        if not self.modules:
            self.error("There is no more modules!")
            self.send('project_stop')
            return

        self.write.writeSource()
        self.send('python_source', self.filename)

class PythonProcess(CreateProcess):
    def on_python_source(self, filename):
        self.cmdline.arguments[-1] = filename
        self.createProcess()

class WritePythonCode:
    def __init__(self, filename, module, module_name):
        self.simple_argument_generators = (
            self.genNone,
            self.genBool,
            self.genSmallUint,
            self.genInt,
            self.genLetterDigit,
            self.genString,
            self.genUnicode,
            self.genUnixPath,
            self.genFloat,
            self.genExistingFilename,
            self.genUserObject,
            self.genUserClass,
#            self.genOpenFile,
#            self.genException,
        )
        self.complex_argument_generators = self.simple_argument_generators + (
            self.genList,
            self.genTuple,
            self.genDict,
        )
        self.indent = ' ' * 4
        self.filename = filename
        self.base_level = 0
        self.smallint_generator = UnsignedGenerator(3)
        self.int_generator = IntegerGenerator(20)
        self.str_generator = BytesGenerator(0, 20)
        self.unix_path_generator = UnixPathGenerator(100)
        self.letters_generator = BytesGenerator(1, 8, LETTERS | DECIMAL_DIGITS)
        self.float_int_generator = IntegerGenerator(3)
        self.float_float_generator = UnsignedGenerator(3)
        self.module = module
        self.module_name = module_name

        self.functions, self.classes = self.getFunctions()
        if not self.functions and not self.classes:
            raise PythonFuzzerError("Module %s has no function and no class!" % self.module_name)

    def writeSource(self):
        self.output = open(self.filename, "w")
        self.write(0, "from sys import stderr")
        self.write(0, 'print "import %s"' % self.module_name)
        self.write(0, "import %s" % self.module_name)
        self.emptyLine()
        self.write(0, "class %s:" % USER_CLASS)
        self.write(1, "def __init__(self, x):")
        self.write(2, "self.x = x")
        self.emptyLine()
        self.write(1, "def test(self):")
        self.write(2, "print self.x")
        self.emptyLine()
        self.write(0, "%s = %s(42)" % (USER_OBJECT, USER_CLASS))
        self.emptyLine()
        self.writeCode(self.module_name, self.module, self.functions, self.classes, 1, NB_CALL)
        self.output.close()

    def getFunctions(self):
        classes = []
        functions = []
        try:
            blacklist = BLACKLIST[self.module_name]
        except KeyError:
            blacklist = set()
        for name in dir(self.module):
            attr = getattr(self.module, name)
            if name in blacklist:
                continue
            if isinstance(attr, (FunctionType, BuiltinFunctionType)):
                functions.append(name)
            elif isinstance(attr, type):
                classes.append(name)
        return functions, classes

    def getMethods(self, object, class_name):
        try:
            key = "%s:%s" % (self.module_name, class_name)
            blacklist = BLACKLIST[key]
        except KeyError:
            blacklist = set()
        methods = []
        for name in dir(object):
            if name in blacklist:
                continue
            if SKIP_PRIVATE and name.startswith("__"):
                continue
            attr = getattr(object, name)
            if not ismethoddescriptor(attr):
                continue
            methods.append(name)
        return methods

    def createComplexArgument(self):
        callback = choice(self.complex_argument_generators)
        return callback()

    def createArgument(self):
        callback = choice(self.simple_argument_generators)
        return callback()

    def getNbArg(self, func, func_name, min_arg):
        try:
            # Known method of arguments?
            value = METHODS_NB_ARG[func_name]
            if isinstance(value, tuple):
                min_arg, max_arg = value
            else:
                min_arg = max_arg = value
            return min_arg, max_arg
        except KeyError:
            pass

        if PARSE_PROTOTYPE:
            # Try using the documentation
            args = parseDocumentation(func.__doc__, MAX_VAR_ARG)
            if args:
                return args

        return min_arg, MAX_ARG

    def callFunction(self, func_index, context, func_name, func, min_arg):
        name = func_name
        func_name = "%s.%s" % (context, func_name)
        self.write(0, 'print "Call %s/%s: %s()"' % (
            1+func_index, self.nb_function, func_name))
        self.write(0, 'try:')
        self.write(1, '%s(' % func_name)
        min_arg, max_arg = self.getNbArg(func, name, min_arg)
        nb_arg = randint(min_arg, max_arg)
        self.base_level += 1
        for index in xrange(nb_arg):
            self.write(1, '# argument %s/%s' % (1+index, nb_arg))
            self.writeArgument(1)
        self.base_level -= 1
        self.write(1, ')')
        self.exceptBlock(0)
        self.emptyLine()

    def exceptBlock(self, level):
        self.write(level, 'except Exception, err:')
        self.write(level+1, 'print >>stderr, "ERROR: %s" % err')

    def writeArgument(self, level):
        lines = self.createComplexArgument()
        lines[-1] += ','
        for line in lines:
            self.write(level, line)

    def write(self, level, text):
        indent = self.indent * (self.base_level + level)
        print >>self.output, indent + text

    def emptyLine(self):
        print >>self.output

    def useClass(self, cls_index, context, cls, class_name):
        methods = self.getMethods(cls, class_name)
        class_name = "%s.%s" % (context, class_name)

        self.write(0, 'print "Class %s/%s: %s"' % (
            1 + cls_index, self.nb_class, class_name))
        obj_name = 'obj'
        self.write(0, 'try:')
        self.write(1, '%s = %s(' % (obj_name, class_name))

        nb_arg = randint(1, MAX_ARG)
        for index in xrange(nb_arg):
            self.write(2, '# argument %s/%s' % (1+index, nb_arg))
            self.writeArgument(2)
        self.write(1, ')')
        self.exceptBlock(0)
        self.write(0, 'else:')
        if methods:
            self.base_level += 1
            self.writeCode(obj_name, cls, methods, tuple(), 0, NB_METHOD)
            self.base_level -= 1
        self.write(1, 'del %s' % obj_name)
        self.emptyLine()

    def writeCode(self, context, object, functions, classes, func_min_arg, nb_call):
        if functions:
            self.nb_function = nb_call
            for index in xrange(self.nb_function):
                func_name = choice(functions)
                func = getattr(object, func_name)
                self.callFunction(index, context, func_name, func, func_min_arg)
        if classes:
            self.nb_class = NB_CLASS
            for index in xrange(self.nb_class):
                class_name = choice(classes)
                cls = getattr(object, class_name)
                self.useClass(index, context, cls, class_name)

    def genNone(self):
        return ['None']

    def genBool(self):
        if randint(0, 1) == 1:
            return ['True']
        else:
            return ['False']

    def genSmallUint(self):
        return [self.smallint_generator.createValue()]

    def genInt(self):
        return [self.int_generator.createValue()]

    def genString(self):
        bytes = self.str_generator.createValue()
        return ['"' + ''.join( r"\x%02X" % ord(byte) for byte in bytes) + '"']

    def genUnixPath(self):
        path = self.unix_path_generator.createValue()
        return ['"%s"' % path]

    def genLetterDigit(self):
        text = self.letters_generator.createValue()
        return ['"%s"' % text]

    def genUnicode(self):
        length = randint(0, 20)
        return ['u"' + ''.join( r"\u%04X" % randint(0, 65535) for index in xrange(length)) + '"']

    def genFloat(self):
        int_part = self.float_int_generator.createValue()
        float_part = self.float_float_generator.createValue()
        return ["%s.%s" % (int_part, float_part)]

    def genExistingFilename(self):
        filename = choice(FILENAMES)
        return ["'%s'" % filename]

    def genUserObject(self):
        return ["%s" % USER_OBJECT]

    def genUserClass(self):
        return ["%s" % USER_CLASS]

    def genOpenFile(self):
        filename = choice(FILENAMES)
        return ["open('%s')" % filename]

    def genException(self):
        return ["Exception('pouet')"]

    def _genList(self, open_text, close_text, empty, is_dict=False):
        # 90% of the time generate values of the same type
        same_type = (randint(0, 10) != 0)
        nb_item = randint(0, 10)
        if not nb_item:
            return [empty]
        items = []
        if same_type:
            if is_dict:
                key_callback = choice(self.simple_argument_generators)
            value_callback = choice(self.simple_argument_generators)
            for index in xrange(nb_item):
                if is_dict:
                    item = self.createDictItem(key_callback, value_callback)
                else:
                    item = value_callback()
                items.append(item)
        else:
            for index in xrange(nb_item):
                if is_dict:
                    item = self.createDictItem()
                else:
                    item = self.createArgument()
                items.append(item)
        lines = []
        for item_index, item_lines in enumerate(items):
            if item_index:
                lines[-1] += ","
                for index, line in enumerate(item_lines):
                    # Add ' ' suffix to all lines
                    item_lines[index] = ' ' + line
            lines.extend(item_lines)
        if nb_item == 1 and empty == 'tuple()':
            lines[-1] += ','
        lines[0] = open_text + lines[0]
        lines[-1] += close_text
        return lines

    def createDictItem(self, key_callback=None, value_callback=None):
        if key_callback:
            key = key_callback()
        else:
            key = self.createArgument()
        if value_callback:
            value = value_callback()
        else:
            value = self.createArgument()
        key[-1] += ": " + value[0]
        key.extend(value[1:])
        return key

    def genList(self):
        return self._genList('[', ']', '[]')

    def genTuple(self):
        return self._genList('(', ')', 'tuple()')

    def genDict(self):
        return self._genList('{', '}', '{}', True)

if RUNNING_PYPY:
    MODULES = (
        "exceptions", "_file", "sys", "__builtin__", "posix",
        "_codecs", "gc", "_weakref", "marshal", "errno",
        "math", "_sre", "operator",
        "symbol", "_random", "__pypy__", "sqlite",
        "_socket", "unicodedata", "mmap", "fcntl",
        "time" , "select", "zipimport", "_lsprof", "parser", "dyngram"
        "crypt", "signal", "termios", "zlib", "ctypes", "pyexpat", "array", "pwd",
        "struct", "md5", "sha", "bz2", "_minimal_curses", "cStringIO",
    )
else:
    # List generated from Python source code in Modules/ directory with command:
    #     /bin/grep -H InitModule $(find -name "*.c")|sed 's/.*("\(.*\)",.*/\1/g'|grep -v xx|sort -u
    # plus manual changes for lines like Py_InitModule*(PySocket_MODULE_NAME, ...)
    MODULES = """
al
array
audioop
binascii
_bisect
bsddb185
_bsddb
_bytesio
bz2
cd
cl
cmath
_codecs
_collections
cPickle
crypt
cStringIO
_csv
_ctypes
_ctypes_test
_curses
_curses_panel
datetime
dbm
dl
_elementtree
errno
fcntl
_fileio
fl
fm
fpectl
fpetest
_functools
future_builtins
gc
gdbm
gl
grp
_hashlib
_heapq
_hotshot
imageop
imgfile
itertools
_json
linuxaudiodev
_locale
_lsprof
math
_md5
mmap
_multibytecodec
_multiprocessing
nis
nt
operator
os2
ossaudiodev
parser
posix
pure
pwd
pyexpat
_random
readline
resource
select
sgi
_sha
_sha256
_sha512
signal
_socket
spwd
_sqlite3
_sre
_ssl
strop
_struct
sunaudiodev
sv
_symtable
syslog
termios
_testcapi
thread
time
timing
_tkinter
unicodedata
_weakref
zipimport
zlib
""".split()

