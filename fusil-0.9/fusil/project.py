from fusil.project_agent import ProjectAgent
from fusil.session import Session
from imp import load_source
from weakref import ref as weakref_ref
from fusil.mas.agent_list import AgentList
from fusil.project_directory import ProjectDirectory
from time import time
from fusil.aggressivity import AggressivityAgent
from ptrace.os_tools import RUNNING_LINUX, RUNNING_PYPY
from os import unlink
from shutil import copyfile
if RUNNING_PYPY:
    from gc import collect as gc_collect
if RUNNING_LINUX:
    from fusil.system_calm import SystemCalm

class Project(ProjectAgent):
    def __init__(self, application):
        ProjectAgent.__init__(self, self, "project", mta=application.mta())
        self.application = weakref_ref(application)
        self.agents = AgentList()
        if RUNNING_LINUX:
            if application.options.fast:
                self.system_calm = SystemCalm(0.75, 0.2)
            elif not application.options.slow:
                self.system_calm = SystemCalm(0.50, 0.5)
            else:
                self.system_calm = SystemCalm(0.30, 3.0)
        else:
            self.warning("SystemCalm class is not available")
            self.system_calm = None

        # Configuration
        self.max_session = application.options.session
        self.success_score = 0.50 # minimum score for a successful session
        self.error_score = -0.50 # maximum score for a session failure
        self.max_success = application.options.success

        # Session
        self.session = None
        self.session_index = 0
        self.session_timeout = None # in second

        # Statistics
        self.session_executed = 0
        self.session_total_duration = 0
        self.total_duration = None

        # Add Application agents, order is important: MTA have to be the first agent
        for agent in application.agents:
            self.registerAgent(agent)
        self.registerAgent(self)

        # Create aggressivity agent
        self.aggressivity = AggressivityAgent(self)

        # Initial aggresssivity value
        if application.options.aggressivity is not None:
            self.aggressivity.setValue(application.options.aggressivity / 100)
            self.error("Initial aggressivity: %s" % self.aggressivity)

    def registerAgent(self, agent):
        self.debug("Register %r" % agent)
        self.agents.append(agent)

    def unregisterAgent(self, agent, destroy=True):
        if agent not in self.agents:
            return
        self.debug("Unregister %r" % agent)
        self.agents.remove(agent, destroy)

    def init(self):
        self.directory = ProjectDirectory(self)
        self.directory.activate()
        self.error("Use directory: %s" % self.directory.directory)

        self.initLog()

        self.project_start = time()
        self.step = None
        self.nb_success = 0
        self.createSession()

    def initLog(self):
        # Move fusil.log into run-xxx/project.log: copy fusil.log content
        # and then remove fusil.log file and log handler)
        logger = self.application().logger
        filename = self.directory.uniqueFilename("project.log")
        copyfile(logger.filename, filename)
        self.log_handler = logger.addFileHandler(filename, mode='a')
        logger.removeFileHandler(logger.file_handler)
        unlink(logger.filename)
        logger.filename = filename

    def deinit(self):
        self.summarize()
        self.aggressivity = None
        self.debug("Remove all project agents")
        for agent in self.application().agents:
            self.agents.remove(agent, False)
        self.agents.clear()

        remove = self.directory.destroy()
        if remove:
            logger = self.application().logger
            logger.removeFileHandler(self.log_handler)
            logger.filename = None

        self.directory = None
        if RUNNING_PYPY:
            gc_collect()

    def createSession(self):
        # Wait until system is calm
        if self.system_calm:
            self.system_calm.wait(self)

        self.info("Create session")
        self.step = 0
        self.session_index += 1
        self.session_start = time()

        # Enable project agents
        for agent in self.agents:
            if not agent.is_active:
                agent.activate()

        # Create session
        self.session = Session(self)

        # Send 'project_start' and 'session_start' message
        if self.session_index == 1:
            self.send('project_start')
        self.send('session_start')
        self.error("Start session")

    def destroySession(self):
        self.info("Destroy session")

        # Update statistics
        if not self.application().exitcode:
            self.session_executed += 1
            self.session_total_duration += (time() - self.session_start)

        # First deactivate session agents
        self.session.deactivate()

        # Deactivate project agents
        application_agents = self.application().agents
        for agent in self.agents:
            if agent not in application_agents:
                agent.deactivate()

        # Clear session variables
        self.step = None
        self.session = None

        # Remove waiting messages
        for agent in application_agents:
            agent.mailbox.clear()
        self.mta().clear()

    def on_session_done(self, session_score):
        self.send('project_session_destroy', session_score)

    def on_project_stop(self):
        self.send('univers_stop')

    def on_univers_stop(self):
        if self.session:
            self.destroySession()

    def on_project_session_destroy(self, session_score):
        # Use session score
        self.session.score = session_score
        duration = time() - self.session_start
        if self.project().success_score <= session_score:
            log = self.error
        else:
            log = self.warning
        log("End of session: score=%.1f%%, duration=%.3f second" % (
            session_score*100, duration))

        # Destroy session
        self.destroySession()

        # Session success? project is done
        if self.project().success_score <= session_score:
            self.nb_success += 1
            self.error("Success %s/%s!" % (self.nb_success, self.max_success))
            if self.max_success <= self.nb_success:
                self.send('univers_stop')
                return

        # Hit maximum number of session?
        if self.max_session and self.max_session <= self.session_index:
            self.error("Stop (limited to %s session)" % self.max_session)
            self.send('univers_stop')
            return

        # Otherwise: start new session
        self.createSession()

    def live(self):
        if self.step is not None:
            self.step += 1
        if not self.session:
            return
        if not self.session_timeout:
            return
        duration = time() - self.session_start
        if self.session_timeout <= duration:
            self.error("Timeout!")
            self.send('session_stop')

    def summarize(self):
        count = self.session_executed
        info = []
        if count:
            duration = self.session_total_duration
            info.append("%s session in %.1f second (%.1f ms per session)"
                % (count, duration, duration * 1000 / count))
        duration = time() - self.project_start
        info.append("total %.1f second" % duration)
        info.append("aggresssivity: %s" % self.aggressivity)
        self.error("Project done: %s" % ", ".join(info))
        self.error("Total: %s success" % self.nb_success)

def loadProject(application, filename):
    project = Project(application)
    source = load_source('', filename)
    source.setupProject(project)
    return project

