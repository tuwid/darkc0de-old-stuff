from errno import EEXIST
from os import mkdir
from os.path import basename

def safeMkdir(path):
    try:
        mkdir(path)
    except OSError, err:
        if err.errno == EEXIST:
            return
        else:
            raise

def filenameExtension(filename):
    ext = basename(filename)
    if '.' in ext:
        return '.'+ext.rsplit('.', 1)[-1]
    else:
        return None

