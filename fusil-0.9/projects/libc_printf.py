# -*- coding: UTF-8 -*-
"""
Generate valid printf format to test GNU libc implementation

Written using manual page to get all options.
"""

from random import choice, randint
from fusil.c_tools import encodeUTF32, quoteString, CodeC
from fusil.process.create import CreateProcess
from fusil.process.watch import WatchProcess
from fusil.project_agent import ProjectAgent
from ptrace.compatibility import any

def setupProject(project):
    printf = GeneratePrintfProgram(project)
    printf.max_nb_arg = 10

    # AVOID printf("%*d", 10000000, 42) crash
#    printf.max_width = 10*1000

    # AVOID "%.10000000s" crash
#    printf.max_precision = 10*1000

    # AVOID "%10000000hc" crash
    del printf.modifiers['char']['h']

    # AVOID "%qp" and "%llC" crashes
    for size in ('char', 'wide char', 'pointer'):
        for key in ('ll', 'q', 'j'):
            del printf.modifiers[size][key]

    process = PrintfProcess(project, name="printf", stdout='null')
    WatchProcess(process)

class PrintfProcess(CreateProcess):
    def on_printf_program(self, program):
        self.cmdline.arguments = [program]
        self.createProcess()

HELLO_UTF32 = encodeUTF32(u"Héllô")+"\0"*4

class GeneratePrintfArguments:
    def __init__(self, printf):
        self.printf = printf

    def genFormat(self, argument_index):
        # choose type
        prefix = None
        type = choice(self.printf.types)
        size = FORMAT_TO_SIZE[type]
        format = ['%']

        # add attribute
        format.append(choice(self.printf.format_attr))

        # add width
        rnd = randint(0, 2)
        if rnd == 1:
            format.append(str(randint(0, self.printf.max_width)))
        elif rnd == 2:
            width = randint(self.printf.min_width, self.printf.max_width)
            prefix = '/* width of x%s */ %s' % (argument_index, width)
            format.append('*')
            #if randint(0, 1) == 1:
            #    format.append('*')
            #else:
            #    format.append('%s$*%s$' % (
            #        argument_index+2, argument_index+1))

        # add precision
        if randint(0, 1) == 1:
            format.append('.%s' % randint(0, self.printf.max_precision))

        # add modifier
        if size in self.printf.modifiers:
            modifiers = self.printf.modifiers[size]
            keys = modifiers.keys()+[None]
            modifier = choice(keys)
            if modifier:
                format.append(modifier)
                size = modifiers[modifier]

        # add type
        format.append(type)
        return format, prefix, size

    def generate(self, nb_arg):
        text = []
        arguments = []
        for index in xrange(nb_arg):
            if text:
                text.append(' -- ')

            # Generate format and value
            format, prefix, size = self.genFormat(index)
            if size:
                value = self.printf.values[size]
            else:
                value = None

            # Append format and value
            format = ''.join(format)
            text.append('x%s' % index + '=' + format)
            if prefix:
                arguments.append(prefix)
            if value is not None:
                if value == "&written":
                    arguments.append('/* written bytes at x%s */ ' % index + value)
                else:
                    arguments.append('/* x%s value */ ' % index + value)
        text.append('\n')
        return [quoteString(''.join(text))]+arguments

class GeneratePrintfProgram(ProjectAgent):
    def __init__(self, project):
        ProjectAgent.__init__(self, project, "gen printf")

        # --- printf options ---
        self.min_nb_arg = 1
        self.max_nb_arg = 6
        self.types = 'aAcCdeEfFgGimnopuxXsS%'
        self.format_attr = ('#', '0', '-', ' ', '+', "'", 'I', '')
        self.min_width = 0
        self.max_width = 10*1000*1000
        self.max_precision = 10*1000*1000
        self.values = {
            'str': quoteString('Hello'),
            'wide str': quoteString(HELLO_UTF32),
            'char': "'A'",
            'wide char': "(wchar_t)322", # 'ł'
            'double': "(double)3.14",
            'short': "(short)7",
            'pointer': "(void *)0xDEADBEEF",
            'int': "(int)42",
            'intmax': "(intmax_t)232",
            'size_t': "(size_t)-1",
            'long': "(long)1234567890",
            'long long': "(long long)10101010",
            'ptrdiff_t': "(ptrdiff_t)100",
            'write': "&written",
            'long double': '(long double)5.92',
        }
        int_modifiers = {
            'hh': 'char',
            'h': 'short',
            'l': 'long',
            'll': 'long long',
            'q': 'long long',
            'j': 'intmax',
            'z': 'size_t',
            't': 'ptrdiff_t',
        }
        self.modifiers = {
            'int': dict(int_modifiers),
            'char': dict(int_modifiers),
            'wide char': dict(int_modifiers),
            'pointer': dict(int_modifiers),
            'str': {'l': 'wide str'},
            'wide str': {'l': 'wide str'},
            'double': {'L': 'long double'},
        }

    def on_session_start(self):
        self.use_locale = (randint(0, 1) == 0)
        self.use_asprintf = (randint(0, 1) == 0)

        # Generate printf() arguments
        nb_arg = randint(self.min_nb_arg, self.max_nb_arg)
        arguments = GeneratePrintfArguments(self).generate(nb_arg)
        self.info("Arguments: %s" % repr(arguments[1:]))
        self.info("Format: %s" % repr(arguments[0]))

        # Write C code to reproduce the bug
        code = CodeC()
        self.writeC(code, arguments)

        session_dir = self.project().session.directory
        self.c_filename = session_dir.uniqueFilename("printf.c")
        self.program_filename = session_dir.uniqueFilename("printf")

        code.compile(self, self.c_filename, self.program_filename, options="-Wno-format")
        self.send('printf_program', self.program_filename)

    def writeC(self, code, arguments):
        if self.use_asprintf:
            code.gnu_source = True
        code.includes = [
            '<stddef.h>',   # for ptrdiff_t
            '<stdint.h>',   # for intmax_t
            '<stdio.h>',    # for printf()
        ]
        if self.use_locale:
            code.includes.append('<locale.h>')  # for setlocale()
        main = code.addMain()

        if any( "&written" in text for text in arguments):
            main.variables.append('int written')

        if self.use_locale:
            main.callFunction('setlocale', ['LC_ALL', '""'])

        if self.use_asprintf:
            main.variables.append("char *text = NULL")
            arguments.insert(0, "&text")
            name = "asprintf"
        else:
            name = "printf"
        main.callFunction(name, arguments)

FORMAT_TO_SIZE = {
    's': 'str',
    'S': 'wide str',
    'c': 'char',
    'C': 'wide char',
    'p': 'pointer',
    'm': None,
    '%': None,
    'n': 'write',

    'a': 'double',
    'A': 'double',
    'e': 'double',
    'E': 'double',
    'f': 'double',
    'F': 'double',
    'g': 'double',
    'G': 'double',

    'i': 'int',
    'u': 'int',
    'd': 'int',
    'x': 'int',
    'X': 'int',
    'o': 'int',
    'O': 'int',
}

