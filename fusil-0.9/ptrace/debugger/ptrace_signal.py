from logging import error
from ptrace.disasm import HAS_DISASSEMBLER
from signal import SIGFPE, SIGCHLD, SIGSEGV, SIGABRT
from ptrace.os_tools import RUNNING_LINUX
from ptrace.cpu_info import CPU_64BITS
from ptrace.debugger import ProcessEvent
from ptrace.ctypes_tools import formatAddress
from ptrace.error import PtraceError
from ptrace import signalName
from ptrace.process_tools import formatProcessStatus
import re

class SignalInfo(Exception):
    def display(self):
        pass

class DivisionByZero(SignalInfo):
    def __init__(self, info):
        self.info = info

    def display(self):
        error("Division by zero: %s" % self.info)

class Abort(SignalInfo):
    def display(self):
        error("Program received signal SIGABRT, Aborted.")

class StackOverflow(SignalInfo):
    def __init__(self, stack_ptr, stack_start, stack_end):
        self.stack_ptr = stack_ptr
        self.stack_start = stack_start
        self.stack_end = stack_end

    def display(self):
        error("STACK OVERFLOW! Stack pointer (%s) is not in %s-%s" % (
            formatAddress(self.stack_ptr),
            formatAddress(self.stack_start),
            formatAddress(self.stack_end)))

class InvalidMemoryAcces(SignalInfo):
    def __init__(self, address=None, text=None,
    prefix_addr="Invalid memory access to %s", prefix="Invalid memory access"):
        self.prefix_addr = prefix_addr
        self.prefix = prefix
        self.text = text
        self.address = address

    def display(self):
        if self.address is not None:
            if isinstance(self.address, (list, tuple)):
                address = " or ".join( formatAddress(addr) for addr in self.address )
            else:
                address = formatAddress(self.address)
            message = self.prefix_addr % address
        else:
            message = self.prefix
        if self.text:
            message = "%s: %s" % (message, self.text)
        error(message)

class InvalidRead(InvalidMemoryAcces):
    def __init__(self, address=None, text=None):
        InvalidMemoryAcces.__init__(self, address, text,
            "Invalid read from %s", "Invalid read")

class InvalidWrite(InvalidMemoryAcces):
    def __init__(self, address=None, text=None):
        InvalidMemoryAcces.__init__(self, address, text,
            "Invalid write to %s", "Invalid write")

class InstructionError(SignalInfo):
    def __init__(self, address):
        self.address = address

    def display(self):
        error("UNABLE TO EXECUTE CODE AT %s (SEGMENTATION FAULT)" % formatAddress(self.address))

class ChildExit(SignalInfo):
    def __init__(self, pid=None, status=None, uid=None):
        self.pid = pid
        self.status = status
        self.uid = uid

    def display(self):
        if self.pid is not None and self.status is not None:
            message = formatProcessStatus(self.status, "Process %s" % self.pid)
            error(message)
        else:
            error("Child process exited")
        if self.uid is not None:
            error("Signal sent by user %s" % self.uid)

class ProcessSignal(ProcessEvent):
    def __init__(self, signum, process):
        # Initialize attributes
        self.name = signalName(signum)
        ProcessEvent.__init__(self, process, "Signal %s" % self.name)
        self.signum = signum
        self.error = None

    def _analyze(self):
        if self.signum == SIGSEGV:
            self.memoryFault()
        elif self.signum == SIGFPE:
            self.mathError()
        elif self.signum == SIGCHLD:
            self.childExit()
        elif self.signum == SIGABRT:
            self.error = Abort()
        return self.error

    def getInstruction(self):
        if not HAS_DISASSEMBLER:
            return None
        try:
            return self.process.disassembleOne()
        except PtraceError:
            return None

    def memoryFaultInstr(self, instr, fault_address):
        error_cls = None
        asm = instr.text
        deref = r'(?:BYTE |WORD |DWORD )?\[[^]]+\]'

        # "MOV [...], value" instruction
        match = re.search(r"^(?:MOV|TEST)[A-Z]* %s," % deref, asm)
        if match:
            self.error = InvalidWrite(fault_address, text=asm)
            return

        # "CMP [...], value" instruction
        match = re.search(r"^(?:CMP[A-Z]*|TEST) %s," % deref, asm)
        if match:
            self.error = InvalidRead(fault_address, text=asm)
            return

        # "MOV reg, [...]" instruction
        match = re.match(r"(?:MOV|TEST|CMP)[A-Z]* [^,]+, %s" % deref, asm)
        if match:
            self.error = InvalidRead(fault_address, text=asm)
            return

        # "MOVS*" instructions
        match = re.search(r"^(?:REP )?MOVS", asm)
        if match:
            error_cls = InvalidMemoryAcces
            try:
                if CPU_64BITS:
                    di = self.process.getreg('rdi')
                    si = self.process.getreg('rsi')
                else:
                    di = self.process.getreg('edi')
                    si = self.process.getreg('esi')
                if fault_address is not None:
                    if fault_address == di:
                        error_cls = InvalidRead
                    elif fault_address == si:
                        error_cls = InvalidWrite
                else:
                    fault_address = (di, si)
            except PtraceError:
                pass
            self.error = error_cls(fault_address, text=asm)
            return

    def getSignalInfo(self):
        if RUNNING_LINUX:
            return self.process.getsiginfo()
        else:
            return None

    def memoryFault(self):
        # Get fault
        siginfo = self.getSignalInfo()
        if siginfo:
            fault_address = siginfo._sigfault._addr
            if not fault_address:
                 fault_address = 0
        else:
             fault_address = None

        # Call to invalid address?
        if fault_address is not None:
            try:
                ip = self.process.getInstrPointer()
                if ip == fault_address:
                    self.error = InstructionError(ip)
                    return
            except PtraceError:
                pass

        # Stack overflow?
        stack = self.process.findStack()
        if stack:
            sp = self.process.getStackPointer()
            if not (stack[0] <= sp <= stack[1]):
                self.error = StackOverflow(sp, stack[0], stack[1])
                return

        # Guess error type using the assembler instruction
        instr = self.getInstruction()
        if instr:
            self.memoryFaultInstr(instr, fault_address)
            if self.error:
                return

        # Last chance: use generic invalid memory access error
        if fault_address is not None:
            self.error = InvalidMemoryAcces(fault_address)

    def mathError(self):
        instr = self.getInstruction()
        if not instr:
            return
        match = re.match(r"I?DIV (.*)", instr.text)
        if not match:
            return
        self.error = DivisionByZero(instr.text)

    def childExit(self):
        siginfo = self.getSignalInfo()
        if siginfo:
            child = siginfo._sigchld
            self.error = ChildExit(child.pid, child.status, child.uid)
        else:
            self.error = ChildExit()

    def display(self):
        self._analyze()
        error("-" * 60)
        error("PID: %s" % self.process.pid)
        error("Signal: %s" % self.name)
        if self.error:
            self.error.display()
        error("-" * 60)

