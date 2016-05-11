from fusil.time_watch import TimeWatch
from time import time

class ProcessTimeWatch(TimeWatch):
    def init(self):
        TimeWatch.init(self)
        self.time0 = None

    def on_process_create(self, agent):
        self.time0 = time()

    def on_session_done(self, score):
        pass

    def on_process_done(self, agent, status):
        duration = time() - self.time0
        self.warning("Process done: duration=%.1f ms" % (duration*1000))
        self.setScore(duration)

