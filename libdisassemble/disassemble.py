#! /usr/bin/env python

# Immunity libdisassemble
#
# Most of the functions are ported from the great libdisassm since we
#  we are using their opcode map. 

# TODO:
#    - Fix the getSize(), doesn't work well with all the opcodes
#    - Enhance the metadata info with more information on opcode.
#      i.e. we need a way to know if an address is an immediate, a relative offset, etc
#    - Fix the jmp (SIB) opcode in at&t that it has different output that the others. 
#    - support all the PREFIX*

# NOTE: This is less than a week work, so it might be full of bugs (we love bugs!)
#
# Any question, comments, hate mail: dave@immunitysec.com


# 
#    This library is free software; you can redistribute it and/or
#    modify it under the terms of the GNU Lesser General Public
#    License as published by the Free Software Foundation; either
#    version 2.1 of the License, or (at your option) any later version.
#                                                                                
#    This library is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Lesser General Public License for more details.
#                                                                                
#    You should have received a copy of the GNU Lesser General Public
#    License along with this library; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

# This code largely copyright Immunity, Inc (2004), parts
# copyright mammon and used under the LGPL by permission

import opcode86, struct

table86=opcode86.tables86
OP_PERM_MASK =  0x0000007L  
OP_TYPE_MASK =  0x0000F00L  
OP_MOD_MASK  =  0x00FF000L  
OP_SEG_MASK  =  0x00F0000L  
OP_SIZE_MASK = 0x0F000000L  


class Mode:
	def __init__(self, type):
		self.type = type #type & 0x700
		#self.flag = type & 0x7
		self.flag  = type & OP_PERM_MASK
		self.size = 0
		
	# format "AT&T" or "INTEL"
	def printOpcode(self, format):
		return "Not available"

	def getType(self):
		return self.type

	def getSize(self):
		return self.size
	
	def getFlag(self):
		return self.flag

	def getSFlag(self):
		return ("R", "W", "X")[self.flag/2]
	
	def getOpSize(self):
		return (self.type & OP_SIZE_MASK)

	def getAddrMeth(self):
		return (self.type & opcode86.ADDRMETH_MASK)
	
class Register(Mode):
	def __init__(self, regndx, type=opcode86.OP_REG):
		Mode.__init__(self, type)
		(self.name, self.detail, self.size)=opcode86.regs[regndx]

	def printOpcode(self, format="INTEL"):
		if format == "INTEL":
			return self.name
		else:
			return "%%%s" % self.name

	def getName(self):
		return self.name
	
class Address(Mode):
	def __init__(self, data, size, type=opcode86.ADDEXP_DISP_OFFSET, signed=1):
		Mode.__init__(self, type)
		
		self.signed=signed
		self.size  = size
		if self.signed:
			fmt = ("b", "h", "l")[size/2]
		else:
			fmt = ("B", "H", "L")[size/2]
		self.value, = struct.unpack(fmt, data[:size])

		
	def printOpcode(self, format="INTEL", exp=0):
		if format == "INTEL":
			if self.signed:
				tmp=""
				if self.value < 0:
					return "-0x%x" % (self.value * -1)
				return "0x%x" % self.value
			else:
			#if self.size == 4 or not self.signed:
				return "0x%x" % self.value
			#else:
				
		else:
			pre=""
			if self.getAddrMeth() == opcode86.ADDRMETH_E and not exp:
				pre+="$"
			return "%s0x%0x" % (pre, self.value)
class Expression(Mode):
	def __init__(self, disp, base, type):
		Mode.__init__(self, type)		
		self.disp  = disp
		self.base  = base
		self.psize = 4

	def setPsize(self, size):
		self.psize= size

	def getPsize(self):
		return self.psize

	def getType(self):
		return EXPRESSION

	def printOpcode(self, format="INTEL"):
		tmp=""
		if format == "INTEL":
			if self.base:
				tmp += self.base.printOpcode(format)
			if self.disp:
				if self.disp.value:
					if self.disp.value > 0 and tmp:
						tmp+="+"
					tmp += self.disp.printOpcode(format, 1)
			pre=""
			optype=self.getOpSize()
		
			addr_meth=self.getAddrMeth()
			if addr_meth == opcode86.ADDRMETH_E:
				if optype  == opcode86.OPTYPE_b:
					pre="BYTE PTR"
				elif optype== opcode86.OPTYPE_w:
					pre="WORD PTR"
				else :
					pre="DWORD PTR"
			tmp="%s [%s]" % (pre, tmp)
		else:
			if self.base:
				tmp+="(%s)" % self.base.printOpcode(format)
			if self.disp:
				tmp= "%s%s" % (self.disp.printOpcode(format,1), tmp)				
			#tmp="Not available"
		return tmp
