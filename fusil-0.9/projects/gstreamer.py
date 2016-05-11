"""
Gstreamer fuzzing project.
"""

INCR_MANGLE = False

def setupProject(project):
    TIMEOUT = 4
    GST_LAUNCH_BIN = 'gst-launch-0.10'
    USE_DECODEBIN = True
    NO_AUDIO = True
    NO_VIDEO = True

    # Profile parameters
    AUDIO_SINK = "alsasink"
    VIDEO_SINK = "xvimagesink"
    if NO_AUDIO:
        AUDIO_SINK = "fakesink"
    if NO_VIDEO:
        VIDEO_SINK = "fakesink"

    # Create buggy input file
    orig_filename = project.application().getInputFilename("Audio or video file")
    if INCR_MANGLE:
        mangle = IncrMangle(project, orig_filename)
        mangle.max_size = 50*1024
        # OGG
        #mangle.operation_per_version = 10
        #mangle.max_version = 100
        # WAVE
        #mangle.operation_per_version = 100
        #mangle.max_version = 30
        # AVI
        mangle.operation_per_version = 500
        mangle.max_version = 50
    else:
        mangle = AutoMangle(project, orig_filename)
        mangle.hard_max_op = 500
        mangle.max_size = 10*1024*1024

    if USE_DECODEBIN:
        # -f option: Do not install a fault handler
        arguments = [GST_LAUNCH_BIN, '-f',
            "filesrc", "location=<filename>", "!", "decodebin", "name=decoder",
            "decoder.", "!", "queue", "!", "audioconvert", "!", "audioresample", "!", AUDIO_SINK]
        if isVideo(orig_filename):
            arguments.extend(["decoder.", "!", "ffmpegcolorspace", "!", VIDEO_SINK])

        class GstreamerProcess(CreateProcess):
            def on_mangle_filenames(self, movie_filenames):
                self.cmdline.arguments[3] = 'location=' + movie_filenames[0]
                self.createProcess()
    else:
        arguments = [GST_LAUNCH_BIN, '-f', 'playbin', 'uri=file://<playbin_uri>']

        class GstreamerProcess(CreateProcess):
            def on_mangle_filenames(self, movie_filenames):
                self.cmdline.arguments[3] = 'uri=file://%s' % movie_filenames[0]
                self.createProcess()

    process = GstreamerProcess(project, arguments, timeout=TIMEOUT)

    WatchProcess(process, exitcode_score=0.20, timeout_score=0.20)
    #, timeout_score=0)
    setupX11Process(process)

    stdout = WatchStdout(process)
    stdout.words['error'] = 0.10
    stdout.words['critical'] = 0.30
    del stdout.words['assertion']
    stdout.addRegex(r'Could not decode stream\.$', -1.0)
    stdout.addRegex(r'Could not (?:decode stream|determine type of stream|demultiplex stream)\.$', -1.0)
    stdout.addRegex(r'The stream is of a different type than handled by this element\.$', -1.0)
    stdout.addRegex(r'You might need to install the necessary plugins', 1.0)
    stdout.score_weight = 0.40

from fusil.process.create import CreateProcess
from fusil.process.watch import WatchProcess
from fusil.process.stdout import WatchStdout
if INCR_MANGLE:
    from fusil.incr_mangle import IncrMangle
else:
    from fusil.auto_mangle import AutoMangle
from fusil.file_tools import filenameExtension
from fusil.x11 import setupX11Process

VIDEO_EXTENSIONS = (".avi", ".mkv", ".mov", ".mpg", ".mpeg", ".mp4")

def isVideo(filename):
    ext = filenameExtension(filename).lower()
    return ext in VIDEO_EXTENSIONS

