"""
ImageMagick picture toolkit

Use "identify -verbose" command line.

Supported file formats: BMP, GIF, JPG, ICO, ...
"""

USE_CONVERT = False
INCR_MANGLE = False
USE_STDOUT = True

def setupProject(project):
    global CMDLINE_ARG_POS
    orig_filename = project.application().getInputFilename("Image")
    mangle = ImageMangle(project, orig_filename)
    if INCR_MANGLE:
        mangle.operation_per_version = 1
        mangle.max_version = 50
    else:
        mangle.fixed_size_factor = 0.5

    options = {'timeout': 2.0}
    if USE_CONVERT:
        cmdline = ['convert', '<source>', '/tmp/output.bmp']
        CMDLINE_ARG_POS = 1
    else:
        cmdline = ['identify', '-verbose', '<source>']
        CMDLINE_ARG_POS = -1
    if not USE_STDOUT:
        options['stdout'] = 'null'
    process = IdentifyProcess(project, cmdline, **options)
    options = {'exitcode_score': -0.25}
    if orig_filename.endswith(".jpg"):
        # Don't care about libjpeg stdout flooding
        options['timeout_score'] = -0.25
    WatchProcess(process, **options)

    if USE_STDOUT:
        stdout = WatchStdout(process)
        stdout.max_nb_line = (3000, 0.20)
        stdout.patterns['memory allocation failed'] = 1.0
        stdout.patterns['no decode delegate for this image format'] = -1.0
        stdout.addRegex('Corrupt', 0.05)
        stdout.addRegex('Unsupported', 0.05)
        stdout.addRegex('Not a JPEG file', -0.50)
        stdout.addRegex('JPEG datastream contains no image', -0.50)
        stdout.show_not_matching = False

from fusil.process.create import CreateProcess
from fusil.process.watch import WatchProcess
from fusil.process.stdout import WatchStdout
if INCR_MANGLE:
    from fusil.incr_mangle import IncrMangle as BaseMangle
else:
    from fusil.auto_mangle import AutoMangle as BaseMangle
from fusil.fixpng import fixPNG

class IdentifyProcess(CreateProcess):
    def on_mangle_filenames(self, image_filenames):
        self.cmdline.arguments[CMDLINE_ARG_POS] = image_filenames[0]
        self.createProcess()

class ImageMangle(BaseMangle):
    def mangleData(self, data, file_index):
        data = BaseMangle.mangleData(self, data, file_index)
        if self.source_filename.endswith(".png"):
            self.info("Fix CRC32 of PNG chunks")
            data = fixPNG(data)
        return data

