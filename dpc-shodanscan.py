#!/usr/bin/python 
# dpc-shodanscan.py v1.0 
# network service search engine tools using shodan query 
# usage: ./dpc-shodanscan.py -q <shodan_query> -f <log_file_name> 
# ex. 
# ./dpc-shodanscan.py -q squid -f log.txt 
# ex shodan query: 
# 1.How about finding only apache servers running version 2.2.3? 
# ./dpc-shodanscan.py -q apache+2.2.3 -f log.txt 
# 2.get all web (port:80) hosts running 'apache' in switzerland 
# (country:CH) that also have '.ch' in any of their domain names: 
# ./dpc-shodanscan.py -q apache+country:CH+port:80+hostname:.ch -f log.txt 
# 
# c0ded by: 5ynL0rd <5ynlord@depredac0de.net> 
# special thx to: d3hydr8,xco, Dr_EIP, ch3cksum, gat3w4y, g4pt3k, shamus, pyfla, unixc0de 
# for community: darkc0de, depredac0de, and antijasakom 
#******************************************************************************************

from sgmllib import SGMLParser
import urllib, sys, re, os

class URL(SGMLParser):
	def reset(self):
		SGMLParser.reset(self)
		self.urls=[]
	def start_a(self,attrs):
		href = [v for k,v in attrs if k=="href"]
		if href:
			self.urls.extend(href)
def label():
	os.name == "posix":
		os.system("clear")
	else:
		os.system("cls")
	banner = ''' 
 ____________________________________________________________________________
| network service search engine tools using shodan query                     |
| ex shodan query:                                                           |
| 1.How about finding only apache servers running version 2.2.3?             |
| ./dpc-shodascan.py -q apache+2.2.3 -f log.txt                              |
| 2.get all web (port:80) hosts running 'apache' in switzerland              |
| (country:CH) that also have '.ch' in any of their domain names:            |
| ./dpc-shodanscan.py -q apache+country:CH+port:80+hostname:.ch -f log.txt   |
|   ___________________                                                      |
| < dpc-shodanscan.py   >                                                    |
|   -------------------                                                      |
|            \   ,__,                                                        |
|             \  (oo)____                                                    |
|                (__)    )\                   5ynL0rd<at>depredac0de<dot>net |
|                   ||--|| *          depredac0de.net & antijasakom.org crew |
|____________________________________________________________________________|'''
	print banner

def crawl(page):
	try:
		sock = urllib.urlopen("http://shodan.surtri.com/?q=%s&page=%i"%(args1,page))
	except:
		print "[-] Connection problem"
	parser = URL()
	parser.feed(sock.read())
	return parser.urls
	sock.close()
	parser.close()

if __name__ == "__main__":
	page = 1
	if len(sys.argv) != 5:
		label()	
		print "usage: ./%s -q <shodan_query> -f <logfile>"%sys.argv[0]
		sys.exit(0)
	else:
		if sys.argv[1].lower() == "-q":
        		args1 = sys.argv[2]
		if sys.argv[3].lower() == "-f":
        		args2 = sys.argv[4]
	label()
	log = open(args2,"a")
	print "[+] Searching query: %s"%args1
	log.write("[+] Searching query: %s"%args1)
	log.close()
	print "[+] please wait!..."
	while page:
		data = crawl(page)
		for i in data:
			log = open(args2,"a")
			if re.search("http://",i):
				i = i.replace("http://","")					
				print "%s"%i
				log.write("%s\n"%i)
			log.close()
		if data[-3][-1:] == "/":
			print "Finished..."
			break
		page += 1

# depredator-c0de [01-01-2010]
