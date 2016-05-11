#!/usr/local/bin/python

"""
#  (C) COPYRIGHT SERGIO ALVAREZ
#  SECURITY RESEARCH & DEVELOPMENT, 2000-2004
#  Covered under GPL v 2.0
#
#  TITLE:       PACKET_SENDER.PY
#
#  VERSION:     1.00
#
#  AUTHOR:      Sergio 'shadown' Alvarez
#
#  DATE:        03 Feb 2004
"""

import sys
import timeoutsocket
from OpenSSL import SSL
from socket import *

timeoutsocket.setDefaultSocketTimeout(10)

class twister_skt:
	def __init__(self):
		self.ssl		= 0		# 0 = OFF || 1 = ON
		self.state	= 0		# 0 = disconnected || 1 = connected
		self.type	= 0		# 0 = TCP || 1 = UDP || 2 = RAW
		self.bsize	= 1024	# 1024 default || 70000 for sqlinjection
		self.wait	= 0

	def timeout(self, timeout = 10):
		timeoutsocket.setDefaultSocketTimeout(timeout)

	def sslsocket(self, ssl = 1):
		self.ssl		= ssl

	def inject(self):
		self.bsize	= 70000
		self.wait	= 1

	def proto(self, type = 0): # default TCP
		if type == 0:		# TCP
			return
		elif type == 1:	# UDP
			self.type = type
		elif type == 2:	# RAW
			self.type = type
		else:
			print "Unknown protocol"

	def connect (self, host, port):
		if self.state == 1:
			print "Already has an active connection"
		elif self.type == 0: # TCP
			if self.ssl == 1:
				ctx = SSL.Context (SSL.SSLv23_METHOD)
				s = SSL.Connection (ctx, socket(AF_INET, SOCK_STREAM))
				try:
					err = s.connect_ex ((host, port))
				except:
					print "Couldn't connect SSL socket"
					return
				if err == 0:
					self.skt		= s
					self.state	= 1
			else:
				s = socket (AF_INET, SOCK_STREAM)
				try:
					err = s.connect_ex ((host, port))
				except:
					print "Couldn't connect TCP socket"
					return
				if err == 0:
					self.skt		= s
					self.state	= 1
		elif self.type == 1: # UDP
				s = socket (AF_INET, SOCK_DGRAM)
				try:
					err = s.connect_ex ((host, port))
				except:
					print "Couldn't create UDP socket"
					return
				if err == 0:
					self.skt		= s
					self.state	= 1
		else:
			print "RAW sockets not implemented yet"
		if self.state == 1:
			return "OK"

	def send(self, pkg_send = ""):
		if self.state == 0:
			print "No connection available"
			return None
		else:
			# If something to send let's send it
			if pkg_send != "":
				if self.type == 0:
					try:
						err = self.skt.send (pkg_send)
					except:
						print "TCP socket unexpectedly closed when sending"
						self.close()
						return None
				elif self.type == 1:
					try:
						err = self.skt.send (pkg_send)
					except:
						print "UDP socket unexpectedly closed when sending"
						self.close()
						return None
				else:
					print "RAW not implemented yet"
					return None
				if err == 0:
					print "Connection lost"
					self.close()
					return None
			return "OK"

	# Let's receive
	def recv(self):
		if self.state == 0:
			print "No connection available"
			return None
		else:
			if self.ssl == 0:
				if self.type == 0:
					try:
						if self.wait:
							pkg_received = self.skt.recv (self.bsize, MSG_WAITALL)
						else:
							pkg_received = self.skt.recv (self.bsize)
					except:
						print "TCP socket unexpectedly closed when receiving"
						self.close()
						return None
				elif self.type == 1:
					try:
						if self.wait:
							pkg_received = self.skt.recvfrom (self.bsize, MSG_WAITALL)
						else:
							pkg_received = self.skt.recvfrom (self.bsize)
					except:
						print "UDP socket unexpectedly closed when receiving"
						self.close()
						return None
			else: # SSL
				try:
					pkg_received = self.skt.read(self.bsize)
				except:
					print "SSL socket unexpectedly closed when receiving"
					self.close()
					return None
			# Did we reveive some stuff ?
			if pkg_received == 0:
				print "Connection lost"
				self.close()
				return None
			# if so...let's return it
			return pkg_received

	def send_recv(self, pkg_send = ""):
		"""
		Function: send_recv(s, pkg_s)
		receives socket_descriptor and string to send
		returns answer from server
		"""
		if self.send(pkg_send) == None:
			return None
		res = self.recv()
		if res == None:
			return None
		return res

	# Let's interact ;)
	def interact(self):
		if self.state == 0:
			print "No connection available"
			return None
		else:
			from telnetlib import Telnet
			telnet = Telnet()
			telnet.sock = self.skt
			telnet.interact()
			return None

	def close(self):
		try:
			self.skt.close()
		except:
			pass
		self.state = 0

	def request (self, req, host, port, ssl = 0):
		self.ssl == ssl
		self.inject()
		skt = self.connect(host, port)
		if skt == None:
			return 0
		rcv = self.send_recv(req)
		self.close()
		if rcv != None:
			return rcv
		else:
			return 0
		
if __name__ == '__main__':
	if len(sys.argv) != 2:
		print "Usage: %s [host/ip]" % sys.argv[0]
		sys.exit(0)
	ports = [21, 22, 23, 25, 80, 110, 143, 220, 443] # default ports
	s = twister_skt()
	for port in ports:
		#print "Trying port %d" % port
		#s.proto(1)
		#s.inject()
		#s.sslsocket()
		if port == 443:
			s.sslsocket() # ssl on
		if s.connect(sys.argv[1], port) == None:
			continue
		if port == 80 or port == 443:
			res = s.send_recv('HEAD / HTTP/1.0\n\n')
		else:
			res = s.send_recv()
		if res != None:
			print "Port %d:" % port
			print res
			#s.interact()
		if port == 443:
			s.sslsocket(0) # ssl off
		s.close()
