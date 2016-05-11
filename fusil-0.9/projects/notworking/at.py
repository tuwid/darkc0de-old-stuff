"""
Fuzz at command line

Cleanup at queue after each session each.
"""

def setupProject(project):
    process = MyProcess(project, ['/usr/bin/at'], timeout=5.0)
    WatchProcess(process, exitcode_score=0.15)
    stdout = WatchStdout(process)
    stdout.ignoreRegex(r'Bug reports to')
    stdout.words['error'] = 0.10
    stdout.words['usage'] = 0.10

from fusil.process.create import ProjectProcess
from fusil.process.tools import system
from fusil.process.watch import WatchProcess
from fusil.process.stdout import WatchStdout
from fusil.bytes_generator import (
    BytesGenerator, UnixPathGenerator,
    ASCII0, DECIMAL_DIGITS)
from random import choice, randint

class MyProcess(ProjectProcess):
    def __init__(self, project, arguments, **kw):
        ProjectProcess.__init__(self, project, arguments, **kw)
        self.options = 'Vqfldbv'
        VALUE_SET = DECIMAL_DIGITS | set('.:-/ ')
        self.stdin_generator = BytesGenerator(1, 5000)
        self.value_generator = BytesGenerator(1, 30, VALUE_SET)
        self.queue_generator = BytesGenerator(1, 1, ASCII0)
        self.filename_generator = UnixPathGenerator(100)
        self.min_opt = 0
        self.max_opt = 2

    def createOption(self):
        option = choice(self.options)
        arg = '-' + option
        if option == 'q':
            return [arg, self.queue_generator.createValue()]
        elif option == 'f':
            return [arg, self.filename_generator.createValue()]
        else:
            return [arg]

    def createStdin(self):
        data = self.stdin_generator.createValue()

        filename = self.project().session.directory.uniqueFilename('stdin')
        open(filename, 'w').write(data)
        self.popen_args['stdin'] = open(filename, 'r')

    def createArguments(self):
        self.createStdin()

        arguments = self.cmdline.create()
        nb_opt = randint(self.min_opt, self.max_opt)
        for index in xrange(1, nb_opt+1):
            arg = self.createOption()
            arguments.extend(arg)

        timestamp = self.value_generator.createValue()
        arguments.append(timestamp)

        self.error("Arguments = %r" % arguments)
        return arguments

    def on_process_done(self, agent, status):
        system(self, r""" bash -c 'atq|awk "{print \$1}"|xargs -r atrm'""")

