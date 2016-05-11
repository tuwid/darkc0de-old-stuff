from fusil.project_agent import ProjectAgent
from fusil.linux.cpu_load import ProcessCpuLoad
from ptrace.linux_proc import ProcError
from time import time

class CpuProbe(ProjectAgent):
    def __init__(self, project, name,
    max_load=0.75, max_duration=3.0, max_score=1.0):
        ProjectAgent.__init__(self, project, name)
        self.max_load = max_load
        self.max_duration = max_duration
        self.max_score = max_score

    def init(self):
        self.score = None
        self.timeout = None
        self.load = None

    def setPid(self, pid):
        self.load = ProcessCpuLoad(pid)

    def live(self):
        # Read CPU load
        if not self.load:
            return
        try:
            load = self.load.get()
            if not load:
                return
        except ProcError:
            self.load = None
            return

        # Check maximum load
        if load < self.max_load:
            self.timeout = None
            return
        if self.timeout is None:
            self.warning("CPU load: %.1f%%" % (load*100))
            self.timeout = time()
            return

        # Check maximum duration
        duration = time() - self.timeout
        if duration < self.max_duration:
            return

        # Success
        self.score = self.max_score
        self.error("CPU load (%.1f%%) bigger than maximum (%.1f%%) during %.1f sec: score=%.1f%%"
            % (load*100, self.max_load*100, duration, self.score*100))
        self.load = None

    def getScore(self):
        return self.score

