from os.path import (basename,
    join as path_join, exists as path_exists)
from os import mkdir, listdir, chmod
from shutil import rmtree

class Directory:
    def __init__(self, directory):
        self.directory = directory
        self.files = set()

    def ignore(self, filename):
        try:
            self.files.remove(filename)
        except KeyError:
            pass

    def mkdir(self):
        mkdir(self.directory)

    def isEmpty(self, ignore_generated=False):
        for filename in listdir(self.directory):
            if filename in ('.', '..'):
                continue
            if filename in self.files and ignore_generated:
                continue
            return False
        return True

    def rmtree(self):
        rmtree(self.directory, onerror=self.rmtree_error)

    def rmtree_error(self, operation, argument, stack):
        # Try to change file permission (allow write) and retry
        try:
            chmod(argument, 0700)
        except OSError:
            pass
        operation(argument)

    def uniqueFilename(self, name,
    count=None, count_format="%04d", save=True):
        # Test with no count suffix
        name = basename(name)
        if count is None and not self._exists(name):
            if save:
                self.files.add(name)
            return path_join(self.directory, name)

        # Create filename pattern: "archive.tar.gz" => "archive-%04u.tar.gz"
        name_pattern = name.split(".", 1)
        if count is None:
            count = 0
        count_format = "-" + count_format
        if 1 < len(name_pattern):
            name_pattern = name_pattern[0] + count_format + '.' + name_pattern[1]
        else:
            name_pattern = name_pattern[0] + count_format

        # Try names and increment count at each step
        while True:
            name = name_pattern % count
            if not self._exists(name):
                if save:
                    self.files.add(name)
                return path_join(self.directory, name)
            count += 1

    def _exists(self, name):
        if name in self.files:
            return True
        filename = path_join(self.directory, name)
        return path_exists(filename)

