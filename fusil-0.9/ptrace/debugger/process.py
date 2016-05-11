from ptrace.binding import (
    HAS_PTRACE_SINGLESTEP, HAS_PTRACE_EVENTS,
    HAS_PTRACE_SIGINFO, HAS_PTRACE_IO, HAS_PTRACE_GETREGS,
    ptrace_attach, ptrace_detach,
    ptrace_cont, ptrace_syscall,
    ptrace_setregs,
    ptrace_peektext, ptrace_poketext,
    REGISTER_NAMES)
if HAS_PTRACE_SINGLESTEP:
    from ptrace.binding import ptrace_singlestep
if HAS_PTRACE_SIGINFO:
    from ptrace.binding import ptrace_getsiginfo
if HAS_PTRACE_IO:
    from ctypes import create_string_buffer, addressof
    from ptrace.binding import (
        ptrace_io, ptrace_io_desc,
        PIOD_READ_D, PIOD_WRITE_D)
if HAS_PTRACE_EVENTS:
    from ptrace.binding import (
        ptrace_setoptions, ptrace_geteventmsg, WPTRACEEVENT,
        PTRACE_EVENT_FORK, PTRACE_EVENT_VFORK, PTRACE_EVENT_CLONE)
    NEW_PROCESS_EVENT = (PTRACE_EVENT_FORK, PTRACE_EVENT_VFORK, PTRACE_EVENT_CLONE)
if HAS_PTRACE_GETREGS:
    from ptrace.binding import ptrace_getregs
else:
    from ptrace.binding import ptrace_peekuser, ptrace_registers_t
from ptrace.os_tools import HAS_PROC
from ptrace.tools import dumpRegs
from ptrace.cpu_info import CPU_WORD_SIZE, CPU_PPC, CPU_64BITS, CPU_MAX_UINT
from ptrace.ctypes_tools import bytes2word, word2bytes
from signal import SIGTRAP, SIGSTOP, SIGKILL
from ptrace.ctypes_tools import formatAddress, formatWordHex
from ctypes import sizeof, cast, POINTER, c_char_p
from logging import debug, info, warning, error
from ptrace.error import PtraceError
from ptrace.signames import signalName
from errno import ESRCH, EACCES
from ptrace.debugger import (Breakpoint,
    ProcessExit, ProcessSignal, NewProcessEvent)
from os import (kill,
    WIFSTOPPED, WSTOPSIG,
    WIFSIGNALED, WTERMSIG,
    WIFEXITED, WEXITSTATUS)
import re
from ptrace.disasm import HAS_DISASSEMBLER
if HAS_DISASSEMBLER:
    from ptrace.disasm import disassemble, disassembleOne, MAX_INSTR_SIZE
if HAS_PROC:
     from ptrace.linux_proc import iterProc, ProcError
from ptrace.debugger.backtrace import getBacktrace

class ProcessError(PtraceError):
    def __init__(self, process, message):
        PtraceError.__init__(self, message, pid=process.pid)
        self.process = process

