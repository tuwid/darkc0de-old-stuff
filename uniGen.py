##!/usr/bin/python
################################################################ 
#       .___             __          _______       .___        # 
#     __| _/____ _______|  | __ ____ \   _  \    __| _/____    # 
#    / __ |\__  \\_  __ \  |/ // ___\/  /_\  \  / __ |/ __ \   # 
#   / /_/ | / __ \|  | \/    <\  \___\  \_/   \/ /_/ \  ___/   # 
#   \____ |(______/__|  |__|_ \\_____>\_____  /\_____|\____\   # 
#        \/                  \/             \/                 # 
#                   ___________   ______  _  __                # 
#                 _/ ___\_  __ \_/ __ \ \/ \/ /                # 
#                 \  \___|  | \/\  ___/\     /                 # 
#                  \___  >__|    \___  >\/\_/                  # 
#      est.2007        \/            \/   forum.darkc0de.com   # 
################################################################ 
# uniGen.py - universal pattern based wordlist generator
# fill the gaps in your wordlist / generate wordlists for wifi attacks
#
# darkc0de Crew 
# www.darkc0de.com 
# code low1z
# 
# Greetz to 
# d3hydr8, rsauron, baltazar, inkubus, kopele, p47rick, houby
# and the rest of the Darkc0de members 
#
# examples:
#
# uniGen.py -s MyPassword99
#	- generate a wordlist from a single word pattern
#
# uniGen.py -m plains.txt  
#	- generate a top10 pattern list from a plain password file
#	- choose one pattern to generate a special wordlist
#
# uniGen.py -c
#	- constructor mode
#	- define pattern by word
#	- add prefix to pattern
#	- adjust count of words to be generated
#	- generate a wordlist with defined parameters
#
# NO DUPE CHECKS, average dupecount < 1% @ password length > 7

version = '0.2b'
ldm = 'jun_10_09'

import string, sys, time
from random import choice
from optparse import OptionParser

def extPatConv(cword):
	text = ''
	for i in  range ( len(cword) ):
		if cword[i] in string.ascii_lowercase:
			text = text + 'x'
		elif cword[i] in string.ascii_uppercase:
			text = text + 'X'
		elif cword[i] in string.digits:
			text = text + 'N'
		elif cword[i] in string.punctuation:
			text = text + 'S'
	        else:
			break
	return text			

def PatternPwd(pattern):
        newpasswd = ''
        for i in range(len(pattern)):
		if pattern[i] == 'x':
		        chars = string.ascii_lowercase
	                newpasswd = newpasswd + choice(chars)
		if pattern[i] == 'X':
		        chars = string.ascii_uppercase
	                newpasswd = newpasswd + choice(chars)
		if pattern[i] == 'N':
		        chars = string.digits
	                newpasswd = newpasswd + choice(chars)
       	return newpasswd

def txt2top(fname):
	fp = open(fname, "r").readlines()
	mydic = {}
	for entry in fp:
		tmpgen = extPatConv(entry[:-1])
		if mydic.has_key(tmpgen):
			mydic[tmpgen] += 1
		else:
			mydic[tmpgen] = 1
	tmplist = []
	for pat,cnt in mydic.items():
		if cnt not in tmplist:
			tmplist.append(cnt)
	tmplist.sort(reverse=True); tmpdic = {}
	print "\nNo \t: Count   :   Pattern\n" 
	for x in range(0,20):
		for pat,cnt in mydic.items():
			if cnt == tmplist[x]:
				tmpdic[pat] = cnt
	stecnt = 0
	for pat,cnt in tmpdic.items():
		stecnt += 1
		print str(stecnt), "\t:", cnt, "  \t", pat
	patkey = raw_input('Pattern Number: ')
	patarray =  tmpdic[tmpdic.keys()[int(patkey)-1]]
	for pat,cnt in tmpdic.items():
		if cnt == patarray:
			return pat

