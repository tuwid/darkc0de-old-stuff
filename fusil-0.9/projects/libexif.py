"""
libexif fuzzer: use "exif picture.jpeg" command.

Supported file formats: JPEG
"""

INCR_MANGLE = True
DEBUG = False

def setupProject(project):
    orig_filename = project.application().getInputFilename("JPEG picture")
    if INCR_MANGLE:
        mangle = IncrMangle(project, orig_filename)
        mangle.operation_per_version = 25
        mangle.max_version = 50
#        mangle.min_offset = 2
#        mangle.max_offset = 555
    else:
        AutoMangle(project, orig_filename)

    process = IdentifyProcess(project,
        ['exif', "<picture>"])
    WatchProcess(process,
#        exitcode_score=-0.50,
        exitcode_score=0,
    )

    stdout = WatchStdout(process)
    stdout.min_nb_line = (3, -0.5)
    stdout.words['error'] = 0.10
    # "Color Space         |Internal error (unknown value 4097)." is not a fatal error
#    stdout.ignoreRegex(r'Internal error \(unknown value')
#    stdout.addRegex(r'^Corrupt data', -1.0)
#    stdout.addRegex(r'does not contain EXIF data!$', -1.0)
    stdout.addRegex(r'The data supplied does not seem to contain EXIF data.$', -1.0)
    stdout.addRegex(r'does not contain EXIF data!$', -1.0)
    stdout.addRegex(r'^Unknown encoding\.$', -1.0)
    if DEBUG:
        stdout.show_not_matching = True

from fusil.process.create import CreateProcess
from fusil.process.watch import WatchProcess
from fusil.process.stdout import WatchStdout
if INCR_MANGLE:
    from fusil.incr_mangle import IncrMangle
else:
    from fusil.auto_mangle import AutoMangle

class IdentifyProcess(CreateProcess):
    def on_mangle_filenames(self, image_filenames):
        self.cmdline.arguments[-1] = image_filenames[0]
        self.createProcess()

