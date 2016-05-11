from fusil.project_agent import ProjectAgent
from os.path import basename
from os import fstat
from stat import ST_SIZE
from array import array

class MangleAgent(ProjectAgent):
    def __init__(self, project, source, nb_file=1):
        ProjectAgent.__init__(self, project, "mangle:%s" % basename(source))
        self.source_filename = source
        self.max_size = None # 10*1024*1024
        self.nb_file = nb_file

    def readData(self, filename, file_index):
        # Open file and read file size
        self.warning("Load input file: %s" % filename)
        data = open(filename, 'rb')
        orig_filesize = fstat(data.fileno())[ST_SIZE]
        if not orig_filesize:
            raise ValueError("Input file (%s) is empty!" % filename)

        # Read bytes
        if self.max_size:
            data = data.read(self.max_size)
        else:
            data = data.read()

        # Display message if input is truncated
        if len(data) < orig_filesize:
            percent = len(data) * 100.0 / orig_filesize
            self.warning("Truncate file to %s bytes (%.2f%% of %s bytes)" \
                % (len(data), percent, orig_filesize))

        # Convert to Python array object
        return array('B', data)

    def writeData(self, filename, data):
        self.warning("Generate file: %s" % filename)
        output = open(filename, 'w')
        data.tofile(output)
        return filename

    def createFilename(self, file_index):
        if 1 < self.nb_file:
            count = 1
        else:
            count = None
        directory = self.project().session.directory
        return directory.uniqueFilename(self.source_filename, count=count)

    def mangle(self):
        filenames = []
        for file_index in xrange(self.nb_file):
            data = self.readData(self.source_filename, file_index)
            data = self.mangleData(data, file_index)
            filename = self.createFilename(file_index)
            self.writeData(filename, data)
            filenames.append(filename)
        self.send('mangle_filenames', filenames)

    # --- Abstract methods ---

    def mangleData(self, data, file_index):
        raise NotImplementedError()

    def on_session_start(self):
        self.mangle()