parser = OptionParser()
parser.add_option("-c", dest='construct',action='store_true', default=False, help="Start in Construct Mode")
parser.add_option("-s",type='string', dest='single_plain',action='store', help="Single Password for generator")
parser.add_option("-m",type='string', dest='plain_list',action='store', help="List of Plains for Top10 generator")
parser.add_option("-w",type='string', dest='outfile',action='store', help="output filename for saving")
(options, args) = parser.parse_args()

print "               _ ______"
print "  __  ______  (_) ____/__  ____"
print " / / / / __ \\/ / / __/ _ \/ __ \\      code : low1z"
print "/ /_/ / / / / / /_/ /  __/ / / /  modified :", ldm
print "\__,_/_/ /_/_/\____/\___/_/ /_/    version :", version, "\n"

if options.single_plain != None:
	tmppat =  extPatConv(options.single_plain)
	numgen = raw_input("Number of Passwords to generate : ")
	if options.outfile == None:
		lclfn = raw_input("Saving as : ")
	else:
		lclfn = options.outfile
	fnp = open(lclfn, "w")
	if numgen.isdigit():
		for x in range(0,int(numgen)):
			tmppp = PatternPwd(tmppat)
			fnp.write(tmppp+"\n")
	fnp.close()

if options.plain_list != None:
	tmppat =  extPatConv(txt2top(options.plain_list))
	numgen = raw_input("Number of Passwords to generate : ")
        if options.outfile == None:
                lclfn = raw_input("Saving as : ")
        else:
                lclfn = options.outfile
        fnp = open(lclfn, "w")	
	if numgen.isdigit():
		for x in range(0,int(numgen)):
                        tmppp = PatternPwd(tmppat)
                        fnp.write(tmppp+"\n")
	fnp.close()

if options.construct == True:
	pwdFin = ''; myPattern = ''; myprefix = ''
	GenCount = 10000
	while pwdFin != 'exit':
		print "\n+-----------------+"
		print "| Current Prefix  : ", myprefix
		print "| Current Pattern : ", myprefix+myPattern
		print "| Generator Count : ", GenCount
		print "+-----------------+\n"
		print "[1] Erase Current Pattern & Prefix"
		print "[2] Enter Plain Password"
		print "[3] Add Prefix (eg. SP-XXXNNX)"
		print "[4] Set Generator Count"
		print "[5] Fixed Length Generator (random)"
		print "\n[9] Generate"
		print "[0] EXIT"
		pwdFin = raw_input("\n( 1|2|3|4|5|9|0 ) : ")
		if pwdFin == '1':
			print "clearing prefix & pattern..."
			myPattern = ''; myprefix = ''
		if pwdFin == '2':
			myPattern = extPatConv(raw_input("Password : "))
		if pwdFin == '3':
			myprefix = raw_input("Prefix : ")
		if pwdFin == '4':
			GenCount = raw_input("New Generator Count : ")
		if pwdFin == '5':
			mylen = raw_input("Lengh : ")
                        if options.outfile == None:
                                lclfn = raw_input("Saving as : ")
                        else:
                                lclfn = options.outfile
                        fnp = open(lclfn, "w")
			for x in range(0, int(GenCount)):
			        newpasswd = ''
			        for i in range(0, int(mylen)):

					cchoice = [string.ascii_lowercase, string.ascii_uppercase, string.digits]
			                chars = choice(cchoice)
			                newpasswd = newpasswd + choice(chars)
				fnp.write(newpasswd+"\n")
			fnp.close()
		if pwdFin == '9':
		        if options.outfile == None:
		                lclfn = raw_input("Saving as : ")
		        else:
		                lclfn = options.outfile
		        fnp = open(lclfn, "w")
	                for x in range(0,int(GenCount)):
	                        tmppp = PatternPwd(myPattern)
	                        fnp.write(myprefix+tmppp+"\n")
		        fnp.close()
			pwdFin = 'exit'
		if pwdFin == '0':
			pwdFin = 'exit'
