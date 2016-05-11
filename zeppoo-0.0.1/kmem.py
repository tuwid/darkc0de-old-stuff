###############################################################################
## kmem.py  -- see http://www.zeppoo.net                                     ##
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

import sys
from memory import Memory

class Kmem(Memory) :
	__fd = 0

	def open(self, mode, typeaccess=0) :
		self.typeaccess = typeaccess
		try :
			self.__fd = open("/dev/kmem", mode)
		except IOError :
			print "Kmem::open IOError"
			sys.exit(-1)

		if(self.typeaccess != 0):
			print "mmap not implement on /dev/kmem"
			sys.exit(-1)
			
	def close(self) :
		self.__fd.close()

	def read(self, pos, len, type=1) :
		try :
			self.__fd.seek(pos, 0)
			temp = self.__fd.read(len)
		except IOError :
			print "Kmem::read IOError"
			sys.exit(-1)

		return temp

	def write(self, pos, buf) :
		try :
			self.__fd.seek(pos, 0)
			self.__fd.write(buf)
		except IOError :
			print "Kmem::write IOError"
			sys.exit(-1)
