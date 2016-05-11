"""
Demonstration of poor gettext parser quality: inject errors
in valid .mo file and use it using dummy program (bash).
"""

def setupProject(project):
    # Locate MO full path
    mo_filename = 'libc.mo'
    COMMAND = ['/bin/bash', '/nonexistantpath']
    orig_filename = locateMO(project, COMMAND, mo_filename)

    # Create (...)/LC_MESSAGES/ directory
    LocaleDirectory(project, "locale_dir")

    # Create mangled MO file
    mangle = MangleGettext(project, orig_filename)
    mangle.max_size = None
    mangle.config.max_op = 2000

    # Run program with fuzzy MO file and special LANGUAGE env var
    process = GettextProcess(project, COMMAND)
    process.timeout = 10.0
    process.env.add(EnvVarValue('LANGUAGE'))
    process.env.copy('LANG')

    # Watch process failure with its PID
    # Ignore bash exit code (127: command not found)
    WatchProcess(process, exitcode_score=0)

    # Watch process failure with its text output
    stdout = WatchStdout(process)
    stdout.words['failed'] = 0


from fusil.process.create import CreateProcess
from fusil.process.watch import WatchProcess
from fusil.process.env import EnvVarValue
from fusil.process.stdout import WatchStdout
from fusil.auto_mangle import AutoMangle
from os.path import (basename, dirname,
    join as path_join, exists as path_exists)
from sys import stderr, exit
from os import unlink, mkdir
from fusil.process.tools import system
from fusil.project_agent import ProjectAgent
import re

STRACE = '/usr/bin/strace'

def locateMO(project, command, mo_filename):
    """
    Locate full path of a MO file used by a command using strace program.
    """
    command = ' '.join(command)
    log = '/tmp/strace'
    if path_exists(log):
        unlink(log)
    system(project, "%s -e open -o %s %s >/dev/null 2>&1" % (
        STRACE, log, command))
    regex = re.compile('open\("([^"]+%s)", [^)]+\) = [0-9]+' % mo_filename)
    for line in open(log):
        match = regex.match(line.rstrip())
        if match:
            return match.group(1)
    print >>stderr, "Unable to locate MO file (%s) used by command %r" \
        % (mo_filename, command)
    exit(1)

class LocaleDirectory(ProjectAgent):
    def on_session_start(self):
        directory = self.project().session.directory
        messages_dir = directory.uniqueFilename('LC_MESSAGES')
        mkdir(messages_dir)
        self.send('gettext_messages_dir', messages_dir)

class MangleGettext(AutoMangle):
    def on_aggressivity_value(self, value):
        self.aggressivity = value
        self.checkMangle()

    def checkMangle(self):
        if self.messages_dir and self.aggressivity is not None:
            self.mangle()

    def createFilename(self, index):
        return path_join(self.messages_dir, basename(self.source_filename))

    def on_gettext_messages_dir(self, messages_dir):
        self.messages_dir = messages_dir
        self.checkMangle()

    def init(self):
        self.messages_dir = None
        self.aggressivity = None

class GettextProcess(CreateProcess):
    def on_mangle_filenames(self, filenames):
        locale_dir = dirname(dirname(filenames[0]))
        self.env['LANGUAGE'].value = '../'*10 + locale_dir
        self.createProcess()

