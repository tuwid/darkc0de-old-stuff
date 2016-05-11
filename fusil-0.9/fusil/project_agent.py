from fusil.mas.agent import Agent
from weakref import ref as weakref_ref
from fusil.score import scoreLogFunc

class ProjectAgent(Agent):
    def __init__(self, project, name, mta=None):
        if not mta:
            mta = project.mta()
        Agent.__init__(self, name, mta)
        self.project = weakref_ref(project)
        if project is not self:
            self.score_weight = 1.0
            self.register()

    def register(self):
        self.project().registerAgent(self)

    def unregister(self, destroy=True):
        self.project().unregisterAgent(self, destroy)

    def scoreLogFunc(self):
        score = self.getScore()
        return scoreLogFunc(self, score)

    def getScore(self):
        # Score: floating number, -1.0 <= score <= 1.0
        #  1: bug found
        #  0: nothing special
        # -1: inputs rejected
        return None

