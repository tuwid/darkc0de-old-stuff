from errno import ENOENT
from os import chdir
from os.path import basename
from subprocess import Popen, STDOUT
from time import time
from fusil.process.cmdline import CommandLine
from fusil.process.env import Environment
from fusil.process.stdout import StdoutFile
from fusil.process.tools import (dumpProcessInfo,
    limitMemory, beNice, locateProgram)
from fusil.project_agent import ProjectAgent
from ptrace.os_tools import RUNNING_WINDOWS

if RUNNING_WINDOWS:
    from win32api import TerminateProcess

    def terminateProcess(process):
        TerminateProcess(process._handle, 1)
else:
    from os import kill
    from signal import SIGKILL

    def terminateProcess(process):
        kill(process.pid, SIGKILL)

class CreateProcess(ProjectAgent):
    def __init__(self, project, arguments=None, stdout="file", stdin=None, timeout=10.0, name=None):
        if not name:
            name = "process:%s" % basename(arguments[0])
        ProjectAgent.__init__(self, project, name)
        self.env = Environment(self)
        if arguments is None:
            arguments = []
        self.cmdline = CommandLine(self, arguments)
        self.timeout = timeout
        self.max_memory = 100*1024*1024
        self.stdout = stdout
        self.popen_args = {
            'stderr': STDOUT,
        }
        if stdin is not None:
            if stdin == "null":
                self.popen_args['stdin'] = open('/dev/null', 'r')
            else:
                raise ValueError("Invalid stdin value: %r" % stdin)

    def init(self):
        self.process = None
        self.timeout_reached = False
        self.is_running = False
        self.status = None

    def prepareProcess(self):
        # Change process priority to be nice
        beNice()

        # Set process priority to nice and limit memory
        if self.max_memory:
            limitMemory(self.max_memory)

        # Set current working directory
        directory = self.project().session.directory.directory
        chdir(directory)

    def createProcess(self):
        arguments = self.createArguments()
        for index, argument in enumerate(arguments):
            if "\0" in argument:
                raise ValueError("Argument %s contains nul byte: %r" % (index, argument))
        arguments[0] = locateProgram(arguments[0])
        popen_args = self.createPopenArguments()
        self.warning("Create process %r" % ' '.join(arguments))
        try:
            self.time0 = time()
            self.process = Popen(arguments, **popen_args)
        except OSError, err:
            if err.errno == ENOENT:
                raise ValueError("Program doesn't exist: %s" % arguments[0])
            else:
                raise
        dumpProcessInfo(self.info, self.process.pid)
        self.is_running = True
        self.send('process_create', self)
        self.send('process_pid', self, self.process.pid)

    def createPopenArguments(self):
        popen_args = dict(self.popen_args)
        popen_args['env'] = self.env.create()
        popen_args['stdout'] = StdoutFile(self).create()
        if not RUNNING_WINDOWS:
            popen_args['preexec_fn'] = self.prepareProcess
        return popen_args

    def createArguments(self):
        return self.cmdline.create()

    def poll(self):
        if self.is_running:
            status = self.process.poll()
            if status is not None:
                self.is_running = False
                self.status = status
        return self.status

    def live(self):
        if not self.is_running or not self.timeout:
            return
        if time() - self.time0 < self.timeout:
            return
        self.warning("Timeout! (%.1f second)" % self.timeout)
        self.timeout_reached = True
        self.destroyProcess()

    def destroyProcess(self):
        self.warning("Terminate process %s" % self.process.pid)
        terminateProcess(self.process)
        self.is_running = False
        if self.status is None:
            self.status = 1

    def deinit(self):
        if self.is_running:
             self.poll()
             if self.is_running:
                self.destroyProcess()
        self.process = None

class ProjectProcess(CreateProcess):
    def on_session_start(self):
        self.createProcess()

