from os import system as os_system, getenv, access, X_OK
from ptrace.os_tools import RUNNING_LINUX, RUNNING_WINDOWS
from os.path import join as path_join
from ptrace import signalName
from ptrace.process_tools import dumpProcessInfo
if RUNNING_LINUX:
    from ptrace.linux_proc import readProcessProcList, readProcessLink, ProcError
if RUNNING_WINDOWS:
    from win32process import SetPriorityClass, BELOW_NORMAL_PRIORITY_CLASS, IDLE_PRIORITY_CLASS
    from win32api import GetCurrentProcessId, OpenProcess
    from win32con import PROCESS_ALL_ACCESS

    def limitMemory(nbytes):
        pass

    def beNice(very_nice=False):
        if very_nice:
            value = BELOW_NORMAL_PRIORITY_CLASS
        else:
            value = IDLE_PRIORITY_CLASS

        pid = GetCurrentProcessId()
        handle = OpenProcess(PROCESS_ALL_ACCESS, True, pid)
        SetPriorityClass(handle, value)
else:
    from resource import setrlimit, RLIMIT_AS
    try:
        from os import nice
    except ImportError, err:
        # Workaround PyPy lack: it doesn't have os.nice()
        print "WARNING: Missing function os.nice()"
        def nice(level):
            pass

    def limitMemory(nbytes):
        setrlimit(RLIMIT_AS, (nbytes, -1))

    def beNice(very_nice=False):
        if very_nice:
            value = 10
        else:
            value = 5
        nice(value)

def displayProcessStatus(log, status):
    if status == 0:
        log("Process exited normally")
    elif status < 0:
        signum = -status
        log("Process killed by signal %s" %
            signalName(signum))
    else:
        log("Process exited with error code: %s" % status)

def system(logger, command):
    logger.info("Run command: %r" % command)
    exit_code = os_system(command)
    if not exit_code:
        return
    raise RuntimeError("Unable to run command %r (error %r)" % (
        command, exit_code))

def locateProgram(program):
    # FIXME: Fix for Windows
    if program[0] == '/':
        return program
    path = getenv('PATH')
    if not path:
        return program
    for dirname in path.split(":"):
        filename = path_join(dirname, program)
        if access(filename, X_OK):
            return filename
    return program

