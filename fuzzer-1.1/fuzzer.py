#!/usr/bin/env python

"""
#  (C) COPYRIGHT SERGIO ALVAREZ 
#	SECURITY RESEARCH & DEVELOPMENT, 2000-2004
#	Covered under GPL v 2.0
#
#  TITLE:       FUZZER.PY
#
#  VERSION:     1.10
#
#  AUTHOR:      Sergio 'shadown' Alvarez
#
#  DATE:        25 SEP 2004
"""

"""
NOTE: best view with 'tabstop=3'
"""

import sys
from fuzzgenerator import fuzzgenerator
from packet_sender import twister_skt
import time		# sleep
import struct	# for packing
import getopt	# for parsing opts

class fuzzer:
	# import protocols avialable
	import protocols

	def __init__(self):
		# host and port
		self.host	= 'localhost'
		self.port	= 21
		self.sleep	= 0	# seconds to wait between requests
		# 'self.lastsent' to hold if a bug has been found
		self.lastsent	= None
		# create fuzzdata
		fuzzshit			= fuzzgenerator()
		# add stop requesting tags
		fuzzshit.ints.append('lastrequest')
		fuzzshit.injects.append('lastrequest')
		# assotiate to local variables
		self.strings	= fuzzshit.getstrings()
		self.integers	= fuzzshit.getints()
		self.injects	= fuzzshit.getinjects()
		self.strings	+= self.injects # agrego los injects a strings ;)
		# bag of 'mustuse' command sequense
		self.mustuse = []
		# variables globales de la clase
		self.tryproto	= 'ftp' # protocol to fuzz, default is 'ftp'
		self.fromsize	= 128
		self.tosize		= 10240
		self.increment	= 128

	def sethost(self, host):
		self.host = host

	def setport(self, port):
		self.port = port

	# this shit makes the diference when finding bugs
	def setsleep(self, sleep):
		self.sleep = sleep

	def ultrafasttest(self):
		self.strings	= ['A'*(1024+4*3), 'B'*(4096+4*3), 'A'*(10240+4*3), 'B'*(65535+4*3), '%s'*128]
		self.integers	= ['65536', '0xfffffff', '268435455', '1', '0', '-1', '-65536', '-268435455', 'lastrequest']
		self.injects	= ['\'', ';', ';--', 'lastrequest']
		self.strings	+= self.injects # agrego los injects a strings ;)

	def settryproto(self, proto = 'ftp'):
		if self.protocols.protoname.keys().count(proto):
			self.tryproto = proto
		else:
			print 'Unknown protocol ['+str(proto)+'] using [ftp]'
			self.tryproto = 'ftp'
	
	def getprotocols(self):
		return self.protocols.protoname.keys()

	def fuzz(self):
		print "<*>here fuzzing begins [%s]<*>" % str(self.tryproto)
		if self.protocols.protoname[self.tryproto]:
			print '\t[+] Keys del protocolo: '+str(self.protocols.protoname[self.tryproto].keys())
			print '\t[+] Protocol family: '+self.protocols.protoname[self.tryproto]['proto']
			print '\t[+] Recv Banner: '+('OFF', 'ON')[self.protocols.protoname[self.tryproto]['banner']]
			# creo el socket y asigno el tipo
			skt = twister_skt()
			if self.protocols.protoname[self.tryproto]['proto'] == 'udp':
				skt.proto(1)
			elif self.protocols.protoname[self.tryproto]['proto'] == 'ssl':
				skt.sslsocket(1)
			# aca empiesa la joda ;)
			if self.protocols.protoname[self.tryproto]['comm']:
				print '\t[+] Commands'
				for cmd in self.protocols.protoname[self.tryproto]['comm']:
					#print "\t\t[-] Command: %s"	% str(cmd['command'])
					#print "\t\t[-] Datatype: %s"	% str(cmd['datatype'])
					#print "\t\t[-] Default: %s"	% str(cmd['default'])
					#print "\t\t[-] Mustuse: %s"	% ('OFF', 'ON')[cmd['mustuse']]
					if cmd['datatype'] == 'string':
						for string in self.strings:
							# nos conectamos
							if skt.connect(self.host, self.port) == None:
								if self.lastsent:
									return self.lastsent
								else:
									return None
							# si es necesario recibimos el banner
							if self.protocols.protoname[self.tryproto]['banner']:
								res = skt.send_recv()
								print '\t\t<< '+str(res)
								del(res)
							# fuzzeamos
							if string == 'lastrequest':
								if cmd['mustuse']:
									if cmd['default']:
										self.mustuse.append({'command': str(cmd['command'])+str(cmd['default'])+cmd['endw'], 'recv': cmd['recv']})
									else:
										self.mustuse.append({'command': str(cmd['command'])+cmd['endw'], 'recv': cmd['recv']})
									skt.close()
									time.sleep(self.sleep)
									continue
								else:
									skt.close()
									time.sleep(self.sleep)
									continue
							if self.mustuse:
								for must in self.mustuse:
									print '\t\t>> '+must['command']
									if must['recv']:
										res = skt.send_recv(must['command'])
										print '\t\t<< '+str(res)
									else:
										skt.send(must['command'])
							print '\t\t>> '+str(cmd['command'])+string
							# we backup last request just in case a bug found
							self.lastsent = str(cmd['command'])+string
							if cmd['recv']:
								res = skt.send_recv(str(cmd['command'])+string+cmd['endw'])
								if res:
									print '\t\t<< '+str(res)
								else:
									print '\t\t<**> It was suppose to recv something, but recv nothing CHECKIT! <**>'
							else:
								skt.send(str(cmd['command'])+string+cmd['endw'])
							print '\t\t-----------------------------------------------'
							# desconectamos
							skt.close()
							time.sleep(self.sleep)
					elif cmd['datatype'] == 'inject':
						for inject in self.injects:
							# nos conectamos
							if skt.connect(self.host, self.port) == None:
								if self.lastsent:
									return self.lastsent
								else:
									return None
							# si es necesario recibimos el banner
							if self.protocols.protoname[self.tryproto]['banner']:
								res = skt.send_recv()
								print '\t\t<< '+str(res)
								del(res)
							# fuzzeamos
							if inject == 'lastrequest':
								if cmd['mustuse']:
									if cmd['default']:
										self.mustuse.append({'command': str(cmd['command'])+str(cmd['default'])+cmd['endw'], 'recv': cmd['recv']})
									else:
										self.mustuse.append({'command': str(cmd['command'])+cmd['endw'], 'recv': cmd['recv']})
									skt.close()
									time.sleep(self.sleep)
									continue
								else:
									skt.close()
									time.sleep(self.sleep)
									continue
							if self.mustuse:
								for must in self.mustuse:
									print '\t\t>> '+must['command']
									if must['recv']:
										res = skt.send_recv(must['command'])
										print '\t\t<< '+str(res)
									else:
										skt.send(must['command'])
							print '\t\t>> '+str(cmd['command'])+inject
							# we backup last request just in case a bug found
							self.lastsent = str(cmd['command'])+inject
							if cmd['recv']:
								res = skt.send_recv(str(cmd['command'])+inject+cmd['endw'])
								if res:
									print '\t\t<< '+str(res)
								else:
									print '\t\t<**> It was suppose to recv something, but recv nothing CHECKIT! <**>'
							else:
								skt.send(str(cmd['command'])+inject+cmd['endw'])
							print '\t\t-----------------------------------------------'
							# desconectamos
							skt.close()
							time.sleep(self.sleep)
					elif cmd['datatype'] == 'int':
						for integer in self.integers:
							# nos conectamos
							if skt.connect(self.host, self.port) == None:
								if self.lastsent:
									return self.lastsent
								else:
									return None
							# si es necesario recibimos el banner
							if self.protocols.protoname[self.tryproto]['banner']:
								res = skt.send_recv()
								print '\t\t<< '+str(res)
								del(res)
							# fuzzeamos
							if integer == 'lastrequest':
								if cmd['mustuse']:
									if cmd['default']:
										self.mustuse.append({'command': str(cmd['command'])+str(cmd['default'])+cmd['endw'], 'recv': cmd['recv']})
									else:
										self.mustuse.append({'command': str(cmd['command'])+cmd['endw'], 'recv': cmd['recv']})
									skt.close()
									time.sleep(self.sleep)
									continue
								else:
									skt.close()
									time.sleep(self.sleep)
									continue
							if self.mustuse:
								for must in self.mustuse:
									print '\t\t>> '+must['command']
									if must['recv']:
										res = skt.send_recv(must['command'])
										print '\t\t<< '+str(res)
									else:
										skt.send(must['command'])
							print '\t\t>> '+str(cmd['command'])+integer
							# we backup last request just in case a bug found
							self.lastsent = str(cmd['command'])+integer
							if cmd['recv']:
								res = skt.send_recv(str(cmd['command'])+integer+cmd['endw'])
								if res:
									print '\t\t<< '+str(res)
								else:
									print '\t\t<**> It was suppose to recv something, but recv nothing CHECKIT! <**>'
							else:
								skt.send(str(cmd['command'])+integer+cmd['endw'])
							print '\t\t-----------------------------------------------'
							# desconectamos
							skt.close()
							time.sleep(self.sleep)
					else:
						# nos conectamos
						if skt.connect(self.host, self.port) == None:
							if self.lastsent:
								return self.lastsent
							else:
								return None
						# si es necesario recibimos el banner
						if self.protocols.protoname[self.tryproto]['banner']:
							res = skt.send_recv()
							print '\t\t<< '+str(res)
							del(res)
						# fuzzeamos
						if self.mustuse:
							for must in self.mustuse:
								print '\t\t>> '+must['command']
								if must['recv']:
									res = skt.send_recv(must['command'])
									print '\t\t<< '+str(res)
								else:
									skt.send(must['command'])
						print '\t\t>> '+str(cmd['command'])
						# we backup last request just in case a bug found
						self.lastsent = str(cmd['command'])
						if cmd['recv']:
							res = skt.send_recv(str(cmd['command'])+cmd['endw'])
							if res:
								print '\t\t<< '+str(res)
							else:
								print '\t\t<**> It was suppose to recv something, but recv nothing CHECKIT! <**>'
						else:
							skt.send(str(cmd['command'])+cmd['endw'])
						if cmd['mustuse']:
							self.mustuse.append({'command': str(cmd['command'])+cmd['endw'], 'recv': cmd['recv']})
						print '\t\t-----------------------------------------------'
						# desconectamos
						skt.close()
						time.sleep(self.sleep)
			return None
		else:
			print "El protocolo [%s] aun no esta disponible" % str(self.tryproto)
			return None

