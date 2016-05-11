import struct
from array import array

import PyD3DES

from AppKit import *

from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet import reactor

class NotEnoughDataException(Exception):
    pass


def tocard32(i):
    try:
        return struct.pack('!i', i)
    except struct.error, e:
        raise NotEnoughDataException(e)

def card32(i):
    if len(i) != 4:
        raise NotEnoughDataException(i)
    return array('i', i.tostring())[0]

def tocard16(i):
    try:
        return struct.pack('!h', i)
    except struct.error, e:
        raise NotEnoughDataException(e)

def card16(i):
    if len(i) != 2:
        raise NotEnoughDataException(i)
    return array('h', i.tostring())[0]

def tocard8(i):
    return chr(i)
    
def card8(i):
    return i

class PixelFormat(object):
    def __init__(self, **args):
        for k, v in args.items():
            setattr(self, k, v)
        
    def parse(klass, data):
        parts = list(data[:4])
        parts.append(card16(data[4:6]))
        parts.append(card16(data[6:8]))
        parts.append(card16(data[8:10]))
        parts += map(None, data[10:13])
        args = {}
        for attr, value in zip(('bpp', 'depth', 'bigendian', 'truecolor',
                                'red_max', 'green_max', 'blue_max',
                                'red_shift', 'green_shift',
                                'blue_shift'), parts):
            args[attr] = value
        args['size'] = args['bpp'] / 8
        return klass(**args)
    parse = classmethod(parse)
            
    def __str__(self):
        parts = [x for x in dir(self) if not x.startswith('_')]
        parts.sort()
        s = '\n'.join([('%12s: %s' % (x, getattr(self, x))) for x in parts])
        return s

    def pack(self):
        parts = [tocard8(self.bpp),
                 tocard8(self.depth),
                 tocard8(self.bigendian),
                 tocard8(self.truecolor),
                 tocard16(self.red_max),
                 tocard16(self.green_max),
                 tocard16(self.blue_max),
                 tocard8(self.red_shift),
                 tocard8(self.green_shift),
                 tocard8(self.blue_shift),
                 '\0' * 3]
        return ''.join(parts)

    def default(klass):
        return klass(bpp=32, depth=32, bigendian=0, truecolor=1, red_max=255, green_max=255, blue_max=255, red_shift=0, green_shift=8, blue_shift=16, size=4)
    default = classmethod(default)


