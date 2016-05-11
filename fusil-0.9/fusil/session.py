from fusil.project_agent import ProjectAgent
from fusil.session_agent import SessionAgent
from fusil.mas.agent_list import AgentList
from fusil.session_directory import SessionDirectory
from fusil.score import normalizeScore
from logging import INFO
from ptrace.os_tools import RUNNING_PYPY
from logging import Formatter
if RUNNING_PYPY:
    from gc import collect as gc_collect

class SessionFormatter(Formatter):
    """
    Log formatter for session.log: only write the message and
    remove fusil prefix:

    "[0][session 0010] text" => "text"
    """
    def format(self, record):
        text = record.getMessage()
        text = text.split("] ", 1)[1]
        return text

class Session(SessionAgent):
    def __init__(self, project):
        self.agents = AgentList()
        self.score = None
        self.log_handler = None
        SessionAgent.__init__(self, self, "session", project=project)

    def isSuccess(self):
        if self.score is None:
            return False
        return self.project().success_score <= self.score

    def computeScore(self, verbose=False):
        session_score = 0
        if verbose:
            self.info("Compute score")
        for agent in self.project().agents:
            if not issubclass(agent.__class__, ProjectAgent):
                # Skip application agent which has no score
                continue
            if not agent.is_active:
                continue
            score = agent.getScore()
            if score is None:
                continue
            score = normalizeScore(score)
            score *= agent.score_weight
            if verbose:
                self.info("%s score: %.1f%%" % (agent, score*100))
            session_score += score
        return session_score

    def writeAgents(self):
        self.debug("Project agents:")
        for agent in self.project().agents:
            self.debug("- %r" % agent)

    def registerAgent(self, agent):
        self.debug("Register %r" % agent)
        self.agents.append(agent)

    def unregisterAgent(self, agent, destroy=True):
        if agent not in self.agents:
            return
        self.debug("Unregister %r" % agent)
        self.agents.remove(agent, destroy)

    def init(self):
        directory = self.project().directory.directory
        self.directory = SessionDirectory(self, directory)

        log_filename = self.directory.uniqueFilename("session.log")
        self.log_handler = self.logger.addFileHandler(
            log_filename, level=INFO, formatter=SessionFormatter())

        self.stopped = False

    def on_session_start(self):
        self.writeAgents()

    def deinit(self):
        if self.log_handler:
            self.logger.removeFileHandler(self.log_handler)
        self.debug("Remove all session agents")
        self.agents.clear()
        if RUNNING_PYPY:
            gc_collect()

    def live(self):
        if self.stopped:
            return
        score = self.computeScore()
        if score is None:
            return
        project = self.project()
        if not(project.success_score <= score or score <= project.error_score):
            return
        self.send('session_stop')

    def on_session_stop(self):
        if self.stopped:
            return
        self.stopped = True
        score = self.computeScore(True)
        self.send('session_done', score)

