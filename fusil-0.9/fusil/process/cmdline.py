from fusil.project_agent import ProjectAgent

class CommandLine(ProjectAgent):
    def __init__(self, process, arguments):
        ProjectAgent.__init__(self, process.project(), "%s:cmdline" % process.name)
        self.arguments = arguments

    def create(self):
        self.info("Command=%s" % ' '.join(self.arguments))
        return list(self.arguments)

