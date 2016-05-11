"""
librpm fuzzer using "rpm" command program.
Inject errors in valid RPM file and then recompute MD5 and SHA1 checksums.
"""
from fusil.process.create import CreateProcess
from fusil.process.watch import WatchProcess
from fusil.process.stdout import WatchStdout
from fusil.mangle import MangleFile
from array import array
from md5 import md5
from sha import sha

USE_HACHOIR = False
if USE_HACHOIR:
    from hachoir_core import config as hachoir_config
    from hachoir_core.stream import StringInputStream
    from hachoir_parser import guessParser

class MangleRPM(MangleFile):
    def useHachoirParser(self, parser):
        last = None
        sha1_offset = None
        md5_offset = None
        if "checksum" in parser:
            for item in parser.array('checksum/item'):
                last = item
                if 'tag' not in item or 'offset' not in item:
                    continue
                tag = item['tag'].value
                if tag == 269:
                    sha1_offset = item['offset'].value
                elif tag == 1004:
                    md5_offset = item['offset'].value
        if last:
            offset0 = (last.absolute_address + last.size) // 8
            if sha1_offset is not None:
                self.sha1_offset = offset0 + sha1_offset
#                print "FIX SHA1 OFFSET: %s" % self.sha1_offset
            if md5_offset is not None:
                self.md5_offset = offset0 + md5_offset
#                print "FIX SHA1 OFFSET: %s" % self.md5_offset
        if "header" in parser:
            header = parser['header']
            self.header_offset = header.absolute_address // 8
#            print "FIX HEADER OFFSET: %s" % self.header_offset
            self.filedata_offset = self.header_offset + (header.size // 8)
#            print "FIX FILE DATA OFFSET: %s" % self.filedata_offset

    def mangleData(self, data, index):
        self.sha1_offset = 208
        self.md5_offset = 256
        self.header_offset = 360
        self.filedata_offset = 3170

        data = MangleFile.mangleData(self, data, index)

        if USE_HACHOIR:
            #data.tofile(open('/tmp/oops', 'wb'))
            hachoir_config.quiet = True
            data_str = data.tostring()
            parser = guessParser(StringInputStream(data_str))
            if parser:
                self.useHachoirParser(parser)

        summary_data = data[self.header_offset:].tostring()
        checksum = md5(summary_data).digest()
        data[self.md5_offset:self.md5_offset+16] = array('B', checksum)

        summary_data = data[self.header_offset:self.filedata_offset].tostring()
        checksum = sha(summary_data).hexdigest()
        data[self.sha1_offset:self.sha1_offset+40] = array('B', checksum)

        return data

def setupProject(project):
    orig_filename = project.application().getInputFilename("RPM archive")
    mangle = MangleRPM(project, orig_filename)
    if True:
        mangle.config.max_op = 200
    else:
        mangle.config.min_op = 0
        mangle.config.max_op = 0

    process = RpmProcess(project,
        ['/usr/bin/rpm', '-qpi', 'file.rpm'],
        timeout=10.0)
    WatchProcess(process)

    stdout = WatchStdout(process)
    stdout.patterns['memory allocation failed'] = 1.0

class RpmProcess(CreateProcess):
    def on_mangle_filenames(self, rpm_filenames):
        self.cmdline.arguments[-1] = rpm_filenames[0]
        self.createProcess()

