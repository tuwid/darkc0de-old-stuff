#!usr/bin/python
##############################################################
# Bing url grabber -hkm [@] hakim [.] ws- 6/5/2009
# ------------------------------------------------version 1.0
# Parses urls from Bing (991 Max results * sites * keywords)
# Stores results in badabing_log.txt
##############################################################
#     http://www.hakim.ws     https://www.underground.org.mx
##############################################################

import sys, urllib2, socket, time, os
from optparse import OptionParser

i = 1;j=1;total=0;a=1
socket.setdefaulttimeout(10)

def intro():
	print "\n\t   Bing url grabber 1.0 2009"
	print "               hkm [@] hakim [.] ws"
	print "   --------------------------------------------\n"

def end():
	print "[-] Done\n"
	print "   --------------------------------------------"
	print "\n[ "+str(total)+" ] Links found and stored in badabing_log.txt\n"
	print "   --------------------------------------------\n\n"

def scarab(link):
	global a
	if not os.path.isdir("badabing_sqlmaplog"):
		os.mkdir("badabing_sqlmaplog")
	outputsc = open("badabing_sqlmaplog/"+str(a)+"-request", "w")
	outputsc.writelines("GET "+link+" HTTP/1.1 \n")
	outputsc.close()
	a=a+1

intro()

usage = "usage: %prog [options] [query]"
parser = OptionParser(usage=usage)
parser.add_option("-s", "--site", dest="sitelist",help="Use a 'site:' list", metavar="FILE")
parser.add_option("-k", "--keywords", dest="keywords",help="Use a keyword/query list", metavar="FILE")
parser.add_option("-l", "--sqlmap",action="store_true", dest="scarab",help="save sqlmap compatible log (dir)")
(options, args) = parser.parse_args()

if len(sys.argv) < 2:
	parser.print_help()
	print "\n"
	sys.exit()

def workit(site, query):
	i = 1;
	host = "http://www.bing.com/search?q="+query.replace(" ","+")+"&filt=all&first="
	output = open("badabing_log.txt", "a")
	source = urllib2.urlopen(host+str(i)).read()
	pcount = source.find("1-10", 0, len(source))
	if pcount > 0:
		pcounte = source.find(" ", pcount+8, len(source))
		z = int(source[pcount+7:pcounte].replace(",",""))
	if pcount < 0:
		print "No results for "+host
		z = 0
	if z > 1000:
		z = 1001
	linkcount = 0
	while i<z:	
		try:
			host = "http://www.bing.com/search?q="+query.replace(" ","+")+"&filt=all&first="
			req = urllib2.Request(host+str(i))
			req.add_header('Cookie',"SRCHHPGUSR=NEWWND=0&NRSLT=50")
			response = urllib2.urlopen(req)
			source = response.read()
			start = 0
			count = 1
			end = len(source)
			numlinks = source.count("<h3><a href", start, end)
			while count < numlinks:			
				start = source.find("<h3><a href",start,end)
				end = source.find(" onmouse",start,end)
				link = source[start+13:end-1].replace("amp;","")
				print link
				if options.scarab == True: scarab(link)
				output.writelines(link+"\n")
				linkcount = linkcount + 1
				start = end
				end = len(source)
				count = count+1
			i = i+50
		
		except(urllib2.URLError, socket.timeout, socket.gaierror, socket.error):
			pass
		except(KeyboardInterrupt):
			output.close()
			print "\n\n[ "+str(linkcount)+" ] "+site+" Links found"
			print "\n[ "+str(total)+" ] Links found and stored in badabing_log.txt\n"
			sys.exit("[-] Interrupted!\n")
	print "\n[ "+str(linkcount)+" ] "+site+" Links found\n"
	global total
	total = total + linkcount
	output.close()

queryo = sys.argv[-1]
if options.scarab == True: queryo=""

if options.keywords != None and options.sitelist != None:
	sitelist = open(options.sitelist,"r")
	site = sitelist.readline()
	keywordslist = open(options.keywords,"r")
	keywords = keywordslist.readline()
	while site:
        	if site[-1] == "\n":
			site = site[:-1]
    			while keywords:
        			if keywords[-1] == "\n":
					keywords = keywords[:-1]
					query = "site:"+site+" "+keywords+" "+queryo
					workit(site,query)
					keywords = keywordslist.readline()
					query=""
			keywordslist.close()
			site = sitelist.readline()
			keywordslist = open(options.keywords,"r")
			keywords = keywordslist.readline()

	sitelist.close()
	end()

if options.sitelist != None and options.keywords == None:
	sitelist = open(options.sitelist,"r")
	site = sitelist.readline()
    	while site:
        	if site[-1] == "\n":
			site = site[:-1]
			query = "site:"+site+" "+queryo
			workit(site,query)
			query = ""
		site = sitelist.readline()
		sitelist.close()
	end()

if options.keywords != None and options.sitelist == None:
	keywordslist = open(options.keywords,"r")
	keywords = keywordslist.readline()
    	while keywords:
        	if keywords[-1] == "\n":
			keywords = keywords[:-1]
			query = keywords+" "+queryo
			workit("",query)
			keywords = keywordslist.readline()
			query=""
	keywordslist.close()
	end()

if options.keywords == None and options.sitelist == None:
	workit("",queryo)
	end()