class VNCClient(Protocol):
    RAW_ENCODING, COPYRECT_ENCODING, RRE_ENCODING, CORRE_ENCODING, HEXTILE_ENCODING = 0, 1, 2, 4, 5

    def __init__(self, passwd=''):
        self.read_buffer = array('B')

        self.state = 'ProtocolVersion'
        self.states = { 'ProtocolVersion': self.do_ProtocolVersion,
                        'Authentication': self.do_Auth,
                        'Initialization': self.do_Init,
                        'Connected': self.do_ConnectedHandler
                        }
        self.auth_types = [self.do_ConnectionFailed,
                            self.do_NoAuth,
                            self.do_VNCAuth,
                            ]
        self.vnc_auth_state = 0
        self.vnc_auth_states = [self.do_VNCAuth1,
                                self.do_VNCAuth2,
                                ]
        self.connected_msgs = {0: self.do_FramebufferUpdate,
                               2: self.do_Bell,
                               3: self.do_ServerCutText,
                               }

    def dataReceived(self, data):
        self.read_buffer.extend(array('B', data))
        self.states[self.state]()


    def setFrameBufferRect(self, x, y, w, h, data):
        destRect = ((x, y), (w, h))
        srcRect = ((0, 0), (w, h))
    
        self.frameBuffer.lockFocus()
        data.drawInRect_fromRect_operation_fraction_(destRect, srcRect, NSCompositeCopy, 1.0)
        self.frameBuffer.unlockFocus()
        
    def setFrameBufferRectToRawData(self, x, y, w, h, rawData):
        imgRep = NSBitmapImageRep.alloc().initWithBitmapDataPlanes_pixelsWide_pixelsHigh_bitsPerSample_samplesPerPixel_hasAlpha_isPlanar_colorSpaceName_bytesPerRow_bitsPerPixel_((rawData, None, None, None, None), w, h, 8, 4, True, False, NSCalibratedRGBColorSpace, 0, 4 * 8)
        imgRep.setAlpha_(False)
        img = NSImage.alloc().initWithSize_((w, h))
        img.setFlipped_(True)
        img.lockFocus()
        imgRep.drawInRect_(((0, 0), (w, h)))
        img.unlockFocus()
        self.setFrameBufferRect(x, y, w, h, img)
        
    def dumpFramebufferToFile(self):
        self.frameBuffer.TIFFRepresentationUsingCompression_factor_(NSTIFFCompressionLZW, 1.0).writeToFile_atomically_('VNC - %s.tiff' % (self.name, ), False)


    def do_ProtocolVersion(self):
        # Remove the servers version and return our own
        print('Protocol version recieved "%s"' % (''.join(self.read_buffer[:11].tostring()), ))
        self.read_buffer = self.read_buffer[12:]
        self.transport.write('RFB 003.003\n')
        self.state = 'Authentication'

    def do_ConnectionFailed(self):
        try:
            reason_length = card32(self.read_buffer[4:8])
            reason = self.read_buffer[8:8 + reason_length]
            self.read_buffer = self.read_buffer[8 + reason_length:]
            self.transport.loseConnection()
            print('Connection failed: %s' % (reason,))
            return 1
        except Exception, e:
            print repr(e)

    def do_Auth(self):
        t = self.read_buffer[:4]
        t = card32(t)
        print('Authentication type is %d (%r)' % (t, self.auth_types[t]))
        if self.auth_types[t]():
            pass
                

    def do_NoAuth(self):
        pass

    def do_VNCAuth(self):
        self.vnc_auth_states[self.vnc_auth_state]()

    def do_VNCAuth1(self):
        try:
            if len(self.read_buffer) < 20:
                raise IndexError
            challenge = self.read_buffer[4:20]
            self.read_buffer = self.read_buffer[20:]
            self.read_buffer.extend(array('B', '\x00\x00\x00\x02'))
            PyD3DES.setkey(self.factory.password)
            self.transport.write(PyD3DES.encrypt(challenge[:8]) + PyD3DES.encrypt(challenge[8:]))
            self.vnc_auth_state += 1
        except Exception, e:
            print repr(e), e
            return

    def do_VNCAuth2(self):
        try:
            if len(self.read_buffer) < 8:
                raise IndexError
            response = card32(self.read_buffer[4:8])
            if response == 0:
                print('Authentication succeeded')
                self.state = 'Initialization'
                self.read_buffer = self.read_buffer[8:]
                # Send the ClientInit message that consists
                # of a card32 that is 1 if the session is shared
                try:
                    self.transport.write(chr(self.shared))
                except:
                    self.transport.write(chr(0))
            elif response == 1:
                print('Invalid password')
                self.transport.loseConnection()
            elif response == 2:
                print('Too many connections!')
                self.transport.loseConnection()
        except Exception, e:
            print(e)
            
            
    def do_Init(self):
        """
        Handle a ServerInitialisation message.
        """
        if len(self.read_buffer) >= 24:
            print('ServerInitialisation buffer length: %d' % (len(self.read_buffer), ))
            self.fbsize = (card16(self.read_buffer[:2]), card16(self.read_buffer[2:4]))
            self.pixel_format = PixelFormat.parse(self.read_buffer[4:20])
            name_length = card32(self.read_buffer[20:24])
        else:
            return
        
        if len(self.read_buffer) < 24 + name_length:
            return
        self.name = ''.join(self.read_buffer[24:24 + name_length].tostring())
        print('Connected to %s' % (self.name, ))
        print('Servers pixel format: \n%s' % (self.pixel_format, ))
        
        self.frameBuffer = NSImage.alloc().initWithSize_(self.fbsize)
        self.frameBuffer.setFlipped_(True)

        self.alreadyProcessedRectangles = (0, 4)


        self.read_buffer = self.read_buffer[24 + name_length:]
        self.state = 'Connected'
        self.send_SetPixelFormat(PixelFormat.default())
        self.send_SetEncoding((self.CORRE_ENCODING, ))
        self.send_FramebufferUpdateRequest((0, 0, self.fbsize[0], self.fbsize[1]), 0)

        
    def do_ConnectedHandler(self):
        """ """
        p = NSAutoreleasePool.alloc().init()
        self.connected_msgs[self.read_buffer[0]]()
        del p

    def do_FramebufferUpdate(self):
        buf = self.read_buffer

        try:
            messageType = buf[0]
            numberOfRectangles = card16(buf[2:4])
            
            firstRectangle, currentRectangleStart = self.alreadyProcessedRectangles

            for currentRectangle in range(firstRectangle, numberOfRectangles):
                currentRectangleLength = 0
                x, y, width, height = card16(buf[currentRectangleStart    :currentRectangleStart + 2]), \
                                      card16(buf[currentRectangleStart + 2:currentRectangleStart + 4]), \
                                      card16(buf[currentRectangleStart + 4:currentRectangleStart + 6]), \
                                      card16(buf[currentRectangleStart + 6:currentRectangleStart + 8])
                encodingType = card32(buf[currentRectangleStart + 8:currentRectangleStart + 12])
                currentRectangleLength += 12
                
                currentEncodingStart = currentRectangleStart + 12
                currentEncodingLength = 0
                if encodingType == self.RAW_ENCODING:
                    currentEncodingLength = VNCClient._Raw(self, currentEncodingStart, x, y, width, height, NotEnoughDataException)
                elif encodingType == self.CORRE_ENCODING:
                    currentEncodingLength = VNCClient._CoRRE(self, currentEncodingStart, x, y, width, height, NotEnoughDataException)

                else:
                    print '\t\tUnknown encoding!', encodingType

                currentRectangleLength += currentEncodingLength
                currentRectangleStart += currentRectangleLength
                
                self.alreadyProcessedRectangles = (currentRectangle + 1, currentRectangleStart)
            
            self.read_buffer = self.read_buffer[currentRectangleStart:]
            self.alreadyProcessedRectangles = (0, 4)
