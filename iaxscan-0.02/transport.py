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

import socket

from select import select

class UDPTransceiver:
    def __init__(self):        
        self.send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rList = [self.send_sock]
        self.selectTimeout = .005

    def checkIncoming(self):    
        timeout = .005
        r, w, x = select(self.rList, [], [], self.selectTimeout)

        if r:
            data, addr = r[0].recvfrom(1024)
            return data, addr

        return None, None

    def sendScan(self, targetList, data, callback):
        cnt = 0            

        for target in targetList:
            self.send_sock.sendto(data, target)
            while True:
                data, addr = self.checkIncoming()
                if data != None:
                    callback(data, addr)
                else:
                    break

    def sendTo(self, data, target):
        self.send_sock.sendto(data, target)