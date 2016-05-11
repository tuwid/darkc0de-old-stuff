from fusil.project_agent import ProjectAgent
from time import time

class TimeWatch(ProjectAgent):
    def __init__(self, project,
    too_fast=None, too_slow=None,
    too_fast_score=-1.0, too_slow_score=1.0):
        if too_fast is not None and too_slow is not None:
            if too_fast > too_slow:
                raise ValueError("too_fast > too_slow")
        else:
            if too_fast is None and too_slow is None:
                raise ValueError("TimeWatch requires too_fast or too_slow parameters")

        ProjectAgent.__init__(self, project, "time watch")
        self.too_fast = too_fast
        self.too_slow = too_slow
        self.too_fast_score = too_fast_score
        self.too_slow_score = too_slow_score
        self.time0 = None
        self.duration = None

    def init(self):
        self.score = None
        self.duration = None
        self.time0 = time()

    def getScore(self):
        return self.score

    def setScore(self, duration):
        if self.too_fast is not None and duration < self.too_fast:
            self.score = self.too_fast_score
        if self.too_slow is not None and duration > self.too_slow:
            self.score = self.too_slow_score

    def on_session_done(self, score):
        duration = time() - self.time0
        self.warning("Session done: duration=%.1f ms" % (duration*1000))
        self.setScore(duration)