def usage():
	# enumerate protocols avialable
	tfuz = fuzzer()
	protos = ''
	for proto in tfuz.getprotocols():
		protos += proto+', '
	del tfuz
	# show usage message
	print "#####################################"
	print "#     Net-Twister Fuzzer Module     #"
	print "# Coded by Sergio 'shadown' Alvarez #"
	print "#    Contact: shadown@gmail.com     #"
	print "#####################################"
	print "Usage: %s -h <host> -p <port> -t <protocol> -s <sleep in secs> -f [use fastmode]" % sys.argv[0]
	print "protocols available: %s" % protos[:-2]
	print "Options:"
	print "\t-h : target host"
	print "\t-p : target port"
	print "\t-t : target protocol"
	print "\t-s : time to wait between attempts, default 0 (OPTIONAL)"
	print "\t-f : turns ON fast mode, few but most common bugs, default OFF (OPTIONAL)"
	sys.exit(1)

if __name__ == '__main__':
	# variables to check the 'must specified' values
	target	= 0
	port		= 0
	protocol	= 0
	# parse option flags
	try:
		options = getopt.getopt(sys.argv[1:], 'h:p:t:s:f')[0]
	except getopt.GetoptError, err:
		print err
		usage()
	# asign option values
	tfuz = fuzzer()
	for option, value in options:
		if option == '-h':
			tfuz.sethost(value)
			target += 1
		if option == '-p':
			tfuz.setport(int(value))
			port += 1
		if option == '-t':
			tfuz.settryproto(value)
			protocol += 1
		if option == '-s':
			tfuz.setsleep(int(value))	# play around with this, is the key to found bugs. (2 is the best i've found)
		if option == '-f':
			tfuz.ultrafasttest()			# muy pocos tests, pero los mas comunes, para correr todos comentar esta linea
	# check if minimum args were specified
	if not target	\
		or not port	\
		or not protocol:
		usage()
	# launch fuzzing tests
	res = tfuz.fuzz()
	if res:
		print '<**> Bug found!!! ;)) <**>'
		print '-> Sending: '+res
	else:
		print '<**> No bugs found =( <**>'
