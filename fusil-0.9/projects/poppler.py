"""
libpoppler fuzzer using "pdftotext" command line program.
"""

AUTO_MANGLE = True

from fusil.process.time_watch import ProcessTimeWatch
from fusil.process.create import CreateProcess
from fusil.process.watch import WatchProcess
from fusil.process.stdout import WatchStdout
if AUTO_MANGLE:
    from fusil.auto_mangle import AutoMangle
else:
    from fusil.mangle import MangleFile
import re

def setupProject(project):
    USE_STDOUT = True

    time = ProcessTimeWatch(project,
        too_slow=3.0, too_slow_score=0.10,
        too_fast=0.100, too_fast_score=-0.80,
    )

    orig_filename = project.application().getInputFilename("PDF document")
    if AUTO_MANGLE:
        mangle = AutoMangle(project, orig_filename)
        mangle.hard_max_op = 1000
    else:
        mangle = MangleFile(project, orig_filename)
        mangle.config.max_op = 1000

    options = {'timeout': 5.0}
    if not USE_STDOUT:
        options['stdout'] = 'null'
    process = PopplerProcess(project, ['pdftotext'], **options)
    WatchProcess(process, exitcode_score=-0.10)

    if USE_STDOUT:
        stdout = WatchStdout(process)
        def cleanupLine(line):
            match = re.match(r"Error(?: \([0-9]+\))?: (.*)", line)
            if match:
                line = match.group(1)
            return line
        stdout.cleanup_func = cleanupLine
        del stdout.words['unknown']
#        stdout.show_not_matching = True
#        stdout.ignoreRegex(r"Unknown operator 'allocate'$")
#        stdout.ignoreRegex(r" operator is wrong type \(error\)$")
#        stdout.ignoreRegex(r'^No current point in lineto$')
#        stdout.ignoreRegex(r'^No current point in lineto')
#        stdout.ignoreRegex(r'^Unknown operator ')
#        stdout.ignoreRegex(r"^Couldn't open 'nameToUnicode' file ")
#        stdout.ignoreRegex(r"^Illegal character ")
#        stdout.ignoreRegex(r"^No font in show$")
#        stdout.ignoreRegex(r"^Element of show/space array must be number or string$")
#        stdout.ignoreRegex(r"^No current point in curveto$")
#        stdout.ignoreRegex(r"^Badly formatted number$")
#        stdout.ignoreRegex(r"^Dictionary key must be a name object$")
#        stdout.ignoreRegex(r"^End of file inside array$")
#        stdout.ignoreRegex(r"^Too few \([0-9]+\) args to .* operator$")
#        stdout.ignoreRegex(r"Too many args in content stream")
        stdout.max_nb_line = (100, 0.20)

class PopplerProcess(CreateProcess):
    def on_mangle_filenames(self, filenames):
        directory = self.project().session.directory
        text_filename = directory.uniqueFilename('output.txt')
        self.cmdline.arguments = (
            self.cmdline.arguments[0], filenames[0], text_filename)
        self.createProcess()

