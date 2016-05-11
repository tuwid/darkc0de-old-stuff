###############################################################################
## networks.py  -- see http://www.zeppoo.net                                 ##
##									     ##	
## The project zeppoo is (C) 2006 : contact@zeppoo.net			     ##
## This program is free software;            				     ##
## you can redistribute it and/or modify it under the terms of the GNU       ##
## General Public License as published by the Free Software Foundation;      ##
## Version 2. This guarantees your right to use, modify, and                 ##
## redistribute this software under certain conditions.                      ##
##      								     ##
## Source is provided to this software because we believe users have a       ##
## right to know exactly what a program is going to do before they run       ##
## it.                                                                       ##
##									     ##
## This program is distributed in the hope that it will be                   ##
## useful, but WITHOUT ANY WARRANTY; without even the implied                ##
## warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR                   ##
## PURPOSE. See the GNU General Public License for more details (            ##
## http://www.gnu.org/copyleft/gpl.html ).                                   ##
##                                                                           ##
###############################################################################

from memory import Memory
from struct import pack
from struct import unpack
import string
import os
import sys

class Networks :
	def __init__(self) :
		self.list_tcp = []
		self.list_udp = []

class GVNetworks :
	networks_mem = Networks()
	networks_proc = Networks()
	networks_netstat = Networks()

	networks_check = Networks()

	tranlateState = { '01' : 'ESTABLISHED', '02' : 'SYN_SENT', '03' : 'SYN_RECV', '04' : 'FIN_WAIT1', '05' : 'FIN_WAIT2', '06' : 'TIME_WAIT', '07' : 'CLOSED', '08' : 'CLOSE_WAIT', '09' : 'LAST_ACK', '0A' : 'LISTEN', '0B' : 'CLOSING', '0C' : 'UNKNOWN' }

	def __init__(self, mmemory, typeaccess=0) :
		if not isinstance(mmemory, Memory):
			raise TypeError("ERREUR")

		self.mmemory = mmemory
		self.mmemory.open("r", typeaccess)

	def __del__(self) :
		self.mmemory.close()

	def _getNetworksNetstatProto(self, proto) :
		if(proto == "tcp") :
			current_list = self.networks_netstat.list_tcp
			argproto = "-t"
		elif(proto == "udp") :
			current_list = self.networks_netstat.list_udp
			argproto = "-u"

		i, o = os.popen2("/bin/netstat -an " + argproto)
			
		j = o.readline()
		j = o.readline()
		j = o.readline()
		while(j != ""):
			liste = j.split()
			if(proto == "tcp") :
				current_list.append([liste[3], liste[4], liste[5]])
			elif(proto == "udp") :
				current_list.append([liste[3], liste[4], None])
			
			j = o.readline()
						
		o.close()
		i.close()
	
	def getNetworksNetstat(self) :
		self._getNetworksNetstatProto("tcp")
		self._getNetworksNetstatProto("udp")

	def _iphexatodec(self, iphexa) :
		ipdec=""

		for i in range(0, 8, 2) :
			ipdec = "%d" % string.atol(iphexa[i:i+2], 16) + "." + ipdec
		
		if(iphexa[9:] == "0000") :
			ipdec = ipdec[:-1] + ":" + "*"
		else :
			ipdec = ipdec[:-1] + ":" + "%d" % string.atol(iphexa[9:], 16)
		
		
		return ipdec
		
	def _getNetworksProcProto(self, proto) :
                if(proto == "tcp") :
			current_list = self.networks_proc.list_tcp
		elif(proto == "udp") :
			current_list = self.networks_proc.list_udp
		
		try :
			fichier = open("/proc/net/" + proto, "r")
		except IOError :
			print "No such file /proc/net/" + proto 
			sys.exit(-1)
		
		liste = fichier.readlines()
		fichier.close()
		
		liste.pop(0)

		for i in liste :
			l = string.split(i)
			if(proto == "tcp") :
				current_list.append([self._iphexatodec(l[1]), self._iphexatodec(l[2]), self.tranlateState[l[3]]])
			elif(proto == "udp") :
				current_list.append([self._iphexatodec(l[1]), self._iphexatodec(l[2]), None])
	def getNetworksProc(self) :
		self._getNetworksProcProto("tcp")
		self._getNetworksProcProto("udp")
	
	def _simpleViewNetworks(self, networks) :
		print "Proto\t Local Address\t\t Foreign Address\tState"
		for i in networks.list_tcp:
			print "TCP" + "\t %-16s\t " % i[0] + "%-16s\t" % i[1] + i[2]

		for i in networks.list_udp:
			print "UDP" + "\t %-16s\t " % i[0] + "%-16s\t" % i[1]
	
	def viewNetworks(self) :
		self.getNetworksProc() #MUST BE BY MEMORY
		self._simpleViewNetworks(self.networks_proc)
	
	def _checkNetworks(self, ref, cmp, check) :
		for i in ref.list_tcp :
			try :
				cmp.list_tcp.index(i)
			except ValueError :
				check.list_tcp.append(i)

		for i in ref.list_udp :
			try :
				cmp.list_udp.index(i)
			except ValueError :
				check.list_udp.append(i)

	def checkViewNetworks(self) :
		self.getNetworksNetstat()
		self.getNetworksProc()

		self._checkNetworks(self.networks_proc, self.networks_netstat, self.networks_check)

		if((self.networks_check.list_tcp != []) or (self.networks_check.list_udp != [])):
			print "LISTS OF CONNECTIONS HIDE"
			self._simpleViewNetworks(self.networks_check)
		else :
			print "NO CONNECTIONS HIDE"
			print "YOUR SYSTEM SEEMS BE SAFE"
