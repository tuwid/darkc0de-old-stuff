from time import sleep
from fusil.mas.application_agent import ApplicationAgent
from fusil.error import FUSIL_ERRORS, writeError

class Univers(ApplicationAgent):
    def __init__(self, application, mta, step_sleep):
        ApplicationAgent.__init__(self, "univers", application, mta)
        self.is_done = False
        self.step_sleep = step_sleep

    def executeAgent(self, agent):
        if agent.is_active:
            self.debug("execute %s" % agent)
            agent.readMailbox()
            agent.live()
        else:
            self.debug("skip inactive %s" % agent)

    def execute(self, project):
        try:
            age = 0
            self.is_done = False
            while True:
                age += 1
                self.debug("Univers step %s" % age)
                # Execute one univers step
                for agent in project.agents:
                    self.executeAgent(agent)

                # Application is done? stop
                if self.is_done:
                    return

                # Be nice with CPU: sleep some milliseconds
                sleep(self.step_sleep)
        except KeyboardInterrupt:
            self.error("Interrupt!")
        except FUSIL_ERRORS, error:
            writeError(self, error)

    def on_univers_stop(self):
        self.is_done = True

