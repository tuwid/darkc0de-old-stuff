"""
Classes mockup used for unit tests.
"""

from weakref import ref

class NullLogger:
    def __init__(self):
        self.show = False

    def debug(self, message, sender=None):
        self.display(message)

    def info(self, message, sender=None):
        self.display(message)

    def warning(self, message, sender=None):
        self.display(message)

    def error(self, message, sender=None):
        self.display(message)

    def display(self, message):
        if not self.show:
            return
        print message

class MTA:
    def __init__(self, logger=None):
        if not logger:
            logger = NullLogger()
        self.logger = logger

    def registerMailingList(self, mailbox, event):
        pass

class Options:
    def __init__(self):
        self.debug = False

class Application:
    def __init__(self):
        self.options = Options()

class Project:
    def __init__(self, logger=None):
        self._mta = MTA(logger)
        self.mta = ref(self._mta)
        self._application = Application()
        self.application = ref(self._application)

    def registerAgent(self, agent):
        pass

    def unregisterAgent(self, agent):
        pass

