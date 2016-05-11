###############################################################################
## syscalls.py  -- see http://www.zeppoo.net                                 ##
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
from opcodes import Opcodes
from struct import pack
from struct import unpack
import string
import re
import sys

class Syscalls :
	def __init__(self) :
		self.map_syscalls = {}
	
class GVSyscalls :
	op = Opcodes()
	syscalls_mem = Syscalls()
	syscalls_fingerprints = Syscalls()
	
	lists_syscalls = []

	def __init__(self, mmemory, typeaccess=0) :
		if not isinstance(mmemory, Memory):
			raise TypeError("ERREUR")

		self.mmemory = mmemory
		self.mmemory.open("r", typeaccess)

		try :
			fichier = open("/usr/include/asm/unistd.h", "r")
		except IOError :
			print "No such file /usr/include/asm/unistd.h"
			sys.exit(-1)
			
		liste = fichier.readlines()
		fichier.close()
		count = 0
		for i in liste :
			if(re.match("#define __NR_", i)) :
				l = string.split(i)
				if(l[2][0].isdigit()) :
					count = string.atoi(l[2], 10)
					self.lists_syscalls.append([count, l[1][5:]])
				else :
					count = count + 1
					self.lists_syscalls.append([count, l[1][5:]])

	def __del__(self) :
		self.mmemory.close()
				
	def getSyscalls(self) :
		sys_call_table = self.mmemory.getSysCallTable()
		#print 'SYS_CALL_TABLE 0x%x' % sys_call_table
		for i in self.lists_syscalls :
			temp = self.mmemory.read(sys_call_table + 4*i[0], 4)
			self.syscalls_mem.map_syscalls[i[0]] = [unpack("<L", temp)[0], ()]

	def getOpcodes(self) :
		for i in self.lists_syscalls :
			temp = "%8x" % unpack("<L", self.mmemory.read(self.syscalls_mem.map_syscalls[i[0]][0], 4))[0]
			opcodes = self.op.reverseOpcodes(temp)
			
			temp2 =  "%8x" % unpack("<L", self.mmemory.read(self.syscalls_mem.map_syscalls[i[0]][0]+4, 4))[0] 
			opcodes = opcodes + " " + self.op.reverseOpcodes(temp2)
			self.syscalls_mem.map_syscalls[i[0]][1] = opcodes
			

	def _simpleViewSyscalls(self, syscalls) :
		print 'POS\t MEM\t\t NAME\t\t\t\t OPCODES'
		for i in self.lists_syscalls :
			print '%d\t 0x%x\t %-15s\t\t %s' % (i[0], syscalls.map_syscalls[i[0]][0], i[1], syscalls.map_syscalls[i[0]][1])

	def viewSyscalls(self) :
		self.getSyscalls()
		self.getOpcodes()
		self._simpleViewSyscalls(self.syscalls_mem)

	def doFingerprints(self, fd) :
		self.getSyscalls()
		self.getOpcodes()
	
		print "++ Generating Syscalls Fingerprints"
		fd.write("#\n# BEGIN SYSCALLS FINGERPRINTS\n")
		
		for i in self.lists_syscalls :
			data = "%d %x %s %s\n" % (i[0], self.syscalls_mem.map_syscalls[i[0]][0], i[1], self.syscalls_mem.map_syscalls[i[0]][1])
			fd.write(data)
		
		fd.write("#\n# END SYSCALLS FINGERPRINTS\n")
		
	def checkFingerprints(self, fd) :
		syscalls_hijack = []
		end = 0
		self.getSyscalls()
		self.getOpcodes()
			
		i = fd.readline()
		liste = i.split()
		while(liste != [] and end == 0):
			if(liste[0] != '#') :
				self.syscalls_fingerprints.map_syscalls[int(liste[0])] = [string.atol(liste[1], 16), liste[3] + " " + liste[4]]
			else :
				if(len(liste) > 1) :
					if(liste[1] == "END"):
						end = -1

			i = fd.readline()
			liste = i.split()

		print "++ Checking Syscalls Fingerprints !!!"
		for i in self.lists_syscalls:
			if((self.syscalls_fingerprints.map_syscalls[i[0]][0] != self.syscalls_mem.map_syscalls[i[0]][0]) or (self.syscalls_fingerprints.map_syscalls[i[0]][1] != self.syscalls_mem.map_syscalls[i[0]][1])):
				syscalls_hijack.append([i[0], i[1]])
	
		if(syscalls_hijack != []):
			print "\t** LISTS OF SYSCALLS HIJACK !!"
			for i in syscalls_hijack:
				print "\t\t** %d\t %-15s" %(i[0], i[1])

			print "\n\t** PLEASE REINSTALL YOUR SYSTEM NOW !!!"

		else:
			print "\t** NO SYSCALLS HIJACK"
