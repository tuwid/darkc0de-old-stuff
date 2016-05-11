#!/usr/bin/python
#
# linux ONLY
#
# ProxyHarvest.py v1.1
#
# REQUIREMENTS:
#	- GeoIP Database + GeoIP Python API
#	- sudo apt-get install libgeoip1 && sudo apt-get install python-geoip (ubuntu/debian)
#
# Extract IP:Port from a proxylist site code from low1z lurking at darkc0de.com
# this code is protected under the gpl get your copy at <http://www.gnu.org/licenses/>
#
# update from 0.9 - 1.1 notes
# - fetch planetlab(codeen) proxylist & clean our list with it
# - validate external ip with whatsmyip.com
# - GeoIP
#
# - !! due to urllib1/2 limitations there is no way yet to except username/passwd input !!

import sys, os, urllib, urllib2, re, httplib, sets, socket
from time import time, localtime, strftime
from socket import gethostbyaddr

nogeoip = 0
try:
	import GeoIP
except:
	nogeoip = 1
	print "\nGeoIP Module/Database NOT found, try:"
	print "sudo apt-get install libgeoip1 && sudo apt-get install python-geoip"
	print "or visit www[.]maxmind[.]com for download"
	print "GeoIP is not required but highly recommended!\n"

output = 'proxylist.txt'
sleeptimer = 3
socket.setdefaulttimeout(2)
alivelist = []
myipadress = urllib.urlopen('http://www.whatismyip.com/automation/n09230945.asp').read()
anon_list = []
trans_list = []
planetlab = []

sites = ['http://www.darkc0de.com/cgi-bin/proxies.py',
	 'http://www.1proxyfree.com/', 
	 'http://www.atomintersoft.com/products/alive-proxy/socks5-list/',
	 'http://www.proxylist.net/',
	 'http://www.proxylists.net/http_highanon.txt']

def StripTags(text):
	return re.sub(r'<[^>]*?>','', text)

def timer():
	now = strftime('%H:%M:%S-%d/%b/%Y', localtime())
	return now

def ipcheck(proxy):
	try:
		pxhandle = urllib2.ProxyHandler({"http": proxy})
		opener = urllib2.build_opener(pxhandle)
		urllib2.install_opener(opener)
		myip = urllib2.urlopen('http://www.whatismyip.com/automation/n09230945.asp').read()
		xs =  re.findall(('\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}'), StripTags(myip))
		if xs[0] == myipadress or myipadress == myip:
			trans_list.append(proxy)
			print proxy[:-1],"\t- ALIVE -", timer(), "- TRANSPARENT"
		elif xs == None:
			pass
		else:
			anon_list.append(proxy)
			print proxy[:-1],"\t- ALIVE -", timer(), "- EXT-iP :",xs[0]
	except KeyboardInterrupt:
		print "\n\nCTRL+C - check temporary proxylist file\n\n"
		sys.exit(0)
	except:
		pass

def proxyvalidator(proxylist):
        finalcount = 0
	for proxy in proxylist:
		proxy.replace('\n', '')
		try:
			proxies = {'http': "http://"+proxy[:-1]}
			opener = urllib.FancyURLopener(proxies)
			try:
				loopchk = opener.open("http://www.google.com").read()
			except:
				pass
		except(IOError,socket.timeout), detail: 
			pass
		ipcheck(proxy)		
		alivelist.append(proxy)
		finalcount += 1
	return alivelist

def getsamairdotru():
	counter = 1
	pxycnt = 0
	maxpages = 10
	urls = []
	pfile = file(output, 'a')
	while counter <= maxpages:
		if counter < 10: # workaround for page-01 to page-09
			opener = urllib2.build_opener()
			opener.addheaders = [('User-agent', 'Mozilla/5.0')]
			url = opener.open('http://www.samair.ru/proxy/proxy-0'+repr(counter)+'.htm').read()
		else:
			opener = urllib2.build_opener()
			opener.addheaders = [('User-agent', 'Mozilla/5.0')]
			url = opener.open('http://www.samair.ru/proxy/proxy-'+repr(counter)+'.htm').read()
		strings = re.findall(('\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}:\d{1,5}'), StripTags(url))
		for string in strings:
			pfile.write(string+"\n")
			pxycnt = pxycnt+1
		counter = counter+1		
		opener.close()
	print pxycnt, "\t: Proxies received from : http://www.samair.ru/proxy/"
	pfile.close()

def getsinglesitelist(site):
        pxycnt = 0
        urls = []
        pfile = file(output, 'a')
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        url = opener.open(site).read()
        strings = re.findall(('\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}[:]\d{1,5}'), StripTags(url))
        for string in strings:
		pfile.write(string+"\n")
                pxycnt = pxycnt+1
	print pxycnt, "\t: Proxies recieved from :", site.split("//",3)[1]
        opener.close()
        pfile.close()

def getplanetlabs():
	opener = urllib2.build_opener()
        url = opener.open('http://fall.cs.princeton.edu/codeen/tabulator.cgi?table=table_all').read()
	strings = re.findall(('\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}'), StripTags(url))
	for string in strings:
		planetlab.append(string)
	print len(planetlab), "\t: PlanetLab Proxylist Loaded", "\n"

