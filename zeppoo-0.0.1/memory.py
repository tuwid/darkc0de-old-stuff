###############################################################################
## memory.py  -- see http://www.zeppoo.net                                   ##
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

import ulibzeppoo
import string
from struct import unpack
from opcodes import Opcodes
from struct import pack
from struct import unpack


class Memory(object):
	op = Opcodes()

	def _getBase(self) :
		base = ulibzeppoo.idtr()
		return string.atol(base, 16)
		
	def _getSystemCall(self, base) :
		temp = self.read(base+8*0x80, 2)
		off1 = unpack("<H", temp)[0]
		temp = self.read(base+8*0x80+6, 2)
		off2 = unpack("<H", temp)[0]
		
		return (off2 << 16) | off1
	
	def _getSysCallTableFd(self) :
		base = self._getBase()
		system_call = self._getSystemCall(base)

		buffer = self.read(system_call, 255)
		temp = self.op.find_opcodes(buffer, "\xff\x14\x85", 4)
		return  unpack("<L", temp)[0] 	

	def _getSysCallTableMmap(self) :
		offset = self.dataFind("\xff\x14\x85")
		offset = 3221225472 + offset
		addr = unpack("<L", self.read(offset+3, 4))[0]
		#print '0x%x' % addr
		return addr
		
	def getSysCallTable(self) :
		if(self.typeaccess != 0):
			return self._getSysCallTableMmap()
		else:
			return self._getSysCallTableFd()	
	
	def dataFind(self, data) :
		raise NotImplementedError

	def dataSeek(self, pos, offset) :
		raise NotImplementedError
	
	# Based on p61_BONUS_BONUS by c0de @ UNF <c0de@uskf.com>
	def _find_proc_root(self) :
		for t in range(3221225472, 3238002688, 4096) :
			data = self.read(t, 4096)
			for i in range(0, 4096, 1) :
				try : 
					if(data[i] == '\x01' and data[i+2] == '\x00' and data[i+4] == '\x05' and data[i+12] == '\x6d'):
						if(data[i+20] == '\x00' and data[i+24] == '\x00'):
							return (t+i)
				except IndexError :
					i = 4096

	def _find_proc_root_operations(self, proc_root) :
		return unpack("<L", self.read(proc_root+32, 4))[0]

	def _find_proc_root_readdir(self, proc_root_operations) :
		return unpack("<L", self.read(proc_root_operations+24, 4))[0]

	def _find_proc_pid_readdir(self, proc_root_readdir) :
		data = self.read(proc_root_readdir, 256)
		offset =  data.find("\xe9")
		tmp = unpack("<L", self.read(proc_root_readdir + offset + 1, 4))[0]
		offset = offset + 5
		return (proc_root_readdir + tmp + offset + 5)
		
	def _find_get_tgid_list(self, proc_pid_readdir) :
		data = self.read(proc_pid_readdir, 256)
		offset =  data.find("\xe8")
		tmp = unpack("<L", self.read(proc_pid_readdir + offset + 1, 4))[0]

		offset = offset + 5
		addr = proc_pid_readdir + tmp + offset + 5

		if(addr > 4294967296):
			addr = addr - 4294967296

		return (addr)
	
	def _find_init_task(self) :
		proc_root = self._find_proc_root()
		#print "PROC_ROOT @ 0x%x" % proc_root
		
		proc_root_operations = self._find_proc_root_operations(proc_root)
		#print "PROC_ROOT_OPERATIONS @ 0x%x" % proc_root_operations
		
		proc_root_readdir = self._find_proc_root_readdir(proc_root_operations)
		#print "PROC_ROOT_READDIR @ 0x%x" % proc_root_readdir

		
		proc_pid_readdir = self._find_proc_pid_readdir(proc_root_readdir)
		#print "PROC_PID_READDIR @ 0x%x" % proc_pid_readdir
		
		get_tgid_list = self._find_get_tgid_list(proc_pid_readdir)
		#print "GET_TGID_LIST @ 0x%x" % get_tgid_list

		data = self.read(get_tgid_list, 256)
		offset =  data.find("\x81")
		
		init_task =  unpack("<L", self.read(get_tgid_list + offset + 2, 4))[0]
		return init_task


	
	def find_symbol(self, name) :
		if(self.typeaccess == 0):
			if(name == "init_task") :
				return self._find_init_task()
		else:
			self.dataSeek(0, 0)
			kstrtab_symbol = self.dataFind(name)
			#print kstrtab_symbol
			kstrtab_addr = 3221225472 + kstrtab_symbol
			#print "__kstrtab @ 0x%x" % kstrtab_addr
			kstrtab_ascii = pack("<L", kstrtab_addr)
			offset = self.dataFind(kstrtab_ascii)
			offset = 3221225472 + offset
			#print "OFFSET %d" % offset
			symbol_addr = unpack("<L", self.read(offset-4, 4))[0]
			#print 'symbol %s @ 0x%x' %(name, symbol_addr)
			return symbol_addr

			
	def open(self, mode, typeaccess=0):
		raise NotImplementedError
	
	def close(self):
		raise NotImplementedError
	
	def read(self, pos, len):
		raise NotImplementedError
		
	def write(self, pos, buf):
		raise NotImplementedError
		
	def dump(self, pos, len, type):
		i = 0
     		var = ""
     		print "Dump Memory @ 0x%x to @ 0x%x" %(pos, pos+len)
        	for i in range(0, len, 4) :
        		dump_memory = self.read(pos + i, 4) 
        		temp = '%8x' % unpack("<L", dump_memory)[0]
			if(type == 'h') :
				var = var + self.op.reverseOpcodes(temp)
        
			elif(type == 'v') :
				var = var + self.op.reverseOpcodes(temp) + '\t' + dump_memory + '\n'

        	print var			
	
