from fusil.error import FusilError
from fusil.linux.cpu_load import SystemCpuLoad
from time import time, sleep

class SystemCalm:
    def __init__(self, max_load, sleep_second):
        self.load = SystemCpuLoad()
        self.max_load = max_load
        self.sleep = sleep_second
        self.first_message = 3.0
        self.repeat_message = 5.0
        self.max_wait = 60*5 # seconds (5 minutes)

    def wait(self, agent):
        first_message = False
        start = time()
        next_message = time() + self.first_message
        while True:
            load = self.load.get(estimate=False)
            if load <= self.max_load:
                break
            duration = time() - start
            if next_message < time():
                first_message = True
                next_message = time() + self.repeat_message
                agent.error("Wait until system load is under %.1f%% since %.1f seconds (current: %.1f%%)..."
                    % (self.max_load*100, duration, load*100))
            elif not first_message:
                first_message = True
                agent.info("Wait until system load is under %.1f%% (current: %.1f%%)..."
                    % (self.max_load*100, load*100))
            if self.max_wait <= duration:
                raise FusilError(
                    'Unable to calm down system load after ' \
                    '%.1f seconds (current load: %.1f%% > max: %.1f%%)' % (
                        duration, load*100, self.max_load*100))
            sleep(self.sleep)
        if first_message:
            duration = time() - start
            agent.info("System is now calm after %.1f seconds (current load: %.1f%%)" % (
                duration, load*100))

