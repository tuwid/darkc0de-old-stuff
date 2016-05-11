"""
Mplayer audio/video mplayer.

Supported file formats:
 - AVI video
 - WAV audio
 - Ogg/Vorbis audio
 - Ogg/Theora video
 - Mastroska (.mkv) video
 - DVD
"""

def setupProject(project):
    # Command line
    MAX_FILESIZE = 1*1024*1024
    ARGUMENTS = ['-quiet']
    MPLAYER_BIN = 'mplayer'
    NULL_VIDEO = True
    if NULL_VIDEO:
        ARGUMENTS.extend(['-vo', 'null', '-ao', 'null'])
    if True:
        SECONDS = 5
        TIMEOUT = SECONDS + 1.0
        ARGUMENTS.extend(['-endpos', str(SECONDS)])
    else:
        TIMEOUT = 7.0

    # Create buggy input file
    orig_filename = project.application().getInputFilename("Audio or video file")
    mangle = AutoMangle(project, orig_filename)
    mangle.max_size = MAX_FILESIZE

    process = MplayerProcess(project,
        [MPLAYER_BIN] + ARGUMENTS + ["<movie_filename>"],
        timeout=TIMEOUT)
    if not NULL_VIDEO:
        setupX11Process(process)
    else:
        process.env.copy('HOME')
    watch = WatchProcess(process, timeout_score=0)
    if watch.cpu:
        watch.cpu.weight = 0.20
        watch.cpu.max_load = 0.50
        watch.cpu.max_duration = min(3, TIMEOUT-0.5)
        watch.cpu.max_score = 0.50

    stdout = WatchStdout(process)

    # Ignore input errors
    stdout.ignoreRegex('^Failed to open LIRC support')
    stdout.ignoreRegex("^Can't init input joystick$")
    stdout.ignoreRegex("^Can't open joystick device ")

    # Ignore codec loading errors
    stdout.ignoreRegex('^Failed to create DirectShow filter$')
    stdout.ignoreRegex('^Win32 LoadLibrary failed')
    stdout.ignoreRegex('^Error loading dll$')
    stdout.ignoreRegex('^ERROR: Could not open required DirectShow codec ')
    stdout.ignoreRegex("could not open DirectShow")

    # Ignore other errors
    stdout.ignoreRegex("^Terminal type `unknown' is not defined.$")
    stdout.ignoreRegex('^VDecoder init failed')
    stdout.ignoreRegex("Read error at pos\. [0-9]+")
    stdout.ignoreRegex("could not connect to socket")
    stdout.ignoreRegex('^ADecoder init failed')
    stdout.ignoreRegex('^error while decoding block:')
    stdout.ignoreRegex('^Error while decoding frame!$')
    stdout.ignoreRegex('^\[(mpeg4|msmpeg4|wmv1|h264|NULL) @ ')

    stdout.patterns['overflow'] = 0.10
#    stdout.words['error'] = 0.10
#    stdout.words["can't"] = 0
    stdout.addRegex('MPlayer interrupted by signal', 1.0)
    stdout.addRegex('AVI: Missing video stream', -0.50)
    stdout.max_nb_line = None

    # Restore terminal state
    TerminalEcho(project)

from fusil.process.create import CreateProcess
from fusil.process.watch import WatchProcess
from fusil.process.stdout import WatchStdout
from fusil.auto_mangle import AutoMangle
from fusil.terminal_echo import TerminalEcho
from fusil.x11 import setupX11Process

class MplayerProcess(CreateProcess):
    def on_mangle_filenames(self, movie_filenames):
        self.cmdline.arguments[-1] = movie_filenames[0]
        self.createProcess()

