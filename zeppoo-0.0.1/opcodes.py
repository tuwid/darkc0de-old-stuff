###############################################################################
## opcodes.py  -- see http://www.zeppoo.net                                  ##
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
class Opcodes :
	def addr (self, mytab):
	        l = []
		for i in mytab :
	                l.append(str(hex(ord(i))))

		if(len(l) > 0) :
			l.reverse()
			var = l.pop(0)
			for i in l : 
				if(len(i) == 3) :
					if(i == "0x0") :
						i = i + "0"
		 			else :
						i = i[:2] + "0" + i[2]

				var = var + i[2:]
        
			#print "VAR %s" % var
   			addresse = string.atol(var, 16)
      		else :
			addresse = 0 

      		return (addresse)

	def reverseOpcodes(self, opcodes) :
		temp = ""
		i = 0
		
		for i in range(0, len(opcodes) , 2) :
			temp = opcodes[i:i+2] + temp

		temp = temp[:8]
		temp = temp.replace(' ', '0')
		return temp

	def find_opcodes(self, buffer, opcodes, length):
	        i = string.find(buffer, opcodes)
	        truc = buffer[i+len(opcodes):i+length+len(opcodes)]
	        return (truc)
