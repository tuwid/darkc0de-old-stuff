#!/usr/bin/env python

###############################################################################
## zeppoo.py  -- see http://www.zeppoo.net                                   ##
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

import sys, os, string
from optparse import OptionParser

from syscalls import GVSyscalls
from tasks import GVTasks
from networks import GVNetworks
from fingerprints import Fingerprints
from mem import Mem
from kmem import Kmem

option_1 = { 'name' : ('-d', '--device'), 'help' : 'choose the device(/dev/kmem or /dev/mem)', 'nargs' : 1 }
option_2 = { 'name' : ('-v', '--view'), 'help' : 'tasks, syscalls, networks', 'nargs' : 1 }
option_3 = { 'name' : ('-c', '--check'), 'help' : 'tasks, networks', 'nargs' : 1 }
option_4 = { 'name' : ('-f', '--fingerprints'), 'help' : 'check, create', 'nargs' : 2 }
option_5 = { 'name' : ('-m', '--usemmap'), 'help' : 'using mmap to search symbols(more quick)', 'action' : 'count' }
option_6 = { 'name' : ('-b', '--bump'), 'help' : 'Dump memory', 'nargs' : 3 }

options = [option_1, option_2, option_3, option_4, option_5, option_6]

def usage() :
	print "For help use -h"
	sys.exit(-1)

def main(options, arguments):
	#print 'options %s' % options
	#print 'arguments %s' % arguments
	if(options.device != None) :
		if(options.device == '/dev/mem') :
			mmemory = Mem()
		elif(options.device == '/dev/kmem') :
			mmemory = Kmem()
		else:
			usage()
	else :
		mmemory = Kmem()

	if(options.usemmap == None):
		options.usemmap = 0

	if(options.view != None):
		if(options.view == 'tasks'):
			ttasks = GVTasks(mmemory, options.usemmap)
			ttasks.viewTasks()
		elif(options.view == 'syscalls'):
			mysyscalls = GVSyscalls(mmemory, options.usemmap)
			mysyscalls.viewSyscalls()
		elif(options.view == 'networks'):
			nnetworks = GVNetworks(mmemory, options.usemmap)
			nnetworks.viewNetworks()
			
	elif(options.check != None):
		if(options.check == 'tasks'):
			ttasks = GVTasks(mmemory, options.usemmap)
			ttasks.checkViewTasks()
		elif(options.check == 'networks'):
			nnetworks = GVNetworks(mmemory, options.usemmap)
			nnetworks.checkViewNetworks()
			
	elif(options.fingerprints != None):
		ffingerprints = Fingerprints(mmemory)
		if(options.fingerprints[1] == 'create'):
			ffingerprints.doFingerprints(options.fingerprints[0])
		elif(options.fingerprints[1] == 'check'):
			ffingerprints.checkFingerprints(options.fingerprints[0])
			
	elif(options.bump != None):
		mmemory.open("r", options.usemmap)
		mmemory.dump(string.atol(options.bump[0], 16), int(options.bump[1]), options.bump[2])
		mmemory.close()
	
	else:
		usage()
		
if __name__ == "__main__":

	if(os.getuid() != 0) :
		print "You must be root !!"
		sys.exit(-1)

	parser = OptionParser()
	for option in options:
		param = option['name']
		del option['name']
		parser.add_option(*param, **option)
	
	options, arguments = parser.parse_args()
	sys.argv[:] = arguments
	main(options, arguments)

