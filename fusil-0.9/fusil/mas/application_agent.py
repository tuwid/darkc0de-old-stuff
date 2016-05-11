from fusil.mas.agent import Agent
from weakref import ref as weakref_ref

class ApplicationAgent(Agent):
    def __init__(self, name, application, mta):
        Agent.__init__(self, name, mta)
        self.application = weakref_ref(application)
        if application is not self:
            self.register()

    def register(self):
        self.application().registerAgent(self)

    def unregister(self, destroy=True):
        self.application().unregisterAgent(self, destroy)

