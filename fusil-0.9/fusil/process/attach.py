from fusil.project_agent import ProjectAgent
from ptrace.linux_proc import ProcError, readProcessStatm, searchProcessByName
from fusil.process.tools import dumpProcessInfo
from os import kill
from ptrace.os_tools import RUNNING_LINUX
if RUNNING_LINUX:
    from fusil.process.cpu_probe import CpuProbe

class AttachProcess(ProjectAgent):
    def __init__(self, project, process_name):
        ProjectAgent.__init__(self, project, "attach_process:%s" % process_name)
        self.process_name = process_name
        self.death_score = 1.0
        self.max_memory = 100*1024*1024
        self.memory_score = 1.0
        if RUNNING_LINUX:
            self.cpu = CpuProbe(project, "%s:cpu" % self.name)
        else:
            self.warning("CpuProbe is not available")
            self.cpu = None

    def init(self):
        self.score = 0.0
        self.pid = None

    def setPid(self, pid):
        self.send('process_pid', self, pid)
        self.pid = pid
        dumpProcessInfo(self.info, self.pid)
        if self.cpu:
            self.cpu.setPid(pid)

    def on_session_start(self):
        pid = searchProcessByName(self.process_name)
        self.setPid(pid)

    def live(self):
        if self.pid is None:
            return
        if not self.checkAlive():
            return
        if self.max_memory:
            if not self.checkMemory():
                return

    def checkAlive(self):
        try:
            kill(self.pid, 0)
            return True
        except OSError:
            self.error("Process %s disappeared" % self.pid)
            self.stop(self.death_score)
            return False

    def checkMemory(self):
        try:
            memory = readProcessStatm(self.pid)[0]
            if self.max_memory < memory:
                self.error("Memory limit reached: %s > %s" % (
                    memory, self.max_memory))
                self.stop(self.memory_score)
            else:
                return True
        except ProcError, error:
            self.error(error)
            self.stop()
        return False

    def stop(self, score=None):
        if score:
            self.score = score
        self.pid = None

    def getScore(self):
        return self.score

