"""
Generic UNIX command line program.
"""
from fusil.cmd_help_parser import CommandHelpParser
from fusil.process.create import CreateProcess
from fusil.process.watch import WatchProcess
from fusil.project_agent import ProjectAgent
from os.path import basename

class UnixProject(ProjectAgent):
    def __init__(self, project, program):
        ProjectAgent.__init__(self, project, "unix")
        self.program = program
        self.process = CreateProcess(project, name=basename(program))
        self.watch = WatchProcess(self.process)
        self.states = ("help", "stop")
        self.state = 0
        self.help_arguments = ("--help", "-help", "-h")
        self.state_data = None

    def nextState(self):
        self.state += 1

    def executeState(self):
        arguments = [self.program]
        state = self.states[self.state]
        if state == "help":
            if not self.state_data:
                self.state_data = iter(self.help_arguments)
            try:
                help = self.state_data.next()
            except StopIteration:
                self.nextState()
                self.executeState()
            arguments.append(help)
            self.process.cmdline.arguments = arguments
            self.process.createProcess()
        else: #state == "stop":
            self.send("project_stop")

    def on_session_start(self):
        self.executeState()

    def on_process_stdout(self, agent, stdout):
        self.stdout = stdout

    def on_process_done(self, agent, status):
        state = self.states[self.state]
        if state == "help":
            self.processHelp(status)

    def processHelp(self, status):
        if status != 0:
            return
        if 0 < status:
            print "EXITCODE: %s" % status
        self.stdout.seek(0)

        parser = CommandHelpParser()
        self.info("Parse command line help output")
        parser.parseFile(self.stdout)
        self.nextState()

    def on_session_done(self, score):
        self.stdout = None

def setupProject(project):
    program = project.application().getInputFilename("Program")
    unix = UnixProject(project, program)

