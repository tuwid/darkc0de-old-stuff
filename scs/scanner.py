#!/usr/bin/python

 ###############################################################################
 #                    Simple Conficker Scanner
 #                      (single host scanner)
 #
 #
 # Copyright (C) 2009  Felix Leder & Tillmann Werner
 # 
 # This program is free software; you can redistribute it and/or
 # modify it under the terms of the GNU General Public License
 # as published by the Free Software Foundation; either version 3
 # of the License, or (at your option) any later version.
 # 
 # This program is distributed in the hope that it will be useful,
 # but WITHOUT ANY WARRANTY; without even the implied warranty of
 # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 # GNU General Public License for more details.
 # 
 # You should have received a copy of the GNU General Public License
 # along with this program; if not, write to the Free Software
 # Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
 # 
 # 
 #             contact {leder,werner}@cs.uni-bonn.de
 #
 #
 #  thanks to Dan Kaminsky for tricking us into writing this tool
 #
 ###############################################################################




import struct
import sys

from struct import pack
try:
	from impacket import smb
	from impacket import uuid
	from impacket.dcerpc import dcerpc
	from impacket.dcerpc import transport
except:
	print "[ERROR] Impacket package not found"
	sys.exit(1)

class Request:
	def __init__(self, server, path):
		self.server = server
		self.path = path

		self.stub  = '\x01\x00\x00\x00'
		self.stub += pack('III', len(self.server)/2, 0, len(self.server)/2)
		self.stub += self.server
		self.stub += pack('III', len(self.path)/2, 0, len(self.path)/2)
		self.stub += self.path
		self.stub += '\x02\x00\x00\x00\x02\x00\x00\x00'
		self.stub += '\x00\x00\x00\x00\x02\x00\x00\x00'
		self.stub += '\x5c\x00\x00\x00\x01\x00\x00\x00'
		self.stub += '\x01\x00\x00\x00'

	def run(self):
		self.dce.call(0x1f, self.stub)


class Scan(Request):
	def __init__(self):
		server = 'a' * 1 + '\0\0\0'
		path = '\x5c\0\x2e\0\x2e\0\x5c\0\0\0\0\0'
		Request.__init__(self, server, path)



def test_infection(ip):
	retval = 0

	# INIT
	try:
		t = transport.DCERPCTransportFactory('ncacn_np:%s[\\pipe\\browser]' % ip)
		t.set_dport(445)
		t.connect()
	except:
		print 'No resp.: %s:445/tcp.' % ip
		return 0


	# NetpwPathCanonicalize
	try:
		dce = t.DCERPC_class(t)
		dce.bind(uuid.uuidtup_to_bin(('4b324fc8-1670-01d3-1278-5a47bf6ee188', '3.0')))

		scanner = Scan()
		scanner.dce = dce
		scanner.run()

		response = dce.recv()
	except:
		print 'Error running NetPathCanonicalize'
		return 0
	

	if (len(response)>=16):		
		result = struct.unpack('IIII', response[:16])

                if result[1]==0x5c450000 and result[3]==0x00000057:
                        print '[WARNING] %s seems to be infected by Conficker!' % ip
                        retval = 1
                elif result[1] != 0 and result[3] != 123:
                        print "Unknown dcerpc return value 0x%08x" % result[3]
                elif result[1] != 0 and result[1] != 0x5c450000:
                        print "Unknown error code: 0x%08x" % result[1]

			
	if retval == 0:
		print '%s seems to be clean.' % (ip)

	dce.disconnect()

	return retval


def print_creds():
	print """
----------------------------------
   Simple Conficker Scanner
----------------------------------
scans selected network ranges for
conficker infections
----------------------------------
Felix Leder, Tillmann Werner 2009
{leder, werner}@cs.uni-bonn.de
----------------------------------
"""




if __name__ == '__main__':
	print_creds()

	if len(sys.argv) != 2:
		print 'Usage: %s <host>' % sys.argv[0]
		sys.exit(0)

	test_infection(sys.argv[1])