def cleanup():
	pfile = open(output, 'r').readlines()
	outfile = file(output, 'w')
	sorted = []
	finalcount = 0
	psremove = 0
	for proxy in pfile:
		if proxy.split(':',1)[0] not in planetlab:
			if proxy not in sorted:
				sorted.append(proxy)
				outfile.write(proxy)
				finalcount += 1
		if proxy.split(':',1)[0] in planetlab:
			psremove += 1
	print "\n", psremove, "\t: PlanetLab (CoDeen) Proxies removed!"
	print finalcount,"\t: unique Proxies found\n"
	print "+-[Starting Validation]-----------------------------------------------------+"
	outfile.close()

def fileConst():
	fileC = open(output, 'w')
	falive = []
	fileC.write('+ This List has been generated with proxyharvest_1.1.py // www.darkc0de.com\n')
	fileC.write('+ ANONYMOUS PROXIES\n\n')
	for anon in anon_list:
		fileC.write(anon)
		if anon in alivelist:
			alivelist.remove(anon)
        fileC.write('\n\n+ TRANSPARENT PROXIES\n\n')
        for trans in trans_list:
                fileC.write(trans)
		if trans in alivelist:
			alivelist.remove(trans)
	fileC.write('\n\n+ WORKING BUT UNCLEAR PROXIES\n\n')
	alivelist.sort()
	for alive in alivelist:
		fileC.write(alive)
	fileC.close()	

def helpme():
	print "| -s  / -sitecollect   :: gathers proxylists    |"
	print "| -m  / -multipage     :: get incremental pages |"
	print "| -a  / -all           :: do ALL!!!             |"
	print "| -vl / - validatelist :: check a file          |"
	print "+-----------------------------------------------+"
try:
	os.remove(output)
except:
	pass
print "+-----------------------------------------------+"
print "|              ProxyHarvest.py 1.1              |"
print "|            low1z 2009 // darkc0de             |"
print "+-----------------------------------------------+"
print "IP:", myipadress, "//", timer(), "\n"
getplanetlabs()

if len(sys.argv) <= 1:
        print "\n\t < use -help to get options >\n"
        sys.exit(1)

for arg in sys.argv[1:]:
	if arg.lower() == "-h" or arg.lower() == "-help":
        	helpme()		
	if arg.lower() == "-s" or arg.lower() == "-sitecollect":
		for site in sites:
			try:
			        getsinglesitelist(site)
			except:
				print "Error   :", site
		cleanup()
	        proxylist = open(output, 'r').readlines()
		proxyvalidator(proxylist)
	if arg.lower() == "-m" or arg.lower() == "-multipage":
		getsamairdotru()
		cleanup()
		print "may take some time to print out good proxies, be patient"
		try:
        		proxylist = open(output, 'r').readlines()
			proxyvalidator(proxylist)
		except:
			pass
	if arg.lower() == "-a" or arg.lower() == "-all":
		try:
	                for site in sites:
	                        getsinglesitelist(site)
			getsamairdotru()
			cleanup()
			proxylist = open(output, 'r').readlines()		
			proxyvalidator(proxylist)
		except:
			print "something went wront... using -a is seems a bit buggy"
	if arg.lower() == "-vl" or arg.lower() == "-validatelist":
                try:
			proxyfile = open(sys.argv[2], 'r').readlines()
			proxyvalidator(proxyfile)
                except(IndexError):
                        print "Error: check you proxy file ...\n"
			sys.exit(0)

print "\n+-[ANON LIST]-------------------------------------------------------------+\n"
for anon_proxy in anon_list:
	try: 
        	haddr = gethostbyaddr(anon_proxy.split(':',1)[0])
	except:
		haddr = '-'
	if nogeoip == 1:
		print anon_proxy.replace('\n',''),"\t| HostAdress:", haddr[0]
		pass
	elif nogeoip == 0:
		gi = GeoIP.new(GeoIP.GEOIP_MEMORY_CACHE)
		gx = gi.country_code_by_addr(anon_proxy.split(':',1)[0])
		print anon_proxy.replace('\n',''), "\t| Country:", gx,"\t| HostAdress:", haddr[0]
print "\n\t", len(anon_list), ": Total tested AnonProxies\n"
print "+-[TRANS LIST]--------------------------------------------------------------+\n"
for trans_proxy in trans_list:
        if nogeoip == 1:
                print trans_proxy.replace('\n','')
                pass
        elif nogeoip == 0:
		gi = GeoIP.new(GeoIP.GEOIP_MEMORY_CACHE)
		gx = gi.country_code_by_addr(trans_proxy.split(':',1)[0])
		print trans_proxy.replace('\n',''), "\t| Country:", gx
print "\n\t", len(trans_list), ": Total tested Transparent Proxies\n"
print "+-[OTHER SERVERS]-----------------------------------------------------------+\n"
if len(alivelist) > 16:
	print len(alivelist), "Alive but unverified Servers, check", output
else:
	for alive in alivelist:
		if alive not in trans_list:
			if alive not in anon_list:
				 print alive.replace('\n','')
fileConst()
