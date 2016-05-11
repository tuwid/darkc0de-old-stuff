from fusil.project_agent import ProjectAgent
from weakref import ref as weakref_ref

class SessionAgent(ProjectAgent):
    def __init__(self, session, name, project=None):
        if project:
            mta = project.mta()
        else:
            mta = session.mta()
            project = session.project()
        self.session = weakref_ref(session)
        ProjectAgent.__init__(self, project, name, mta=mta)
        self.activate()

    def register(self):
        ProjectAgent.register(self)
        self.session().registerAgent(self)

    def unregister(self, destroy=True):
        ProjectAgent.unregister(self, destroy)
        self.session().unregisterAgent(self, destroy)

