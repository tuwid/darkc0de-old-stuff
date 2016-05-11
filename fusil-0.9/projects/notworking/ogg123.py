"""
ogg123
"""

FILESIZE = 32*1024
COMMAND = ['ogg123', '-d', 'null', '--quiet', '<file.ogg>']
#COMMAND = ['ogginfo', '<file.ogg>']
#COMMAND = ['oggdec', '--quiet', '<file.ogg>']
INCR_MANGLE = False

def setupProject(project):
    orig_filename = project.application().getInputFilename("OGG/Vorbis file")
    mangle = OggMangle(project, orig_filename)
    if not INCR_MANGLE:
        mangle.hard_min_op = 1
        mangle.hard_max_op = 100
    else:
        from fusil.incr_mangle_op import InverseBit, Increment
        mangle.operations = (InverseBit, Increment)
    mangle.max_filesize = FILESIZE

    process = OggProcess(project, COMMAND, timeout=60.0)
    process.env.copy('HOME')

    if COMMAND[0] == 'ogg123':
        WatchProcess(process, exitcode_score=-0.25)
    else:
        WatchProcess(process, exitcode_score=0)
    stdout = WatchStdout(process)
    if True:
    #    stdout.max_nb_line = (5000, 1.0)
        stdout.show_matching = True
        stdout.show_not_matching = True
        stdout.addRegex(r"The file may be corrupted", -0.50)
        stdout.addRegex(r"Corrupted ogg", -0.50)
        stdout.addRegex(r"Could not decode vorbis header packet", -0.50)
    #    stdout.ignoreRegex('^Warning: Could not decode vorbis header packet')
        stdout.ignoreRegex('^Warning: sequence number gap')
        stdout.ignoreRegex('^New logical stream.*: type invalid$')

from fusil.process.create import CreateProcess
from fusil.process.watch import WatchProcess
from fusil.process.stdout import WatchStdout
if INCR_MANGLE:
    from fusil.incr_mangle import IncrMangle as OggMangle
else:
    from fusil.auto_mangle import AutoMangle as OggMangle

class OggProcess(CreateProcess):
    def on_mangle_filenames(self, filenames):
        self.cmdline.arguments[-1] = filenames[0]
        self.createProcess()