#            self.dumpFramebufferToFile()
            self.send_FramebufferUpdateRequest((0, 0, self.fbsize[0], self.fbsize[1]), 0)
#            self.transport.loseConnection()
        except NotEnoughDataException, e:
            pass
            
    def _Raw(self, currentEncodingStart, x, y, width, height, NotEnoughDataException):
        rawDataLength = width * height * self.pixel_format.size
        rawData = self.read_buffer[currentEncodingStart:currentEncodingStart + rawDataLength]
        if len(rawData) < rawDataLength:
            raise NotEnoughDataException
        
        self.setFrameBufferRectToRawData(x, y, width, height, rawData)
        return rawDataLength

            
    def _CoRRE(self, currentEncodingStart, x, y, width, height, NotEnoughDataException):
        buf = self.read_buffer
        if len(buf) < currentEncodingStart + 8:
            raise NotEnoughDataException
    
        numberOfSubRectangles = card32(buf[currentEncodingStart:currentEncodingStart + 4])
        r, g, b, a = buf[currentEncodingStart + 4:currentEncodingStart + 8]
        
        self.frameBuffer.lockFocus()
        NSColor.colorWithCalibratedRed_green_blue_alpha_(r / 255.0, g / 255.0, b / 255.0, 1.0).set()
        NSRectFill(((x, y), (width, height)))
    
        currentSubRectangleStart = currentEncodingStart + 8
        
        if len(buf) < currentSubRectangleStart + (8 * numberOfSubRectangles):
            raise NotEnoughDataException
    
        subRectangleRects = []
        subRectangleColors = []
        if numberOfSubRectangles:
            for currentSubRectangle in range(numberOfSubRectangles):
                r, g, b, a, srX, srY, srWidth, srHeight = buf[currentSubRectangleStart:currentSubRectangleStart + 8]
    
                subRectangleRects.append(((x + srX, y + srY), (srWidth, srHeight)))
                subRectangleColors.append((r / 255.0, g / 255.0, b / 255.0, 1.0))
                currentSubRectangleStart += 8
    
            subRectangleColors = map(NSColor.colorWithCalibratedRed_green_blue_alpha_, *zip(*subRectangleColors))        
            NSRectFillListWithColors(subRectangleRects, subRectangleColors)
    
        self.frameBuffer.unlockFocus()
            
        currentEncodingLength = 8 * (numberOfSubRectangles + 1)
        return currentEncodingLength
    
    try:
        from _CoRRE import _CoRRE
    except ImportError:
        pass

    def do_Bell(self):
        self.read_buffer = self.read_buffer[1:]

    def do_ServerCutText(self):
        length = card32(self.read_buffer[4:8])
        text = self.read_buffer[8:8 + length]
        print text
        self.read_buffer = self.read_buffer[8 + length:]


    
    def send_SetPixelFormat(self, pixelFormat):
        self.pixel_format = pixelFormat
        msg = tocard8(0)
        msg += '\0' * 3
        msg += pixelFormat.pack()
        self.transport.write(msg)

    def send_SetEncoding(self, encodings):
        msg = tocard8(2)
        msg = msg + '\0'
        msg = msg + tocard16(len(encodings))

        encs = map(tocard32, encodings)
        msg = msg + ''.join(encs)
        self.transport.write(msg)

    def send_FramebufferUpdateRequest(self, pos, incremental):
        msg = tocard8(3)
        msg = msg + tocard8(incremental)
        msg = msg + ''.join(map(tocard16, pos))
        self.transport.write(msg)

    def send_KeyEvent(self, down, key):
        msg = tocard8(4)
        msg = msg + tocard8(down) + '\0'
        msg = msg + tocard32(key)
        self.transport.write(msg)

    def send_PointerEvent(self, pos, buttons):
        msg = tocard8(5)
        msg = msg + tocard8(buttons)
        msg = msg + ''.join(map(tocard16, pos))
        self.transport.write(msg)

    def send_ClientCutText(self, text):
        msg = tocard8(6)
        msg = msg + ' ' + card32(len(text))
        msg = msg + text
        self.transport.write(msg)

class VNCClientFactory(ClientFactory):
    protocol = VNCClient
    def __init__(self, password):
        self.password = password

    def startedConnecting(self, connector):
        print 'startedConnecting'

    def clientConnectionFailed(self, connector, reason):
        print 'Connection failed. Reason:', reason

    def clientConnectionLost(self, connector, reason):
        print 'Connection lost. Reason:', reason
        if reactor.running:
            reactor.stop()

import hotshot, hotshot.stats
def main():
    import sys
    if len(sys.argv) < 4:
        print 'Usage: %s hostname port password' % (sys.argv[0], )
        return

    NSApplicationLoad()
    reactor.connectTCP(sys.argv[1], int(sys.argv[2]), VNCClientFactory(sys.argv[3]))
    reactor.run()

import profile, pstats
if __name__ == '__main__':
    main()
    