class PtraceProcess:
    def __init__(self, debugger, pid, is_attached, parent=None):
        self.debugger = debugger
        self.breakpoints = {}
        self.pid = pid
        self.running = True
        self.parent = parent
        self.is_attached = False
        self.is_stopped = True
        if not is_attached:
            self.attach()
        else:
            self.is_attached = True
        if HAS_PROC:
            self.read_mem_file = None

    def attach(self):
        if self.is_attached:
            return
        info("Attach process %s" % self.pid)
        ptrace_attach(self.pid)
        self.is_attached = True

    def dumpCode(self, address=None, manage_bp=False):
        try:
            ip = self.getInstrPointer()
        except PtraceError, err:
            if address is None:
                error("Unable to read instruction pointer: %s" % err)
                return
            ip = None
        if address is None:
            address = ip

        try:
            self._dumpCode(address, ip, manage_bp)
        except PtraceError, err:
            error("Unable to dump code at %s: %s" % (
                formatAddress(address), err))

    def _dumpCode(self, address, ip, manage_bp):
        if not HAS_DISASSEMBLER:
            code = self.readCode(address)
            text = " ".join( "%02x" % ord(byte) for byte in code )
            error("CODE: %s" % text)
            return

        if manage_bp:
            for line in xrange(10):
                bp = False
                if address in self.breakpoints:
                    bytes = self.breakpoints[address].old_bytes
                    instr = disassembleOne(bytes, address)
                    bp = True
                else:
                    instr = self.disassembleOne(address)
                text = "ASM %s: %s (%s)" % (formatAddress(instr.address), instr.text, instr.hexa)
                if instr.address == ip:
                    text += " <=="
                if bp:
                    text += "     * BREAKPOINT *"
                error(text)
                address = address+instr.size
        else:
            for instr in self.disassemble(address):
                text = "ASM %s: %s (%s)" % (formatAddress(instr.address), instr.text, instr.hexa)
                if instr.address == ip:
                    text += " <=="
                error(text)

    if HAS_DISASSEMBLER:
        def disassemble(self, address=None, nb_instr=10):
            before = 0
            # FIXME: Write better heuristic to read less bytes
            after = nb_instr * MAX_INSTR_SIZE
            if address is None:
                address = self.getInstrPointer()
            address += before
            code = self.readBytes(address, before+1+after)
            for index, instr in enumerate(disassemble(code, address)):
                yield instr
                if nb_instr and nb_instr <= (index+1):
                    break

        def disassembleOne(self, address=None):
            if address is None:
                address = self.getInstrPointer()
            code = self.readBytes(address, MAX_INSTR_SIZE )
            return disassembleOne(code, address)

    def findStack(self):
        if not HAS_PROC:
            return None
        try:
            regex = re.compile(r'^([0-9a-f]+)-([0-9a-f]+).*\[stack\]$')
            for line in iterProc("%s/maps" % self.pid):
                match = regex.match(line.rstrip())
                if not match:
                    continue
                start = int(match.group(1), 16)
                stop = int(match.group(2), 16)
                return (start, stop)
        except (PtraceError, ProcError):
            pass
        return None

    def detach(self):
        if not self.is_attached:
            return
        self.is_attached = False
        if self.running:
            info("Detach %s" % self)
            ptrace_detach(self.pid)
        self.debugger.deleteProcess(process=self)

    def _notRunning(self):
        self.running = False
        if not HAS_PROC:
            return
        if self.read_mem_file:
            try:
                self.read_mem_file.close()
            except IOError:
                pass
        self.detach()

    def kill(self, signum):
        debug("Send %s to %s" % (signalName(signum), self))
        kill(self.pid, signum)

    def terminate(self):
        if not self.running:
            return
        warning("Terminate %s" % self)
        done = False
        try:
            if self.is_stopped:
                self.cont(SIGKILL)
            else:
                self.kill(SIGKILL)
        except PtraceError, event:
            if event.errno == ESRCH:
                done = True
            else:
                raise event
        if not done:
            self.waitExit()
        self._notRunning()

    def waitExit(self):
        debug("Wait %s exit" % self)
        while True:
            # Wait for any process signal
            event = self.waitEvent()
            event_cls = event.__class__

            # Process exited: we are done
            if event_cls == ProcessExit:
                debug(str(event))
                return

            # Event different than a signal? Raise an exception
            if event_cls != ProcessSignal:
                raise event

            # Send the signal to the process
            signum = event.signum
            if signum not in (SIGTRAP, SIGSTOP):
                self.cont(signum)
            else:
                self.cont()

    def processStatus(self, status):
        # Process exited?
        if WIFEXITED(status):
            code = WEXITSTATUS(status)
            event = self.processExited(code)

        # Process killed by a signal?
        elif WIFSIGNALED(status):
            signum = WTERMSIG(status)
            event = self.processKilled(signum)

        # Invalid process status?
        elif not WIFSTOPPED(status):
            raise ProcessError(self, "Unknown process status: %r" % status)

        # Ptrace event?
        elif HAS_PTRACE_EVENTS and WPTRACEEVENT(status):
            event = WPTRACEEVENT(status)
            event = self.ptraceEvent(event)

        else:
            signum = WSTOPSIG(status)
            event = self.processSignal(signum)
        return event

    def processTerminated(self):
        debug("%s terminated abnormally" % self)
        self._notRunning()
        return ProcessExit(self)

    def processExited(self, code):
        debug("%s exited with code %s" % (self, code))
        self._notRunning()
        return ProcessExit(self, exitcode=code)

    def processKilled(self, signum):
        debug("%s killed by signal %s" % (self, signalName(signum)))
        self._notRunning()
        return ProcessExit(self, signum=signum)

    def processSignal(self, signum):
        debug("%s received signal %s" % (self, signalName(signum)))
        self.is_stopped = True
        return ProcessSignal(signum, self)

    if HAS_PTRACE_EVENTS:
        def ptraceEvent(self, event):
            debug("%s received ptrace event %s" % (self, event))
            if event not in NEW_PROCESS_EVENT:
                raise ProcessError(self, "Unknown ptrace event: %r" % event)
            new_pid = ptrace_geteventmsg(self.pid)
            debug("ptrace event %s from %s: new pid=%s" % (
                event, self, new_pid))
            new_process = self.debugger.addProcess(new_pid, is_attached=True, parent=self)
            return NewProcessEvent(new_process)

    if HAS_PTRACE_GETREGS:
        def getregs(self):
            return ptrace_getregs(self.pid)
    else:
        def getregs(self):
            error("Read registers using ptrace_peekuser()")
            words = []
            nb_words = sizeof(ptrace_registers_t) // CPU_WORD_SIZE
            for offset in xrange(nb_words):
                word = ptrace_peekuser(self.pid, offset*CPU_WORD_SIZE)
                bytes = word2bytes(word)
                words.append(bytes)
            bytes = ''.join(words)
            return cast(bytes, POINTER(ptrace_registers_t))[0]

    def getreg(self, name):
        # FIXME: Optimize the function when HAS_PTRACE_GETREGS is False
        if name not in REGISTER_NAMES:
            raise ProcessError(self, "Unknown register: %r" % name)
        regs = self.getregs()
        return getattr(regs, name)

    def setregs(self, regs):
        ptrace_setregs(self.pid, regs)

    def setreg(self, name, value):
        debug("Set register %s to %s" % (name, formatWordHex(value)))
        if name not in REGISTER_NAMES:
            raise ProcessError(self, "Unknown register: %r" % name)
        regs = self.getregs()
        setattr(regs, name, value)
        self.setregs(regs)

    if HAS_PTRACE_SINGLESTEP:
        def singleStep(self):
            info("Single step")
            ptrace_singlestep(self.pid)

    def syscall(self, signum=0):
        message = "Break process %s at next syscall" % self.pid
        if signum:
            message += ": continue with %s" % signalName(signum)
        info(message)
        ptrace_syscall(self.pid, signum)
        self.is_stopped = False

    if CPU_PPC:
        def getInstrPointer(self):
            return self.getreg('nip')

        def setInstrPointer(self, ip):
            self.setreg("nip", ip)

        def getStackPointer(self):
            # FIXME: Is it the right register?
            return self.getreg('gpr1')

        def getFramePointer(self):
            raise NotImplementedError()
    elif CPU_64BITS:
        def getInstrPointer(self):
            return self.getreg('rip')

        def setInstrPointer(self, ip):
            self.setreg("rip", ip)

        def getStackPointer(self):
            return self.getreg('rsp')

        def getFramePointer(self):
            return self.getreg('rbp')
    else:
        def getInstrPointer(self):
            return self.getreg('eip')

        def setInstrPointer(self, ip):
            self.setreg("eip", ip)

        def getStackPointer(self):
            return self.getreg('esp')

        def getFramePointer(self):
            return self.getreg('ebp')

    def _readBytes(self, address, size):
        debug("Read %s bytes at %s" % (size, formatAddress(address)))

        offset = address % CPU_WORD_SIZE
        if offset:
            # Read word
            address -= offset
            word = self.readWord(address)
            bytes = word2bytes(word)

            # Read some bytes from the word
            subsize = min(CPU_WORD_SIZE - offset, size)
            data = bytes[offset:offset+subsize]   # <-- FIXME: Big endian!

            # Move cursor
            size -= subsize
            address += CPU_WORD_SIZE
        else:
            data = ''

        while size:
            # Read word
            word = self.readWord(address)
            bytes = word2bytes(word)

            # Read bytes from the word
            if size < CPU_WORD_SIZE:
                data += bytes[:size]   # <-- FIXME: Big endian!
                break
            data += bytes

            # Move cursor
            size -= CPU_WORD_SIZE
            address += CPU_WORD_SIZE
        return data

    def readWord(self, address):
        """Address have to be aligned!"""
        word = ptrace_peektext(self.pid, address)
        debug("Read word at %s: %s" % (
            formatAddress(address), formatWordHex(word)))
        return word

    if HAS_PTRACE_IO:
        def readBytes(self, address, size):
            debug("Read %s bytes at %s" % (size, formatAddress(address)))
            buffer = create_string_buffer(size)
            io_desc = ptrace_io_desc(
                piod_op=PIOD_READ_D,
                piod_offs=address,
                piod_addr=addressof(buffer),
                piod_len=size)
            ptrace_io(self.pid, io_desc)
            return buffer.raw
    elif HAS_PROC:
        def readBytes(self, address, size):
            debug("Read %s bytes at %s" % (size, formatAddress(address)))

            if not self.read_mem_file:
                filename = '/proc/%u/mem' % self.pid
                try:
                    self.read_mem_file = open(filename, 'rb', 0)
                except IOError, err:
                    message = "Unable to open %s: fallback to ptrace implementation" % filename
                    if err.errno != EACCES:
                        error(message)
                    else:
                        info(message)
                    self.readBytes = self._readBytes
                    return self.readBytes(address, size)

            try:
                mem = self.read_mem_file
                mem.seek(address)
                return mem.read(size)
            except (IOError, ValueError), err:
                raise ProcessError(self, "readBytes(%s, %s) error: %s" % (
                    formatAddress(address), size, err))

        def getsiginfo(self):
            return ptrace_getsiginfo(self.pid)
    else:
        readBytes = _readBytes

    if HAS_PTRACE_IO:
        def writeBytes(self, address, bytes):
            size = len(bytes)
            debug("Write %s bytes at %s" % (
                size, formatAddress(address)))
            bytes = create_string_buffer(bytes)
            io_desc = ptrace_io_desc(
                piod_op=PIOD_WRITE_D,
                piod_offs=address,
                piod_addr=addressof(bytes),
                piod_len=size)
            ptrace_io(self.pid, io_desc)
    else:
        def writeBytes(self, address, bytes):
            debug("Write %s bytes at %s" % (
                len(bytes), formatAddress(address)))

            offset = address % CPU_WORD_SIZE
            if offset:
                # Write partial word (end)
                address -= offset
                size = CPU_WORD_SIZE - offset
                word = self.readBytes(address, CPU_WORD_SIZE)
                if len(bytes) < size:
                    size = len(bytes)
                    word = word[:offset] + bytes[:size] + word[offset + size:]  # <-- FIXME: Big endian!
                else:
                    word = word[:offset] + bytes[:size]   # <-- FIXME: Big endian!
                self.writeWord(address, bytes2word(word))
                bytes = bytes[size:]
                address += CPU_WORD_SIZE

            # Write full words
            while CPU_WORD_SIZE <= len(bytes):
                # Read one word
                word = bytes[:CPU_WORD_SIZE]
                word = bytes2word(word)
                self.writeWord(address, word)

                # Move to next word
                bytes = bytes[CPU_WORD_SIZE:]
                address += CPU_WORD_SIZE
            if not bytes:
                return

            # Write partial word (begin)
            size = len(bytes)
            word = self.readBytes(address, CPU_WORD_SIZE)
            # FIXME: Write big endian version of next line
            word = bytes + word[size:]
            self.writeWord(address, bytes2word(word))

    def readStruct(self, address, struct):
        debug("Read structure %s at %s" % (
            struct.__name__, formatAddress(address)))
        bytes = self.readBytes(address, sizeof(struct))
        if not CPU_64BITS:
            bytes = c_char_p(bytes)
        return cast(bytes, POINTER(struct))[0]

    def readArray(self, address, basetype, count):
        debug("Read array %sx%s at %s" % (
            basetype.__name__, count, formatAddress(address)))
        bytes = self.readBytes(address, sizeof(basetype)*count)
        if not CPU_64BITS:
            bytes = c_char_p(bytes)
        return cast(bytes, POINTER(basetype))

    def readCString(self, address, max_size, chunk_length=256):
        debug("Read char* at %s" % formatAddress(address))
        string = []
        size = 0
        truncated = False
        while True:
            done = False
            data = self.readBytes(address, chunk_length)
            if '\0' in data:
                done = True
                data = data[:data.index('\0')]
            if max_size <= size+chunk_length:
                data = data[:(max_size-size)]
                string.append(data)
                truncated = True
                break
            string.append(data)
            if done:
                break
            size += chunk_length
            address += chunk_length
        return ''.join(string), truncated

    def dumpStack(self):
        stack = self.findStack()
        if stack:
            error("STACK: %s..%s" % (
                formatAddress(stack[0]),
                formatAddress(stack[1])))
        try:
            self._dumpStack()
        except PtraceError, err:
            error("Unable to read stack: %s" % err)

    def _dumpStack(self):
        sp = self.getStackPointer()
        displayed = 0
        for index in xrange(-5, 5+1):
            delta = index * CPU_WORD_SIZE
            try:
                value = self.readWord(sp + delta)
                error("STACK%+ 3i: %s" % (delta, formatWordHex(value)))
                displayed += 1
            except PtraceError:
                pass
        if not displayed:
            error("ERROR: unable to read stack (%s)" % formatAddress(sp))

    def dumpMaps(self):
        if not HAS_PROC:
            return
        try:
            for line in iterProc("%s/maps" % self.pid):
                error("MAPS: %s" % line.rstrip())
        except ProcError, err:
            error("Unable to read memory mappings: %s" % err)

    def readCode(self, address=None, size=6*4):
        if address is None:
            address = self.getInstrPointer(),
        return self.readBytes(address, size)

    def writeWord(self, address, word):
        """
        Address have to be aligned!
        """
        debug("Write word %s at %s" % (
            formatWordHex(word), formatAddress(address)))
        ptrace_poketext(self.pid, address, word)

    def dumpRegs(self, log=None):
        if not log:
            log = error
        try:
            regs = self.getregs()
            dumpRegs(log, regs)
        except PtraceError, err:
            error("Unable to read registers: %s" % err)

    def cont(self, signum=0):
        if signum:
            info("Continue process %s (send signal %s)" % (
                self.pid, signalName(signum)))
        else:
            info("Continue process %s" % self.pid)
        ptrace_cont(self.pid, signum)
        self.is_stopped = False

    if HAS_PTRACE_EVENTS:
        def setoptions(self, options):
            info("Set %s options to %s" % (self, options))
            ptrace_setoptions(self.pid, options)

    def isStopped(self):
        return self.is_stopped

    def waitEvent(self):
        return self.debugger.waitProcessEvent(pid=self.pid)

    def waitSignals(self, *signals):
        return self.debugger.waitSignals(*signals, **{'pid': self.pid})

    def findBreakpoint(self, address):
        for bp in self.breakpoints.itervalues():
            if bp.address <= address < bp.address + bp.size:
                return bp
        return None

    def createBreakpoint(self, address, size=1):
        bp = self.findBreakpoint(address)
        if bp:
            raise ProcessError(self, "A breakpoint is already set: %s" % bp)
        bp = Breakpoint(self, address, size)
        self.breakpoints[address] = bp
        return bp

    def getBacktrace(self, max_args=6, max_depth=20):
        return getBacktrace(self, max_args=max_args, max_depth=max_depth)

    def removeBreakpoint(self, breakpoint):
        del self.breakpoints[breakpoint.address]

    def __del__(self):
        try:
            self.detach()
        except PtraceError:
            pass

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "<PtraceProcess #%s>" % self.pid

    def __hash__(self):
        return hash(self.pid)

