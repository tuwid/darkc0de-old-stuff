"""
class to extract win32 jmp's from .dll's.
not as sexy as it sounds.

handy for local exploits, not really all that useful
for remote except for finding uniform win2k/xp addresses.
- !nd|at|felinemenace.org!
"""  

import os

# for extracting and using jmp's from windows dll's
class jmpreg:

	# use esp (d4) as default
	def __init__(self,reg="esp"):
		# might need more than this, ebx for sure but hey!
		# it's upto you!
		self.registers = {"eax":"c0","esp":"d4"}
		self.reg = self.registers[reg]
		self.addrs = {}
		# my MingW path
		self.objdump = "C:\\MinGW\\bin\\objdump.exe"
		self.found = 0
		self.file = "jmpreg.txt"

	# set the objdump.exe path		
	def set_objdump(self,bin):
		print "objdump is %s" % bin
		self.objdump = bin
		return 1

	# set the reg you want to find the jmp's too
	def set_reg(self,reg):
		print "reg to look for is %s" % reg
		self.reg = self.registers[reg]
		return 1
	
	# uses objdump dump to find the addresses		
	def find_jmpreg(self,dir="c:\windows\system32"):
		k = os.listdir("c:\windows\system32")
		for z in k:
			if z.endswith(".dll"):
				data = []
				cmd = "%s -D C:\windows\system32\%s" % (self.objdump,z)
				fh = os.popen(cmd,"r")
				data = fh.read(100000).split("\n")
				fh.close()
				for r in data:
					y = "eb\x20%s" % self.reg
					if r.find("jmp") != -1 and r.find(y) != -1:
						(addy,null) = r.split(":")
						temp = "0x%s" % addy
						print temp
						self.addrs[z] = int(temp,0)
						self.found = 1
		if self.found != 1:
			print "found no jmp [reg]!"
			return 0
		return 1

	# pre defined database of jmp's
	def read_jmpaddy(self,file="jmpreg.txt"):
		fh = open(file,"r")
		data = fh.read(100000).split("\n")
		fh.close()
		for x in data:
			if self.found == 0:
				(dll,addy) = x.split(":")
				a = int(addy,0)
				self.addrs[dll] = a
		self.found = 1
		return 1				
	
	# returns the jmp of a given DLL
	# good for local exploits
	def use_jmpreg(self,dll="kernel32.dll"):
		if self.found != 0:
			for h in self.addrs.keys():
				if h == dll:
					return self.addrs[h]
			print "could not find jmpesp for requested DLL"
			return ""
		else:
			print "use find_jmpreg or read_jmpreg first"
			return 0
		return 1
	
	# write the recovered jmps to a file given that find_jmpreg
	# has already been run
	def write_jmpreg(self,file="jmp<GOOSE>"):
		if self.found == 1:
			file = file.replace("<GOOSE>",self.reg)
			self.file = file
			fh = open(self.file,"w")
			for x in self.addrs.keys():
				fh.write("%s:0x%8X\n" % (x,self.addrs[x]))
			fh.close()
		else:
			print "use find_jmpreg or read_jmpreg first!"
			return 0
		return 1

	# clear if you want to find different jmp addy's	
	def clear(self):
		self.reg = ""
		self.addrs = {}
		self.objdump = ""
		self.found = 0

# main!
if __name__ == '__main__':
	g = jmpreg()
	g.find_jmpreg()
	g.write_jmpreg()
