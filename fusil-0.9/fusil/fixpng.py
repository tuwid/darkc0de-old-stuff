from array import array
from StringIO import StringIO
from hachoir_core.bits import str2long, BIG_ENDIAN, long2raw
from zlib import crc32
from logging import info

def pngCRC32(data):
    return crc32(data) & 0xFFFFFFFF

def fixPNG(data):
    # array -> str
    data = data.tostring()

    origdata = data
    datalen = len(data)
    data = StringIO(data)

    data.seek(0)
    data.write("\x89PNG\r\n\x1a\n")

    index = 8
    while index < (datalen-4):
        data.seek(index)
        size = str2long(data.read(4), BIG_ENDIAN)
        chunksize = size+12
        if datalen < (index+chunksize):
            info("fixPNG: Skip invalid chunk at %s" % index)
            break
        crcofs = index+chunksize-4
        data.seek(crcofs)
        oldcrc = data.read(4)

        data.seek(index+4)
        o = data.tell()
        crcdata = data.read(chunksize-8)
        newcrc = long2raw(pngCRC32(crcdata), BIG_ENDIAN, 4)

        data.seek(index+chunksize-4)
        data.write(newcrc)

        index += chunksize

    data.seek(0,0)
    data = data.read()
    assert len(data) == len(origdata)

    # str -> array
    data = array('B', data)
    return data

