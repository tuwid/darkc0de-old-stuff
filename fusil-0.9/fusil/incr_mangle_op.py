from random import randint, choice
from fusil.mangle_op import SPECIAL_VALUES
from array import array
from fusil.tools import minmax

MAX_INCR = 32

def createBitOffset(agent, datalen):
    min_offset = 0
    if agent.min_offset is not None:
        min_offset = max(agent.min_offset*8, min_offset)
    max_offset = datalen*8 - 1
    if agent.max_offset is not None:
        max_offset = min(agent.max_offset*8 + 7, max_offset)
    return randint(min_offset, max_offset)

def createByteOffset(agent, datalen):
    min_offset = 0
    if agent.min_offset is not None:
        min_offset = max(agent.min_offset, min_offset)
    max_offset = datalen - 1
    if agent.max_offset is not None:
        max_offset = min(agent.max_offset, max_offset)
    return randint(min_offset, max_offset)

class Operation:
    def __init__(self, offset, size):
        self.offset = offset
        self.size = size

    def __call__(self, data):
        raise NotImplementedError()

    def __str__(self):
        raise NotImplementedError()

class InverseBit(Operation):
    def __init__(self, agent, datalen):
        offset = createBitOffset(agent, datalen)
        Operation.__init__(self, offset, 1)

    def __call__(self, data):
        mask = 1 << (self.offset & 7)
        offset = self.offset >> 3
        if data[offset] & mask:
            data[offset] &= (~mask & 0xFF)
        else:
            data[offset] |= mask

    def __str__(self):
        return "InverseBit(offset=%s.%s)" % (self.offset // 8, self.offset % 8)

class ReplaceByte(Operation):
    def __init__(self, agent, datalen):
        offset = createByteOffset(agent, datalen-1)
        byte = randint(0, 255)
        Operation.__init__(self, offset*8, 8)
        self.byte = byte

    def __call__(self, data):
        data[self.offset // 8] = self.byte

    def __str__(self):
        return "ReplaceByte(byte=0x%02x, offset=%s)" % (self.byte, self.offset//8)

class SpecialValue(Operation):
    def __init__(self, agent, datalen):
        self.bytes = array("B", choice(SPECIAL_VALUES))
        offset = createByteOffset(agent, datalen-len(self.bytes))
        Operation.__init__(self, offset*8, len(self.bytes)*8)

    def __call__(self, data):
        offset = self.offset // 8
        data[offset:offset+len(self.bytes)] = self.bytes

    def __str__(self):
        bytes = ' '.join( '0x%02x' % byte for byte in self.bytes )
        return "SpecialValue(bytes=%r, offset=%s)" % (bytes, self.offset//8)

class Increment(Operation):
    def __init__(self, agent, datalen):
        self.incr = randint(1, MAX_INCR)
        if randint(0, 1) == 1:
            self.incr = -self.incr
        offset = createByteOffset(agent, datalen-1)
        Operation.__init__(self, offset*8, 8)

    def __call__(self, data):
        offset = self.offset // 8
        data[offset] = minmax(0, data[offset] + self.incr, 255)

    def __str__(self):
        return "Increment(incr=%+u, offset=%s)" % (self.incr, self.offset//8)

OPERATIONS = (InverseBit, ReplaceByte, SpecialValue, Increment)

