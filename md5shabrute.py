#!/usr/bin/python 
# This was written for educational and learning purposes only. 
# The author will be not responsible for any damage! 
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
#Special thanks to d3hydr8! 
 
import hashlib, sys, fileinput, re, time 
from optparse import OptionParser 
 
usage= "./%prog -w <wordlist> -H <hashtype[md5,sha1]> [options]" 
usage = usage+"\nExample: ./%prog -w words.txt -H md5 -s dcad9e14ee1e74f957d6f88568e61181" 
parser = OptionParser(usage=usage) 
parser.add_option("-w", 
                  action="store", dest="Inputfile", 
                  help="Wordlist") 
parser.add_option("-H", type="string", 
                  action="store", dest="hash", 
                  help="Hash type") 
parser.add_option("-s", type="string", 
                  action="store", dest="hashtocrack", 
                  help="Raw hash to crack") 
parser.add_option("-f", type="string", 
                  action="store", dest="hashstocrack", 
                  help="Raw hashs to crack from file") 
(options, args) = parser.parse_args() 
 
if len(sys.argv) != 7: 
	print "\n|---------------------------------------------------------------|" 
	print "|        MD5 and SHA1 hash list generator & cracker v0.5        |" 
	print "|                       by MrMe 06/2009                         |" 
	print "|                    Special Greetz: krma                       |" 
	print "|                  mrme-grayhat.blogspot.com                    |" 
	print "|---------------------------------------------------------------|\n" 
   	parser.print_help() 
	sys.exit(1) 
 
hashtype = options.hash 
 
try: 
	names = open(sys.argv[2], "r") 
except(IOError): 
	print "[-] Error: Check your wordlist path" 
  	sys.exit(1) 
 
def howmanylines(): 
	print "[+] Cracking the hash(s).." 
	try: 
		names = open(sys.argv[2], "r") 
	except(IOError): 
		print "[-] Error: Check your wordlist path" 
  		sys.exit(1) 
	lines = len(names.readlines()) 
	print "[+] Loaded",lines,"hashes" 
 
def timer(): 
	now = time.localtime(time.time()) 
	return time.asctime(now) 
 
def checker(): 
	if hashtype == "md5": 
		if len(hash) != 32: 
			print "[-] This is not an MD5 hash" 
			sys.exit() 
	if hashtype == "sha1": 
		if len(hash) != 40: 
			print "[-] This is not an SHA-1 hash" 
			sys.exit() 
 
def hashme(): 
	for line in names: 
		nline = line.rstrip() 
		if hashtype == "md5": 
			md5hash = hashlib.md5(nline).hexdigest()
			lasthash = md5hash[:8]
			printer = lasthash + nline
		if hashtype == "sha1": 
			sha1hash = hashlib.sha1(nline).hexdigest()
			lasthash = sha1hash[:8]
			printer = lasthash + nline
		hashes.write(printer+"\n") 
	hashes.close() 
	print "[+] Cracking the "+hashtype+" hash!" 
 
 
def cracker(): 
	if hashtype == "md5": 
		md5 = open("md5.dat", "r") 
		for line in md5:
                        rehash = hash[:8]
			match = re.search(rehash,line)
			if match:
				nline = line.rstrip()
				x = nline[8:]
				trying = hashlib.md5(x).hexdigest()
				if trying == hash:
                                        match = "\n    [+] Password cracked! " +x+"\n"
				break 
	elif hashtype == "sha1": 
		sha1 = open("sha1.dat", "r") 
		names = open(sys.argv[2], "r") 
		lines = len(names.readlines()) 
		for line in sha1:
                        rehash = hash[:8]
			match = re.search(rehash,line) 
			if match != None: 
				nline = line.rstrip()
				x = nline[8:]
				trying = hashlib.sha1(x).hexdigest()
				if trying == hash:
                                        match = "\n    [+] Password cracked! :" +x+"\n" 
				break 
	if match == None: 
		print "[-] Password not found, try with a bigger dict" 
	else: 
		print match 
		print "[+] Cracking finished at: " +timer() 
 
print "[+] Begin cracking at: " +timer() 
 
def nofile(): 
	print "[-] "+hashtype+".dat file doesn\'t exist" 
	print "[+] Building "+hashtype+".dat hash file.. hold onto your knickers" 
 
howmanylines() 
if sys.argv[5] == "-s": 
	hash = options.hashtocrack 
	checker() 
	try: 
		open(hashtype+".dat", "r") 
	except(IOError): 
		hashes = open(hashtype+".dat", "w") 
		nofile() 
		hashme() 
	cracker() 
if sys.argv[5] == "-f": 
	try: 
		open(hashtype+".dat", "r") 
	except(IOError): 
		hashes = open(hashtype+".dat", "w") 
		nofile() 
		hashme() 
	try: 
		multi_hash = open(sys.argv[6], "r") 
	except(IOError): 
		print "[-] Error: Check your wordlist path" 
  		sys.exit(1) 
	for line in multi_hash: 
		nline = line.rstrip() 
		hash = nline 
		cracker()
