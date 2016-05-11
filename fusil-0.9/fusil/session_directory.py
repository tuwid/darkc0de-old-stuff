from fusil.session_agent import SessionAgent
from fusil.directory import Directory
from os.path import basename

class SessionDirectory(SessionAgent, Directory):
    def __init__(self, session, directory):
        project = session.project()
        directory = project.directory.uniqueFilename('session',
            count=project.session_index)
        Directory.__init__(self, directory)
        SessionAgent.__init__(self, session, "directory:%s" % basename(self.directory))

    def init(self):
        self.info("Create directory: %s" % self.directory)
        self.mkdir()

    def keepDirectory(self):
        session = self.session()
        application = session.project().application()
        if not self.isEmpty(False):
            if session.isSuccess():
                # Session sucess and non-empty directory: keep directory
                self.warning("Success: keep directory %s" % self.directory)
                return True

            if application.exitcode:
                # Session sucess and non-empty directory: keep directory
                self.warning("Fusil error: keep directory %s" % self.directory)
                return True

            if application.options.keep_sessions:
                # User asked to keep all datas
                self.warning("Keep directory %s" % self.directory)
                return True

        if not application.options.remove_generated_files \
        and not self.isEmpty(True):
            # Project generated some extra files: keep the directory
            self.warning("Keep non-empty directory %s" % self.directory)
            return True

        # Remove empty directory
        return False

    def deinit(self):
        if self.keepDirectory():
            filename = basename(self.directory)
            self.project().directory.ignore(filename)
            return
        self.info("Remove directory %s" % self.directory)
        self.rmtree()

