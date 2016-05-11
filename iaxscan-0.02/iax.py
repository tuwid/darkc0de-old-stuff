'''
The contents of this file are subject to the Mozilla Public License
Version 1.1 (the "License"); you may not use this file except in
compliance with the License. You may obtain a copy of the License at
http://www.mozilla.org/MPL/

Software distributed under the License is distributed on an "AS IS"
basis, WITHOUT WARRANTY OF ANY KIND, either express or implied. See the
License for the specific language governing rights and limitations
under the License.

The Original Code is iaxscan, v0.02, 9th October 2008.

The Initial Developer of the Original Code is nnp, http://www.unprotectedhex.com
'''

import random
import struct

from binascii import hexlify, a2b_hex, b2a_hex

class IAXProto:
    REGREG = '\x0d' 
    REGAUTH = '\x0e'
    
    def buildREGREQ(self, src_call, username):
        REGREQ = ''.join([src_call,
                          '\x00\x00', # destination call
                          '\x00\x00\x00\x03', # timestamp
                          '\x00', # outbound seq. number
                          '\x00', # inbound seq. number
                          '\x06', # type
                          '\x0d' # type subclass
                          '\x06',
                          a2b_hex('0' + hex(len(username))[2:]), username, '\x13\x02\x01\x2c'])
        return REGREQ

    def buildACK(self, src_call, dst_call):
        ACK = ''.join([src_call, dst_call, '\x00\x00\x00\x09\x01\x01\x06\x04'])
        return ACK

    def genSourceCallFull(self):
        '''
        This function returns a valid value for a source call in a full packet.
        This means the high bit is set.
        '''
        return a2b_hex(hex(0x8000 + random.randint(0, 0x8000))[2:])

    def extractCallInfo(response):
        rsrc_call_id = response[:2] 

        rdst_call_id = int(hexlify(response[2:4]), 16)
        # The src call value we sent would have had the high bit set to indicate
        # a full packet but in the response this may not be set. Set it here to allow
        # a comparison to our local value
        if not (rdst_call_id & 0x8000):
            rdst_call_id = rdst_call_id + 0x8000
            
        type_subclass = response[11]

        return rsrc_call_id, rdst_call_id, type_subclass
    
    def genAck(self, data):
        src_h, src_l = struct.unpack('BB', data[:2])
        dst_h, dst_l = struct.unpack('BB', data[2:4])

        if src_h & 0x80:
            src_h -= 0x80
        if not dst_h & 0x80:
            dst_h += 0x80

        # swap the source and destination
        return self.buildACK(struct.pack('BB', dst_h, dst_l), struct.pack('BB', src_h, src_l))

    def getMessageType(self, data):
        if data[11] == IAXProto.REGAUTH:
            return IAXProto.REGAUTH
        elif data[11] == IAXProto.REGREG:
            return IAXProto.REGREG
        
        return 0

    def extractAuthUser(self, data):
        cur_pos = 12
        while  cur_pos < len(data) and data[cur_pos] != '\x06':
            cur_pos += 1 # cur_pos now points to the length
            cur_len = struct.unpack('B', data[cur_pos])[0]
            cur_pos += cur_len + 1 # cur_pos now points to the next block
            
        if cur_pos < len(data):
            cur_pos += 1 # cur_pos now points to the length of the username
            cur_len = struct.unpack('B', data[cur_pos])[0]
            cur_pos +=1 # cur_post now points to the username
            username = struct.unpack('c'*cur_len, ''.join(data[cur_pos:cur_pos+cur_len]))

            return ''.join(username)
        
        return None