class SIB(Mode):
	def __init__(self, scale, base, index):
		self.scale = scale
		self.base  = base
		self.index = index
	def printOpcode(self, format="INTEL"):
		tmp=""
		if format == "INTEL":
			if self.base:
				tmp+="%s" % self.base.printOpcode(format)
			if self.scale > 1:
				tmp+= "*%d" % self.scale
			if self.index:
				if tmp:
					tmp+="+"
				tmp+="%s" % self.index.printOpcode(format)
		else:
			if self.base:
				tmp+="%s" % self.base.printOpcode(format)
			if self.index:
				if tmp:
					tmp+=","
				tmp+="%s" % self.index.printOpcode(format)
			if self.scale:
				tmp+=",%d" % self.scale

			return tmp
		return tmp 	
		
class Prefix:
	def __init__(self, ndx, ptr):
		self.ptr = ptr
		self.type = opcode86.prefix_table[ndx]
	
	def getType(self):
		return self.type

	def getName(self):
		if self.ptr[6]:
			return self.ptr[6]
		else:
			return ""
	
class Opcode:
	def __init__(self, data):
		self.size = 0
		self.data = data
		self.off  = 0
		self.source = ""
		self.dest   = ""
		self.prefix = []
		self.parse(table86[0], self.off)
	
	def getOpcodetype(self):
		return self.opcodetype
		
	def parse(self, table, off):
		self.addr_size = 4
		ndx = ord(self.data[off]) 
		#      byte  min          shift       mask
		ndx = ( (ndx- table[3]) >> table[1]) & table[2]
		ptr = table[0][ndx] # index from table

		if ptr[1] == opcode86.INSTR_PREFIX:
			# You can have more than one prefix (!?)
			self.prefix.append( Prefix(ndx, ptr) )
			self.parse(table, off+1) # parse next instruction
			return
		if ptr[0] != 0:
			# > 1 byte length opcode
			self.parse(table86[ptr[0]],  off+1)
			return 
		self.opcode     = ptr[6]
		self.opcodetype = ptr[1]
		self.cpu        = ptr[5]
		self.off        = off + 1 # This instruction
		if table[2] != 0xff:
			self.off-=1

		bytes=0
		#       src dst aux
		values=['', '', '' ]		
		#print self.off

		for a in range(2, 5):
			ret = (0, None)
			self.mode16 = 0
			tmp =ptr[a]
			addr_meth = tmp & opcode86.ADDRMETH_MASK;
			if addr_meth == opcode86.OP_REG:
				# what do i supposed to do?
				pass
			size = self.get_size(tmp)
			
			if size ==1:
				genreg = opcode86.REG_BYTE_OFFSET
			elif size == 2:
				genreg = opcode86.REG_WORD_OFFSET
			else:
				genreg= opcode86.REG_DWORD_OFFSET

			if addr_meth == opcode86.ADDRMETH_E:
				ret=self.get_modrm(self.data[self.off:], opcode86.MODRM_EA, \
						   genreg, self.addr_size, tmp)  
				
			elif addr_meth == opcode86.ADDRMETH_M:
				ret=self.get_modrm(self.data[self.off:], opcode86.MODRM_EA, \
						   genreg, self.addr_size, tmp)  

			elif addr_meth == opcode86.ADDRMETH_Q:
				ret=self.get_modrm(self.data[self.off:], opcode86.MODRM_EA, \
						   opcode86.REG_MMX_OFFSET, self.addr_size, tmp)  
				
			elif addr_meth == opcode86.ADDRMETH_R:
				ret=self.get_modrm(self.data[self.off:], opcode86.MODRM_EA, \
						   genreg, self.addr_size, tmp)  

			elif addr_meth == opcode86.ADDRMETH_W:
				ret=self.get_modrm(self.data[self.off:], opcode86.MODRM_EA, \
						   opcode86.REG_SIMD_OFFSET, self.addr_size, tmp)  

			elif addr_meth == opcode86.ADDRMETH_C:
				ret=self.get_modrm(self.data[self.off:], opcode86.MODRM_EA, \
						   opcode86.REG_CTRL_OFFSET, size, tmp)  

			elif addr_meth == opcode86.ADDRMETH_D:
				ret=self.get_modrm(data[self.off:], opcode86.MODRM_EA, \
						   opcode86.REG_DEBUG_OFFSET, size, tmp)  

			elif addr_meth == opcode86.ADDRMETH_G:
				ret=self.get_modrm(self.data[self.off:], opcode86.MODRM_reg, \
						   genreg, size, tmp)  

			elif addr_meth == opcode86.ADDRMETH_P:
				ret=self.get_modrm(data[self.off:], opcode86.MODRM_EA, \
						   opcode86.REG_MMX_OFFSET, size, tmp)  

			elif addr_meth == opcode86.ADDRMETH_S:
				ret=self.get_modrm(self.data[self.off:], opcode86.MODRM_EA, \
						   opcode86.REG_SEG_OFFSET, size, tmp)  

			elif addr_meth == opcode86.ADDRMETH_T:
				ret=self.get_modrm(self.data[self.off:], opcode86.MODRM_EA, \
						   opcode86.REG_TEST_OFFSET, size, tmp)  
			
			elif addr_meth == opcode86.ADDRMETH_V:
				ret=self.get_modrm(self.data[self.off:], opcode86.MODRM_EA, \
						   opcode86.REG_SIMD_OFFSET, size, tmp)  

			elif addr_meth == opcode86.ADDRMETH_A:
				ret= (self.addr_size, Address(self.data[self.off:], self.addr_size, tmp, signed=0))  

			elif addr_meth == opcode86.ADDRMETH_F:
				# eflags, so what?
				pass

			elif addr_meth == opcode86.ADDRMETH_I:
				if tmp & opcode86.OP_SIGNED:
					ret = (size, Address( self.data[self.off+bytes:], size, tmp))
				else:
					ret = (size, Address( self.data[self.off+bytes:], size,tmp,  signed=0))					

			elif addr_meth == opcode86.ADDRMETH_J:
				ret = (size, Address( self.data[self.off+bytes:], size, tmp, signed=1))

			elif addr_meth == opcode86.ADDRMETH_O:
				ret = (size, Address( self.data[self.off:], size, tmp, signed=0))
			
			elif addr_meth == opcode86.ADDRMETH_X:
				ret = (0, Register(6+opcode86.REG_DWORD_OFFSET, tmp))
				
			elif addr_meth == opcode86.ADDRMETH_Y:
				ret = (0, Register(7+opcode86.REG_DWORD_OFFSET, tmp))

			else:
				if tmp & opcode86.OP_REG:
					ret = (0, Register(ptr[5+a], tmp))
				else:
					ret= (0, None)
			if ret[1]: 
				if isinstance(ret[1], Expression):
					ret[1].setPsize(size)				
			values[a-2]=ret[1]
			bytes += ret[0]
			
		self.source = values[0]
		self.dest   = values[1]
		self.aux    = values[2]

		self.off += bytes

	def getSize(self):
		return self.off
	
	def get_size(self, flag):
		size=4
		for a in self.prefix:
			if a.getType() & opcode86.PREFIX_OP_SIZE:
				size = 2
			if a.getType() & opcode86.PREFIX_ADDR_SIZE:
				self.addr_size = 2
		flag= flag & opcode86.OPTYPE_MASK

		if flag == opcode86.OPTYPE_c:
			size = (1,2)[size==4]
		elif (flag == opcode86.OPTYPE_a) or (flag == opcode86.OPTYPE_v):
			size = (2,4)[size==4]			
		elif flag == opcode86.OPTYPE_p:
			size = (4,6)[size==4]			
		elif flag == opcode86.OPTYPE_b:
			size = 1
		elif flag & opcode86.OPTYPE_w:
			size = 2
		elif flag & opcode86.OPTYPE_d:
			size = 4		
		elif flag & opcode86.OPTYPE_s:
			size = 6		
		elif flag & opcode86.OPTYPE_q:
			size = 8		
		# - a lot more to add
		return size
	
	def get_reg(self, regtable, num):
		return regtable[num]	

	def get_sib(self, data, mod):
		count = 1
		sib     = ord(data[0])
		#print "SIB: %s" %  hex(ord(data[0]))
		
		scale    = (sib >> 6) & 0x3   #  XX
		index   = (sib & 56) >>3   #    XXX
		base   = sib & 0x7          #       XXX

		base2 = None
		index2= None
		#print base, index, scale
		# Especial case
		if base == 5 and not mod:
			base2   = Address(data[1:], 4)
			count += 4
		else:
			base2 = Register(base)

		index2=None
		# Yeah, i know, this is really ugly
		if index != 4: # ESP
			index2=Register( index)
		s= SIB( 1<<scale, base2, index2)
		return (count, s)

	def get_modrm(self, data, flags, reg_type, size, type_flag):
		modrm=  ord(data[0])
		count = 1
		mod  = (modrm >> 6) & 0x3   #  XX
		reg  = (modrm >> 3) & 0x7   #    XXX
		rm   = modrm & 0x7          #       XXX

		result = None
		disp   = None
		base   = None

		if flags == opcode86.MODRM_EA:
			if   mod == 3:  # 11
				result=Register(rm+reg_type, type_flag)
			elif mod == 0:  #  0
				if rm == 5:
					disp= Address(data[count:], self.addr_size, type_flag)
					count+= self.addr_size
				elif rm == 4:
					(tmpcount, base) =self.get_sib(data[count:], mod)
					count+=tmpcount
				else:
					base=Register(rm, type_flag)
			else:
				
				if rm ==4:
					disp_base = 2
					(tmpcount, base) =self.get_sib(data[count:], mod)
					count+=tmpcount
				else:
					disp_base = 1
					base=Register(rm, type_flag)
				#print ">BASE: %s" % base.printOpcode()
				if mod == 01:
					disp= Address(data[disp_base:], 1, type_flag)
					count+=1
				else:
					disp= Address(data[disp_base:], self.addr_size, type_flag)
					count+= self.addr_size
			if disp or base:
				result=Expression(disp, base, type_flag)
		else:
			result=Register(reg+reg_type, type_flag)
			count=0
			
		return (count, result)
	# FIX:
	#   
	def getOpcode(self, FORMAT):
		opcode=[]
		if not self.opcode:
			return [0]
		if FORMAT == "INTEL":
			opcode.append("%s" % self.opcode)
			#tmp="%-06s %s" % (self.opcode, " " * space)
			if self.source:
				opcode.append(self.source.printOpcode(FORMAT))
				#tmp+=" %s" % self.source.printOpcode(FORMAT)
			if self.dest:
				opcode.append(self.dest.printOpcode(FORMAT))
				#tmp+=", %s" % self.dest.printOpcode(FORMAT)
		else:
			mnemonic = self.opcode
			post=[]
			if self.source and self.dest:
				addr_meth = self.source.getAddrMeth()
				optype = self.source.getOpSize()
				mnemonic = self.opcode
				
				if addr_meth == opcode86.ADDRMETH_E and\
				  not (isinstance(p.source, Register) or\
				       isinstance(p.dest, Register)): 
					if optype  == opcode86.OPTYPE_b:
						mnemonic+="b"
					elif optype== opcode86.OPTYPE_w:
						mnemonic+=""
					else :
						mnemonic+="l"

				##first="%-06s %s" %  (mnemonic, " " * space)
				post= [self.dest.printOpcode(FORMAT),  self.source.printOpcode(FORMAT)]
				#post = "%s, %s" % (self.dest.printOpcode(FORMAT),  self.source.printOpcode(FORMAT))
			elif self.source:
				#second="%-06s %s" %  (mnemonic, " " * space)
				opt = self.getOpcodetype() 
				tmp=""
				if (opt== opcode86.INS_CALL or\
				    opt== opcode86.INS_BRANCH)\
				   and self.source.getAddrMeth() == opcode86.ADDRMETH_E:
					
					tmp = "*"
				post=[tmp + self.source.printOpcode(FORMAT)]
				#post += "%s" % self.source.printOpcode(FORMAT)				
			opcode = [mnemonic] + post
			
		return opcode
	
	def printOpcode(self, FORMAT, space=6):
		opcode=self.getOpcode(FORMAT)
		prefix=self.getPrefix()
		if opcode[0]==0:
			return "invalid"
		if len(opcode) ==2:	
			return "%-08s%s%s" % (prefix+opcode[0], " " * space, opcode[1])
		elif len(opcode) ==3:	
			return "%-08s%s%s,%s" % (prefix+ opcode[0], " " * space, opcode[1], opcode[2])
		else:
			return "%-08s" % (prefix+opcode[0])		
		return tmp
	def getPrefix(self):
		prefix=""
		for a in self.prefix:
			if a.getType() in [opcode86.PREFIX_LOCK, opcode86.PREFIX_REPNZ,\
					   opcode86.PREFIX_REP]:
				prefix+= a.getName() + " "
		return prefix
if __name__=="__main__":
	# To get this information, just
	import sys
	if len(sys.argv) != 4:
		print "usage: %s <file> <offset> <size>" % sys.argv[0]
		print "\t file:\t file to disassemble"
		print "\t offset:\t offset to beggining of code(hexa)"
		print "\t size:\t amount of bytes to dissasemble (hexa)\n"


		sys.exit(0)
	f=open(sys.argv[1])
	offset= int(sys.argv[2], 16)
	f.seek( offset )
	buf=f.read(int(sys.argv[3], 16) )
	off=0
	FORMAT="AT&T"
	print "Disassembling file %s at offset: 0x%x" % (sys.argv[1], offset)
        while 1:
                try:
                        p=Opcode(buf[off:])
                                                                                
                        print " %08X:   %s" % (off+offset, p.printOpcode(FORMAT))
                        off+=p.getSize()
		except:
			 break
