"""
ClamAV anti-virus.

Supported file formats:
 - ZIP, CAB archive
 - JPEG
 - Windows PE program (.exe)
 - HTML
"""

from fusil.process.create import CreateProcess
from fusil.process.watch import WatchProcess
from fusil.process.attach import AttachProcess
from fusil.process.stdout import WatchStdout
from fusil.auto_mangle import AutoMangle
from fusil.file_watch import FileWatch

class ClamavProcess(CreateProcess):
    def on_mangle_filenames(self, new_files):
        self.cmdline.arguments = self.cmdline.arguments[0:1] + new_files
        self.createProcess()

def setupProject(project):
    USE_DAEMON = True
    if USE_DAEMON:
        NB_FILE = 3
        PROGRAM = 'clamdscan'
    else:
        NB_FILE = 20
        PROGRAM = 'clamscan'

    orig_filename = project.application().getInputFilename("ClamAV valid file (eg. program)")

    mangle = AutoMangle(project, orig_filename, NB_FILE)
    mangle.config.max_op = 100
    mangle.config.change_size = True

    # Watch clamd server
    if USE_DAEMON:
        AttachProcess(project, 'clamd')

    process = ClamavProcess(project, [PROGRAM], timeout=100.0)
    WatchProcess(process, exitcode_score=0.10)

    if USE_DAEMON:
        log = FileWatch(project, open('/var/log/clamav/clamav.log'),
            'clamav.log', start="end")
    else:
        log = WatchStdout(process)
    log.ignoreRegex('SCAN SUMMARY')
    log.ignoreRegex(': OK$')
    log.ignoreRegex('^Infected files: ')
    log.ignoreRegex('^Time: ')
    log.addRegex(' FOUND$', 0.05)
    log.words['error'] = 0.30 / NB_FILE
    log.patterns[r"Can't connect to clamd"] = 1.0
    log.show_not_matching = True

