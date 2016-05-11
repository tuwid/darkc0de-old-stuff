#!/usr/bin/python 
# 
# low1z / forum.darkc0de.com / 2aug09 
# 
# ShoutMix reader/poster 
# 
# favorable to use with -s d3hydr8 to get the darkc0de feed 
# 
# example: python shoutmix_tool.py -s d3hydr8 -l   <- read the latest 
#          python shoutmix_tool.py -s d3hydr8 -p   <- post something 
 
import sys, re, time, os, urllib2, urllib, cookielib 
from optparse import OptionParser 
 
realhost = 'www6' # real webserver for the shoutmix you want to work with, get your info by opening the shout you need in the browser 
 
if sys.platform == 'linux' or sys.platform == 'linux2': 
	clearscreen = 'clear' 
else: 
	clearscreen = 'cls' 
 
def StripTags(text): 
        return re.sub(r'<[^>]*?>','', text) 
 
def timer(): 
	now = time.localtime(time.time()) 
	return time.asctime(now) 
 
def readLatest(COUNT): 
	request = urllib2.Request('http://'+realhost+'.shoutmix.com/?'+options.smuser+'&view='+COUNT) 
	response = urllib2.urlopen(request) 
	rspinfo = response.read() 
	myrsp = rspinfo.split('<cite>') 
	del myrsp[0] 
	print "Shoutmix : http://"+realhost+".shoutmix.com/?"+options.smuser+"\n" 
	for myinfo in myrsp: 
		myinfostripped = StripTags(myinfo) 
		spinfo1 = myinfostripped.split('Details') 
		postinfo = spinfo1[0].split(' ',1) 
		postername = postinfo[0] 
		post = postinfo[1] 
		tdi = spinfo1[1].split(' ',2) 
		print "Name:", postername, "\nTime:",tdi[0]+" / "+tdi[1], "\nPost:",post, "\n" 
 
def postmsg(): 
	myname = raw_input('Name    : ') 
	mymsg = raw_input('Message :') 
	submitvalue = "submit" 
	myidcode = getClientCode() 
	cjar = cookielib.CookieJar() 
	myopener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cjar)) 
	user_agent = 'Mozilla/4.0 (compatible, MSIE 5.5; Windows NT)' 
	headers = {'User-Agent': user_agent} 
	myvalues = [ ('name', myname), ('message', mymsg), ('code', myidcode), ('shout', submitvalue) ] 
	fencode = urllib.urlencode(myvalues) 
	rqdata = urllib2.Request('http://'+realhost+'.shoutmix.com/?'+options.smuser+"=process", fencode, headers) 
	respdata = urllib2.urlopen(rqdata).read() 
	print "string sent" 
 
def getClientCode(): 
        request = urllib2.Request('http://'+realhost+'.shoutmix.com/?'+options.smuser) 
        response = urllib2.urlopen(request) 
        rspinfo = response.readlines() 
	for line in rspinfo: 
		mymd5code = re.findall("[a-f0-9]"*32,line)[1] 
	return mymd5code 
 
 
print "+-----------------------------------------+" 
print "|        S h o u t M i X _ Tool v0.2      |" 
print "| 					 |" 
print "|        low1z / forum.darkc0de.com       |" 
print "+-----------------------------------------+\n" 
 
parser = OptionParser() 
parser.add_option("-l", dest='readLatest',action='store_true', default=False, help="Fetch Latest Shout Entries") 
parser.add_option("-a", dest='readALL',action='store_true', default=False, help="List all Shout Entries") 
parser.add_option("-p", dest='postShout',action='store_true', default=False, help="Post Shout") 
parser.add_option("-r", dest='autoRefresh',action='store_true', default=False, help="Auto Refresh Latest") 
parser.add_option("-s",type='string', dest='smuser',action='store', help="Shoutmix Username") 
(options, args) = parser.parse_args() 
 
if options.readLatest == True: 
	if options.smuser != None: 
		readLatest('1') 
	else: 
		print "-s option is nessesary, it tells the script which shoutmix to query, exiting!" 
		sys.exit(0) 
 
if options.readALL == True and options.smuser != None: 
	maxview = raw_input('How Far will we query from here? :') 
	for x in range(0,int(maxview)): 
		readLatest(str(x)) 
 
if options.postShout == True: 
	postmsg() 
	sys.exit(0) 
 
if options.autoRefresh == True: 
	if options.smuser != None: 
		autorf = 1 
		while autorf == 1: 
			readLatest('1') 
			time.sleep(60) 
			os.system(clearscreen) 
	else: 
		print "-s option is nessesary, it tells the script which shoutmix to query, exiting!" 
		sys.exit(0)
