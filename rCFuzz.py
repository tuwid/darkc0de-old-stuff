##################################################################################
#
# rCfuzz.py v0.1 (c) 2008
# dB [at] rawsecurity.org
#
# Command line arguments fuzzer used for finding local vulnerabilities 
# in setuid/setgid binaries.  
#
# Usuage: rawCmdFuzz.py "program -a NUM -b SYM" [-s=5] [-p=0.1] [-m=900] [-i=50]
#
# Fuzz Data Types
# RAN - Generates a random string with all characters except special 
#       UNIX characters.
# SYM - Uses only random symbols.
# NUM - Generates a random number.
# FRM - Uses format string %n or %s.
# STR - Generates a random string using alphanumeric characters.
#
# Optional params
# -s Random seed
# -p Pause in seconds
# -m Max length of fuzz strings
# -i Increment value
#
##################################################################################

import signal
import os
import string
import time
import sys
import random
import commands

fuzzTypes = ["RAN","SYM","NUM","FRM","STR"]
symbols = ["!","$","%","*","+",",","-",".","/",
		   ":","?","@","^","_"]
formats = ["%s","%x","%n"]

INDEX = 0
STR_INDEX = 1
PARAM = 2
COUNT = 3

def getOneChar():
	ascii = 65
	if random.randint(0,1) == 1:
		ascii = random.randint(65,90)
	else:
		ascii = random.randint(97,122)
	return chr(ascii)

def getOneSymbol():
	global symbols
	return symbols[random.randint(0,len(symbols)-1)]
		   
def getRandomString(length):
	str_list = []
	ascii = 65
	for i in range(0,length):
		str_list.append(getOneChar())
	return ''.join(str_list)
	
def getRandomNumber(length):
	num_list = []
	for i in range(0,length):
		num_list.append(str(random.randint(0,9)))
	return ''.join(num_list)

def getRandomFormat(length):
	frmt_list = []
	for i in range(0,length):
		frmt_list.append(formats[random.randint(0,len(formats)-1)])
	return ''.join(frmt_list)

def getRandomSymbol(length):
	sym_list = []
	for i in range(0,length):
		sym_list.append(getOneSymbol())
	return ''.join(sym_list)
	
def getRandomRandom(length):
	randStr = ""
	randChar = ""
	for i in range(0,length):
		if random.randint(0,1) == 1:
			randChar = getOneChar()
		else:
			randChar = getOneSymbol()
		randStr += randChar
	return randStr
	
def doneFuzzing(params,maxLength):
	for i in range(0,len(params)):
		if params[i][STR_INDEX] != -1 and params[i][COUNT] < maxLength:
			return False
	return True
	
def printInfo(lastCmd,params):
	print "Last call: " + lastCmd
	for i in range(0,len(params)):
		index = str(params[i][INDEX])
		param = str(params[i][PARAM])
		count = str(params[i][COUNT])
		print "Index: " + index + " Param: " + param + " Num: " + count
	print ""

print ""
print "   rCfuzz v0.1 [ Command line fuzzer ]"
print "   dB [at] rawsecurity.org"
print ""

seed = 1
pause = 0.0
maxLength = 600
increment = 25

if len(sys.argv) < 2:
	print 'Usuage: rawCmdFuzz.py "program arg1 arg2 ..." [-s=5] [-p=0.1]\n'
	sys.exit(-1)
	
if len(sys.argv) > 2:
	for i in range(2,len(sys.argv)):
		if sys.argv[i].startswith("-s="):
			seed = int(sys.argv[i][3:])
		elif sys.argv[i].startswith("-p="):
			pause = float(sys.argv[i][3:])
		elif sys.argv[i].startswith("-m="):
			maxLength = int(sys.argv[i][3:])
		elif sys.argv[i].startswith("-i="):
			increment = int(sys.argv[i][3:])
			
random.seed(seed)

# Extract target process
cmdPieces = sys.argv[1].split(" ")
target = cmdPieces[0]

# Build list of parameters
paramList = []
for i in range(1,len(cmdPieces)):
	index = 0
	try:
		param = string.upper(cmdPieces[i])
		index = fuzzTypes.index(param)
	except ValueError:
	# Not a fuzz data type, must be static parameter
		index = -1
	paramList.append([i,index,cmdPieces[i],1])

time.sleep(3)

try:
	while doneFuzzing(paramList,maxLength) == False:
		# Build execute string
		cmdExec = target
		for i in range(0,len(paramList)):
			# Add a space
			cmdExec += " "
		
			if paramList[i][STR_INDEX] == -1:
			# Static parameter
				cmdExec += paramList[i][PARAM]
			else:
			# Fuzz type
				paramType = string.upper(paramList[i][PARAM])
				currLength = paramList[i][COUNT]
				if paramType == "STR":
					cmdExec += paramType.replace("STR",getRandomString(currLength))
				elif paramType == "NUM":
					cmdExec += paramType.replace("NUM",getRandomNumber(currLength))
				elif paramType == "FRM":
					cmdExec += paramType.replace("FRM",getRandomFormat(currLength))
				elif paramType == "SYM":
					cmdExec += paramType.replace("SYM",getRandomSymbol(currLength))
				elif paramType == "RAN":
					cmdExec += paramType.replace("RAN",getRandomRandom(currLength))
		
		print "Calling: " + cmdExec
		status = os.WTERMSIG(os.system(cmdExec))
		
		if status == signal.SIGSEGV or status == signal.SIGILL or status == signal.SIGABRT:
			print "\nTarget process has crashed."
			printInfo(cmdExec,paramList)
			sys.exit(0)
		
		# Increment first param count
		# Goes through every permutation
		done = False
		for i in range(0,len(paramList)):
			if paramList[i][STR_INDEX] != -1:
				done = False
				paramList[i][COUNT] += increment
				if paramList[i][COUNT] > maxLength:
					paramList[i][COUNT] = 1
					done = True
				else:
					break
		if done == True:
			break
		time.sleep(pause)

	print "Target process did not crash\n"
	
except KeyboardInterrupt:
	print "\nAborting..."
	printInfo(cmdExec,paramList)
	sys.exit(0)