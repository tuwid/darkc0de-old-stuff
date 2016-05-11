###############################################################################
## fingerprints.py  -- see http://www.zeppoo.net                             ##
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
import platform 
from time import strftime, gmtime
from syscalls import GVSyscalls

class Fingerprints:
	def __init__(self, memory) :
		self.mmemory = memory
		self.fichier = None
		self.ssyscalls = GVSyscalls(self.mmemory)	

	def doFingerprints(self, nomfichier) :
		try :
			fichier = open(nomfichier, "w")
		except IOError :
			print "No such file " + nomfichier 
			sys.exit(-1)
	
		print "++ Begin Generating Fingerprints in " + nomfichier
		fichier.write("# Generating Fingerprints for :\n# ")
		for i in platform.uname():
			fichier.write(i + " ")
		
		fichier.write('\n')
		
		temps = strftime('%c', gmtime())
		fichier.write("# " + temps + '\n')
		
		self.ssyscalls.doFingerprints(fichier)

		fichier.close()
		print "++ Keep this fingerprints in safe !"
		print "++ End Generating Fingerprints"
		
	def checkFingerprints(self, nomfichier) :
		try :
			fichier = open(nomfichier, "r")
		except IOError :
			print "No such file " + nomfichier
			sys.exit(-1)

		print "++ Begin Checking Fingerprints in " + nomfichier 

		self.ssyscalls.checkFingerprints(fichier)
		
		fichier.close()
		print "++ End Checking Fingerprints"
