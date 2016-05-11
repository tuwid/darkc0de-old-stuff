from sys import stderr
from fusil.mas.message import Message
from fusil.mas.mailbox import Mailbox
from weakref import ref as weakref_ref
from fusil.error import FUSIL_ERRORS, writeError
from fusil.mas.agent_id import AgentID

class AgentError(Exception):
    pass

class Agent(object):
    def __init__(self, name, mta):
        self.agent_id = AgentID().generate()
        self.is_active = False
        self.name = name
        self.setupMTA(mta)

    def setupMTA(self, mta, logger=None):
        if mta:
            if logger:
                self.logger = logger
            else:
                self.logger = mta.logger
            self.mta = weakref_ref(mta)
            self.mailbox = Mailbox(self, mta)
        else:
            self.logger = None
            self.mta = None
            self.mailbox = None

    def __cmp__(self, other):
        return cmp(self.agent_id, other.agent_id)

    def __del__(self):
        try:
            self.debug("Destroy")
            self.deactivate()
            if self.mailbox:
                self.mailbox.unregister()
            self.destroy()
        except KeyboardInterrupt:
            self.error("Agent destruction interrupted!")
            self.send('application_interrupt')
        except FUSIL_ERRORS, error:
            writeError(self, error, "Agent destruction error")

    def destroy(self):
        pass

    def getEvents(self):
        events = set()
        for attrname in dir(self):
            if attrname.startswith("on_"):
                events.add(attrname[3:])
        return events

    def send(self, event, *arguments):
        if not self.is_active:
            raise AgentError("Inactive agent are not allowed to send message!")
        message = Message(event, arguments)
        self.info("Send %r" % message)
        mta = self.mta()
        if mta is not None:
            mta.deliver(message)
        else:
            self.error("Unable to send %r: MTA is missing" % message)

    def readMailbox(self):
        count = 0
        while self.mailbox:
            message = self.mailbox.pop()
            message(self)
            count += 1
        return count

    def activate(self):
        if self.is_active:
            raise AgentError("%r is already activated!" % self)
        self.debug("Activate")
        self.mailbox.clear()
        self.is_active = True
        self.init()

    def deactivate(self):
        if not hasattr(self, 'is_active') or not self.is_active:
            return
        self.debug("Deactivate")
        self.is_active = False
        self.deinit()

    def init(self):
        pass

    def live(self):
        pass

    def deinit(self):
        pass

    def _log(self, level, message):
        try:
            func = getattr(self.logger, level)
        except AttributeError:
            if level == "error":
                print >>stderr, "(no logger)", message
            return
        func(message, sender=self)

    def debug(self, message):
        self._log('debug', message)

    def info(self, message):
        self._log('info', message)

    def warning(self, message):
        self._log('warning', message)

    def error(self, message):
        self._log('error', message)

    def __repr__(self):
        return '<%s id=%s, name=%r is_active=%s>' % (
            self.__class__.__name__, self.agent_id,
            self.name, self.is_active)

    def __str__(self):
        return repr(self)

