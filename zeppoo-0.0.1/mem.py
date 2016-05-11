###############################################################################
## mem.py  -- see http://www.zeppoo.net                                      ##
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

import string
import mmap
import sys
from struct import pack
from struct import unpack
from memory import Memory

class Mem(Memory) :
	__fd = 0
	__data = 0

		
	def open(self, mode, typeaccess=0, mmapmode = mmap.MAP_PRIVATE) :
		self.typeaccess = typeaccess
		try :
			self.__fd = open("/dev/mem", mode)
		except IOError :
			print "Mem::open IOErreur"
			sys.exit(-1)
		
		if(self.typeaccess != 0):
			try :
				self.__data = mmap.mmap(self.__fd.fileno(), 100 * 1024 * 1024, mmapmode)
				#print self.__data
			except TypeError :
				print "Mem::open TypeError"
				sys.exit(-1)
			
	def close(self) :
		self.__fd.close()
		if(self.typeaccess != 0):
			self.__data.close()
		
	def read(self, pos, len, type=1) :
		if(type == 0):
			realtype = type
		else:
			realtype = self.typeaccess
		try :
			if(realtype == 0) :
				self.__fd.seek(pos - 3221225472, 0)
				return self.__fd.read(len)
			else :
				self.__data.seek(pos - 3221225472, 0)
				return self.__data.read(len) 
				
		except ValueError :
			return ""

		return 0

	def write(self, pos, buf, type=1) :
		if(type == 0):
			realtype = type
		else:
			realtype = self.typeaccess
			
		if(realtype == 0) :
			self.__fd.seek(pos - 3221225472, 0)
			self.__fd.write(buf)
		else :
			self.__data.seek(pos - 3221225472, 0)
			self.__data.write(buf)
	
	def dataFind(self, data) :
		return self.__data.find(data);

	def dataSeek(self, pos, offset) :
		self.__data.seek(pos, offset);
