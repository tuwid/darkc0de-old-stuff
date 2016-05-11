from optparse import OptionParser
from sys import exit
from fusil.mas.application_agent import ApplicationAgent
from fusil.mas.mta import MTA
from fusil.mas.univers import Univers
from fusil.error import FUSIL_ERRORS, writeError
from fusil.application_logger import ApplicationLogger
from fusil.project import loadProject
from fusil.process.tools import limitMemory, beNice
from fusil.version import VERSION, LICENSE, WEBSITE
from fusil.process.watch import dumpProcessInfo
from fusil.mas.agent_list import AgentList
from os import getpid

class Application(ApplicationAgent):
    def __init__(self):
        self.agents = AgentList()
        ApplicationAgent.__init__(self, "application", self, None)
        self.setup()

    def registerAgent(self, agent):
        self.debug("Register %r" % agent)
        self.agents.append(agent)

    def unregisterAgent(self, agent, destroy=True):
        if agent not in self.agents:
            return
        self.debug("Unregister %r" % agent)
        self.agents.remove(agent, destroy)

    def parseOptions(self):
        parser = OptionParser(usage="%prog [options] --project=NAME [arg1 arg2 ...]")
        parser.add_option("--project", '-p', help="Project filename",
            type="str", default=None)
        parser.add_option("--session", help="Maximum number of session (default: none)",
            type="int")
        parser.add_option("--success", help="Maximum number of success sessions (default: 5)",
            type="int", default=5)
        parser.add_option("--remove-generated-files", help="Remove a session directory even if it contains generated files",
            action="store_true")
        parser.add_option("--keep-sessions", help="Do not remove session directories",
            action="store_true")
        parser.add_option("--fast", help="Run faster as possible (opposite of --slow)",
            action="store_true")
        parser.add_option("--slow", help="Try to keep system load low: be nice with CPU (opposite of --fast)",
            action="store_true")
        parser.add_option("--version", help="Display Fusil version (%s) and exit" % VERSION,
            action="store_true")
        parser.add_option("--aggressivity", help="Initial aggressivity factor in percent, value in -100.0..100.0 (default: 0.0%%)",
            type="float", default=None)
        parser.add_option('-v', "--verbose", help="Enable verbose mode (set log level to WARNING)",
            action="store_true")
        parser.add_option("--quiet", help="Be quiet (lowest log level), don't create log file",
            action="store_true")
        parser.add_option("--profiler", help="Enable Python profiler",
            action="store_true")
        parser.add_option("--debug", help="Enable debug mode (set log level to DEBUG)",
            action="store_true")
        self.options, self.arguments = parser.parse_args()

        # Just want to know the version?
        if self.options.version:
            print "Fusil version %s" % VERSION
            print "License: %s" % LICENSE
            print "Website: %s" % WEBSITE
            print
            exit(0)

        if self.options.quiet:
            self.options.debug = False
            self.options.verbose = False
        if self.options.debug:
            self.options.verbose = True
        if not self.options.project:
            parser.print_help()
            exit(1)

    def setup(self):
        # Read command line options
        self.parseOptions()

        # Application objects
        self.max_memory = 100*1024*1024
        self.exitcode = 0
        self.project = None

        # Limit Fusil environment
        beNice(True)
        if self.max_memory:
            limitMemory(self.max_memory)

        # Create logger
        self.logger = ApplicationLogger(self)
        self.error("Fusil version %s -- %s" % (VERSION, LICENSE))
        self.error(WEBSITE)
        dumpProcessInfo(self.info, getpid())

        # Create multi agent system
        self.createMAS()

    def createMAS(self):
        # Create mail transfer agent (MTA)
        self.mta = None
        mta = MTA(self)

        # Create univers
        if self.options.fast:
            step_sleep = 0.005
        elif not self.options.slow:
            step_sleep = 0.010
        else:
            step_sleep = 0.050
        self.univers = Univers(self, mta, step_sleep)

        # Finish to setup application
        self.setupMTA(mta, self.logger)
        self.registerAgent(self)

        # Activate agents
        mta.activate()
        self.activate()
        self.univers.activate()

    def exit(self):
        if self.logger.filename:
            self.error("Fusil log written into %s" % self.logger.filename)
        self.error("Exit Fusil")
        self.mta = None
        self.univers = None
        self.agents.clear()

    def getInputFilename(self, description):
        arguments = self.arguments
        if not arguments:
            raise RuntimeError("Missing filename argument: %s" %
                description)
        return arguments[0]

    def executeProject(self):
        self.project.activate()
        self.univers.execute(self.project)
        self.project.deactivate()

    def runProject(self, filename):
        # Load project
        self.error("Load project %s" % filename)
        self.project = loadProject(self, filename)
        self.registerAgent(self.project)

        # Execute project
        self.executeProject()

        # Destroy project
        self.info("Destroy project")
        self.unregisterAgent(self.project)
        self.project = None

    def on_application_interrupt(self):
        self.error("User interrupt!")
        self.send('univers_stop')

    def on_application_error(self, message):
        self.error(message)
        self.exitcode = 1
        self.send('univers_stop')

    def main(self):
        try:
            if self.options.profiler:
                from fusil.profiler import runProfiler
                runProfiler(self, self.runProject, (self.options.project,))
            else:
                self.runProject(self.options.project)
        except KeyboardInterrupt:
            self.error("Project interrupted!")
            self.exitcode = 1
        except FUSIL_ERRORS, error:
            writeError(self, error)
            self.exitcode = 1
        return self.exitcode

