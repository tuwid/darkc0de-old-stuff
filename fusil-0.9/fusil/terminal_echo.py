from fusil.project_agent import ProjectAgent
from ptrace.terminal import enableEchoMode

class TerminalEcho(ProjectAgent):
    def __init__(self, project):
        ProjectAgent.__init__(self, project, "terminal")

    def deinit(self):
        if enableEchoMode():
            self.error("Terminal: restore echo mode to stdin")

