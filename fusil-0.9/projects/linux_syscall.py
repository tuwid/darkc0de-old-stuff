"""
Linux syscall fuzzer: generate random syscalls

Project based on "sysfuzz.c" fuzzer by Digital Dwarf Society
   http://www.digitaldwarf.be/
"""

from fusil.c_tools import FuzzyFunctionC, CodeC
from fusil.process.create import CreateProcess
from fusil.process.watch import WatchProcess
from random import choice, randint
from fusil.project_agent import ProjectAgent
from fusil.linux.syslog import Syslog
from ptrace.syscall import SYSCALL_NAMES

USERLAND_ADDRESS = "0x0804fd00"
UNMAPPED_ADDRESS = "0x0000a000"
# kernel addr, this is a guess ... should actually get a real one ...
KERNEL_ADDRESS = "0xc01fa0b6"

def setupProject(project):
    IGNORE_SYSCALLS = set((
        2, 120, 190, # fork, clone, vfork
        29, 72, # pause, sigsuspend (suspend until signal send)
        88, # reboot
        91, # munmap
        113, 166, # vm86old, vm86: enter VM86 mode (virtual-8086 in Intel literature)
        119, 173, # sigreturn, rt_sigreturn
        162, # nanosleep
        252, # epoll_wait
    ))

    syscall = GenerateSyscall(project)

    syscall.fixed_arguments[SYS_EXIT] = {1: "0"}
    syscall.fixed_arguments[SYS_OLD_SELECT] = {5: "0"}

    syscall.syscalls = list(set(SYSCALL_NAMES.keys()) - IGNORE_SYSCALLS)

    process = SyscallProcess(project, name="syscall")
    WatchProcess(process)
    syslog = Syslog(project)
    syslog.syslog.patterns['syscall'] = 1.0
    syslog.messages.patterns['syscall'] = 1.0

SYS_EXIT = 1
SYS_OLD_SELECT = 82
SYS_EPOLL_WAIT = 252

class SyscallProcess(CreateProcess):
    def on_syscall_program(self, program):
        self.cmdline.arguments = [program]
        self.createProcess()

class Main(FuzzyFunctionC):
    def __init__(self, syscall):
        FuzzyFunctionC.__init__(self, "main", type="int", random_bytes=400)
        self.footer.append('return 0;')
        self.syscall = syscall

    def getarg(self, syscall, arg_index):
        try:
            return self.syscall.fixed_arguments[syscall][arg_index]
        except KeyError:
            pass
        state = randint(0,4)
        if state == 0:
            return USERLAND_ADDRESS
        elif state == 1:
            return UNMAPPED_ADDRESS
        elif state == 2:
            return KERNEL_ADDRESS
        elif state == 3:
            return "%sU" % self.createInt32()
        else:
            return "&%s" % self.createRandomBytes()[0]

class GenerateSyscall(ProjectAgent):
    def __init__(self, project):
        ProjectAgent.__init__(self, project, "syscall")

        # Syscall parameters
        self.syscalls = xrange(0, 255+1)
        self.fixed_arguments = {}

    def on_session_start(self):
        # Intialize some parameters
        self.buffer_count = 0

        # Create program using C compiler
        code = CodeC()
        code.includes = [
            "<unistd.h>",
            "<sys/syscall.h>",
            "<stdlib.h>",
        ]
        main = Main(self)
        code.addFunction(main)
        main.footer = ['exit(0);']

        syscallnr = choice(self.syscalls)
        if syscallnr in SYSCALL_NAMES:
           syscall = "/* %s */ %s" % (SYSCALL_NAMES[syscallnr], syscallnr)
        else:
           syscall = str(syscallnr)

        arguments = [syscall]
        for index in xrange(1, 8+1):
            value = main.getarg(syscallnr, index)
            arguments.append("/* argument %s */ %s" % (index, value))
        main.callFunction("syscall", arguments)

        directory = self.project().session.directory
        self.c_filename = directory.uniqueFilename("syscall.c")
        self.program_filename = directory.uniqueFilename("syscall")

        code.compile(self, self.c_filename, self.program_filename)
        self.send('syscall_program', self.program_filename)

