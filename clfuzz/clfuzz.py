#!/usr/bin/env python
##
## clfuzz.py v0.2 -- Command line arguments fuzzer
##                   Audit your setuid binaries!!!
##
##                   http://warl0ck.metaeye.org/clfuzz.tar.gz
##
## Copyright (C) 2005-2006  Pranay Kanwar <warl0ck@metaeye.org>
##
## This program is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License version 2 as
## published by the Free Software Foundation; version 2.
##
## This program is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## A copy of the GNU GPL is available as /usr/doc/copyright/GPL on Debian
## systems, or on the World Wide Web at http://www.gnu.org/copyleft/gpl.html
## You can also obtain it by writing to the Free Software Foundation, Inc.,
## 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA
##
## Usage: clfuzz.py program arg1 arg2 ... arg10 ...
##
## In args i.e arg1,arg2 etc STR is replaced with A's,
## FMT with fromat strings,NUM with number
##  
## example :  $clfuzz.py ping -c NUM STR
## 
##
## CHANGELOG
##
## v0.1 (10/10/2005) - First release
## v0.2 (20/10/2005) - Cleaned up a bit
##
## TODO
## 
## Add comman line options to customize fuzzing.
##
import os 
import sys
import time
import signal

#original arguments
cl_o=""

#buffer overflow string
bo_str="A"

#format string
fmt_str="%n"

#number
num_str="9"

#Main fuzz loop ranges
range_lower=1
range_upper=900

#step sizes, keep them > 1
step_size_bo=1 #bo string step size
step_size_fmt=5 #format string step size
step_size_num=3 #number string step size

print "clfuzz v0.2 - Command line arguments fuzzer"
print "Copyright (C) 2005-2006 Pranay Kanwar <warl0ck@metaeye.org>\n"

if len(os.sys.argv) < 2:
	sys.stdout.write("Usage: %s <program> <args...>\n" % (sys.argv[0]))
	sys.stdout.write("       in arguments write STR for strings, FMT\n")
	sys.stdout.write("       for format string and NUM for number.\n") 
	sys.exit(-1)

#build the command line
for x in os.sys.argv:
	cl_o=cl_o+x+" "
	
#chuck out our script name
cl_o=cl_o.replace(os.sys.argv[0],"")
#the command that will be executed
cl=""

bo_final=""
fmt_final=""
num_final=""

sleep_time=0

try:
	sys.stdout.write("[+] Fuzzing %s.\n" % (cl_o))
	for i in range(range_lower,range_upper):
		bo_final=bo_str*(i*step_size_bo)
		fmt_final=fmt_str*(i*step_size_fmt)
		num_final=num_str*(i*step_size_num)
		#sys.stdout.write(">[ BO = %d ] [ FMT = %d ] [ NUM = %d ].i\n" % (len(bo_final),len(fmt_final),len(num_final)))
		sys.stdout.flush()
		#replace STR with our buffer overlow string
		cl=cl_o.replace("STR",bo_final)
		#replace FMT with fmt_str 
		cl=cl.replace("FMT",fmt_final)
		#replace NUM with num_str
		cl=cl.replace("NUM",num_final)
		#execute and enjoy
		retval=os.system(cl) # this cobbles up return value still finding out why ? + " &> " + os.devnull) 
		if os.WTERMSIG(retval)==signal.SIGSEGV:
			sys.stdout.write("[+] Process crashed, Last Call [ BO = %d ] [ FMT = %d ] [ NUM = %d ].\n" % (len(bo_final),len(fmt_final),len(num_final)))
			sys.exit(0)
		#pause for sleep_time seconds for execution
		time.sleep(sleep_time)
except KeyboardInterrupt:
	print "[-] CTRL+C Detected aborting..."
	print "[-] Last call : [ BO =",len(bo_final),"] [ FMT =",len(fmt_final),"] [ NUM =",len(num_final),"]."
	sys.exit(0)
