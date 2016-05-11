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

import time
import struct
import sys

from binascii import hexlify, a2b_hex, b2a_hex

from transport import UDPTransceiver
from iax import IAXProto
from logging import Logger
         
class UserScanner:
    def __init__(self, verbosity=5):
        self.udp_ts = UDPTransceiver()
        self.iax_proto = IAXProto()
        self.log = Logger(verbosity).log

        self.liveUsers = []
        
    def responseReceived(self, data, addr):
        self.log('[d] Response received from %s' % str(addr), 15)
        type = self.iax_proto.getMessageType(data)
        if type == IAXProto.REGAUTH:
            user = self.iax_proto.extractAuthUser(data)
            if user != None:
                try:
                    self.liveUsers.index(user)
                except ValueError:
                    self.liveUsers.append(user)
                    self.log('[+] Found user %s' % user)
            else:
                self.log('[!] Could not extract username from REGAUTH response', 10)
                fName = '.'.join([str(time.time()), 'log']) 
                fOut = open(fName, 'wb')
                fOut.write(data)
                fOut.close()
                self.log('[!] Response logged to %s' % fName, 10)

        self.udp_ts.sendTo(self.iax_proto.genAck(data), addr)

    def makeRange(self, rangeTuple, usernameSize, padValue):
        userRange = []
        for username in range(rangeTuple[0], rangeTuple[1]+1):
            username = str(username)
            user = ''.join([str(padValue)*(usernameSize-len(username)), username])
            userRange.append(user)
                    
        return userRange
    
    def scan(self, targetTuple, userRange=(0, 999), usernameSize=3, padValue=0, probeDelay=.01):
        userRange = self.makeRange(userRange, usernameSize, padValue)
        sent_count = 0
        for user in userRange: 
            req = self.iax_proto.buildREGREQ(self.iax_proto.genSourceCallFull(), user)
            self.udp_ts.sendScan([(targetTuple)], req, self.responseReceived)
            
            sent_count += 1
            if sent_count % 100 == 0:
                self.log('[i] Checked %d usernames' % sent_count)
            else:
                self.log('[d] Checked %d usernames' % sent_count, 10)
                
            # Without this Asterisk has trouble keeping up and probes get lost
            time.sleep(probeDelay)

        self.log('[i] %d user accounts were scanned' % sent_count)
        self.log('[i] Done sending probes. Waiting %d seconds for more responses' % 5)
        eTime = time.time() + 5
        while time.time() <= eTime:
            data, addr = self.udp_ts.checkIncoming()
            if data != None:        
                self.responseReceived(data, addr)
                
class HostScanner:
    def __init__(self, verbosity=5):
        self.udp_ts = UDPTransceiver()
        self.iax_proto = IAXProto()
        self.log = Logger(verbosity).log
        
        self.liveHosts = []
        
    def responseReceived(self, data, addr):
        try:
            self.liveHosts.index(addr[0])
        except ValueError:
            self.liveHosts.append(addr[0])
            self.log('[+] Found host %s' % addr[0])
            self.udp_ts.sendTo(self.iax_proto.genAck(data), addr)

    def scan(self, targetList, port=4569, userName='101', probeDelay=0):
        sent_count = 0
        for target in targetList:
            targetTuple = (target, port) 
            self.log('[d] Checking %s' % str(targetTuple), 10)
            req = self.iax_proto.buildREGREQ(self.iax_proto.genSourceCallFull(), userName)
            self.udp_ts.sendScan([targetTuple], req, self.responseReceived)
            
            sent_count += 1
            if sent_count % 100 == 0:
                self.log('[i] Checked %d hosts' % sent_count)
            else:
                self.log('[d] Checked %d hosts' % sent_count, 10)   
            
            time.sleep(probeDelay)
            
        self.log('[i] %d hosts were scanned' % sent_count)
        self.log('[i] Done sending probes. Waiting %d seconds for more responses' % 5)
        eTime = time.time() + 5
        while time.time() <= eTime:
            data, addr = self.udp_ts.checkIncoming()
            if data != None:        
                self.responseReceived(data, addr)
                