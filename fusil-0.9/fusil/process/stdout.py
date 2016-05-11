from fusil.file_watch import FileWatch
from fusil.session_agent import SessionAgent
from weakref import ref as weakref_ref

class StdoutFile(SessionAgent):
    def __init__(self, process):
        type = process.stdout
        if type not in ('null', 'file'):
            raise ValueError('Invalid stdout type: %r' % type)
        SessionAgent.__init__(self, process.project().session, "stdout file")
        self.type = type
        self.process = weakref_ref(process)

    def create(self):
        if self.type == "null":
            self.fileobj = open('/dev/null', 'wb')
        else:
            self.filename = self.session().directory.uniqueFilename('stdout')

            # output: write mode, unbuffered
            self.fileobj = open(self.filename, "w", 0)

            # input: read, unbuffered
            input = open(self.filename, "r", 0)

        if self.type != "null":
            self.send('process_stdout', self.process(), input)
        return self.fileobj.fileno()

    def on_process_stdout(self, agent, file_obj):
        if agent != self.process():
            return
        self.fileobj.close()

class WatchStdout(FileWatch):
    def __init__(self, process):
        FileWatch.__init__(self, process.project(), None, "watch:stdout")
        self.process = weakref_ref(process)

    def on_process_stdout(self, agent, file_obj):
        if agent != self.process():
            return
        self.setFileObject(file_obj)

    def deinit(self):
        FileWatch.deinit(self)
        self.file_obj = None

