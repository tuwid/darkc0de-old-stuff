from logging import debug, info
from ptrace import PtraceError
from os import waitpid
from signal import SIGTRAP, SIGSTOP
from ptrace.signames import signalName
from errno import ECHILD
from ptrace.debugger import PtraceProcess, ProcessSignal
from ptrace.binding import HAS_PTRACE_EVENTS

class PtraceDebugger:
    def __init__(self):
        self.dict = {}   # pid -> PtraceProcess object
        self.list = []
        if HAS_PTRACE_EVENTS:
            self.options = 0

    def addProcess(self, pid, is_attached, parent=None):
        if pid in self.dict:
            raise KeyError("Process % is already registered!" % pid)
        process = PtraceProcess(self, pid, is_attached, parent=parent)
        info("Attach %s to debugger" % process)
        self.dict[pid] = process
        self.list.append(process)
        process.waitSignals(SIGTRAP, SIGSTOP)
        if HAS_PTRACE_EVENTS and self.options:
            process.setoptions(self.options)
        return process

    def quit(self, terminate=True):
        info("Quit debugger")
        # Terminate processes in reverse order
        # to kill children before parents
        processes = list(self.list)
        for process in reversed(processes):
            if terminate:
                process.terminate()
            process.detach()

    def _waitpid(self, wanted_pid):
        if wanted_pid:
            if wanted_pid not in self.dict:
                raise PtraceError("Unknown PID: %r" % wanted_pid, pid=wanted_pid)

            debug("Wait process %s" % wanted_pid)
            try:
                pid, status = waitpid(wanted_pid, 0)
            except OSError, err:
                if err.errno == ECHILD:
                    process = self[wanted_pid]
                    raise process.processTerminated()
                else:
                    raise err
        else:
            debug("Wait any process")
            pid, status = waitpid(-1, 0)

        if wanted_pid and pid != wanted_pid:
            raise PtraceError("Unwanted PID: %r (instead of %s)"
                % (pid, wanted_pid), pid=pid)
        return pid, status

    def _wait(self, wanted_pid):
        process = None
        while not process:
            pid, status = self._waitpid(wanted_pid)
            try:
                process = self.dict[pid]
            except KeyError:
                info("waitpid() warning: Unknown PID %r" % pid)
        return process.processStatus(status)

    def waitProcessEvent(self, pid=None):
        return self._wait(pid)

    def waitSignals(self, *signals, **kw):
        """
        No signal means "any signal"
        """
        pid = kw.get('pid', None)

        message = "Wait "
        if pid:
            message += "process %s for " % pid
        if signals:
            message += "signals (%s)" % ", ".join(
                signalName(signum)
                for signum in signals)
        else:
            message += "any signal"
        info(message)
        while True:
            event = self._wait(pid)
            if event.__class__ != ProcessSignal:
                raise event
            signum = event.signum
            if signum in signals or not signals:
                return event
            raise event

    def deleteProcess(self, process=None, pid=None):
        if not process:
            try:
                process = self.dict[pid]
            except KeyError:
                return
        debug("Remove %s" % process)
        try:
            del self.dict[process.pid]
        except KeyError:
            pass
        try:
            self.list.remove(process)
        except ValueError:
            pass

    if HAS_PTRACE_EVENTS:
        def setoptions(self, options):
            info("Set debugger ptrace options: %s" % options)
            self.options = options

    def __getitem__(self, pid):
        return self.dict[pid]

    def __iter__(self):
        return iter(self.list)

    def __len__(self):
        return len(self.list)

