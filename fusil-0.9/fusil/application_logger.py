from sys import stdout
from weakref import ref as weakref_ref
from logging import (getLogger, StreamHandler, Formatter,
    DEBUG, INFO, WARNING, ERROR)

LOG_FILENAME = 'fusil.log'

class ApplicationLogger:
    def __init__(self, application):
        self.application = weakref_ref(application)
        self.timestamp_format = '%(asctime)s: %(message)s'

        # Choose log levels
        if application.options.debug:
            stdout_level = INFO
            file_level = DEBUG
        elif application.options.verbose:
            stdout_level = WARNING
            file_level = INFO
        elif not application.options.quiet:
            stdout_level = ERROR
            file_level = WARNING
        else:
            stdout_level = ERROR
            file_level = INFO

        self.logger = getLogger()

        # fusil.log file
        self.filename = LOG_FILENAME
        self.file_handler = self.addFileHandler(self.filename, file_level)

        # Create stdout logger
        handler = StreamHandler(stdout)
        self.addHandler(handler, stdout_level)

    def addFileHandler(self, filename, level=None, mode='w', formatter=None):
        if level is None:
            if self.application().options.verbose:
                level = DEBUG
            else:
                level = INFO
        handler = StreamHandler(open(filename, mode))
        if not formatter:
            formatter = Formatter(self.timestamp_format)
        handler.setFormatter(formatter)
        self.addHandler(handler, level)
        return handler

    def addHandler(self, handler, level=None):
        handler.setLevel(level)
        self.logger.addHandler(handler)
        return handler

    def removeFileHandler(self, handler):
        handler.stream.close()
        self.removeHandler(handler)

    def removeHandler(self, handler):
        handler.close()
        self.logger.removeHandler(handler)

    def formatMessage(self, message, sender):
        message = str(message)
        application = self.application()
        prefix = []
        if application and application.project and application.project.session:
            verbose = application.options.verbose
            project = application.project
            prefix.append('[%s]' % project.nb_success)
            prefix.append('[session %s]' % project.session_index)
            if verbose and project.step:
                prefix.append('[step %s]' % project.step)
        else:
            verbose = False
        if verbose and sender is not None:
            prefix.append('[%s]' % sender.name)
        if prefix:
            message = ''.join(prefix)+' '+message
        return message

    def debug(self, message, sender):
        self.log(self.logger.debug, message, sender)

    def info(self, message, sender):
        self.log(self.logger.info, message, sender)

    def warning(self, message, sender):
        self.log(self.logger.warning, message, sender)

    def error(self, message, sender):
        self.log(self.logger.error, message, sender)

    def log(self, func, message, sender):
        message = self.formatMessage(message, sender)
        func(message)

