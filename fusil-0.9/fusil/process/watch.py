from fusil.project_agent import ProjectAgent
from fusil.process.tools import dumpProcessInfo, displayProcessStatus
from weakref import ref as weakref_ref
from ptrace.os_tools import RUNNING_LINUX
if RUNNING_LINUX:
    from fusil.process.cpu_probe import CpuProbe

class WatchProcess(ProjectAgent):
    def __init__(self, process,
    exitcode_score=0.50, signal_score=1.0, default_score=0.0,
    timeout_score=1.0):
        self.process = weakref_ref(process)
        project = process.project()
        ProjectAgent.__init__(self, project, "watch:%s" % process.name)
        if RUNNING_LINUX:
            self.cpu = CpuProbe(project, "%s:cpu" % self.name)
        else:
            self.warning("CpuProbe is not available")
            self.cpu = None

        # Score if process exited normally
        self.default_score = default_score

        # Score if process exit code is not nul
        self.exitcode_score = exitcode_score

        # Score if process has been killed by signal
        self.signal_score = signal_score

        # Score if process timeout has been reached
        self.timeout_score = timeout_score

    def init(self):
        self.score = None
        self.pid = None

    def on_process_create(self, agent):
        if agent != self.process():
            return
        self.pid = agent.process.pid
        self.prepareProcess()

    def on_session_start(self):
        if self.pid is not None:
            self.prepareProcess()

    def prepareProcess(self):
        dumpProcessInfo(self.info, self.pid)
        if self.cpu:
            self.cpu.setPid(self.pid)

    def live(self):
        if not self.pid:
            return

        # Check if process is done or not
        status = self.process().poll()
        if status is not None:
            self.processDone(status)
            return

    def processDone(self, status):
        self.score = self.computeScore(status)
        if not self.process().timeout_reached:
            log = self.scoreLogFunc()
            displayProcessStatus(log, status)
        self.send("process_done", self.process(), status)
        self.send('session_stop')
        self.pid = None

    def getScore(self):
        return self.score

    def computeScore(self, status):
        # Timeout reached
        if self.process().timeout_reached:
            return self.timeout_score

        # No status: no way to compute score
        if status is None:
            return None

        # Process exit code is not nul?
        if 0 < status:
            return self.exitcode_score

        # Process killed by a signal
        if status < 0:
            return self.signal_score

        # Process exited normally: default score
        return self.default_score

    def deinit(self):
        self.pid = None

