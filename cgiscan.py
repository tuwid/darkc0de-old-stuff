#!/usr/bin/python
#This is a CGI scanner, searches for common vulnerable 
#dirs and files.
#Save the bins.txt file to the dir your 
#running this. http://darkcode.ath.cx/scanners/bins.txt
#If you want verbose output , un-comment lines 78,79

#http://www.darkc0de.com
##d3hydr8[at]gmail[dot]com

import sys, httplib, time

def main(path):
	try:# make a http HEAD request
		h = httplib.HTTP(host+":"+port)
		h.putrequest("HEAD", path)
		h.putheader("Host", host)
		h.endheaders()
		status, reason, headers = h.getreply()
	except: 
		print "Error: Name or service not known. Check your host."
		sys.exit(1)
	return status, reason, headers.get("Server")
		
def timer():
	now = time.localtime(time.time())
	return time.asctime(now)
	

if len(sys.argv) != 3:
	print "\n\t   d3hydr8[at]gmail[dot]com CGIscanner v1.0"
	print "\t--------------------------------------------------"
	print "\n\tUsage: ./cgiscan.py <host> <port>\n"
	print "\tEx. ./cgiscan.py google.com 80\n"
	sys.exit(1)
	
host = sys.argv[1]
port = sys.argv[2]

if host[:7] == "http://":
	host = host.replace("http://","")

okresp = main("/")[:1]
badresp,reason,server = main("/d3hydr8.html")

if okresp[0] == badresp:
	print "\nResponses matched, try another host.\n"
	sys.exit(1)
else:
	print "\n   d3hydr8[at]gmail[dot]com CGIscanner v1.0"
	print "--------------------------------------------------"
	print "+ Target host:",host
	print "+ Target port:",port
	print "+ Target server:",server
	print "+ Target OK response:",okresp[0]
	print "+ Target BAD response:",badresp, reason
	print "+ Scan Started at",timer()


try:
	text = open("bins.txt", "r") #vulerable list, change path/name if necessary
	lines = text.readlines()
	text.close()
	print "\n[--",len(lines),"paths loaded --]\n"
except(IOError): 
 	print "Error: Check your bins.txt path.\n" 
	print "(http://www.darkc0de.com/scanners/bins.txt)\n"
	sys.exit(1)

num = 0

for line in lines:
	try: status, reason = main(line)[:2]
	except(AttributeError): pass
	if status == okresp[0]:
		num += 1
		print "\t++",status,reason,":",host+line,"\n"
	if status == int(401):
		print "\t--",status,reason,":",host+line,"\tNeeds Authorization\n"
	#else:								#uncomment for verbose mode
		#print "\n-",status,reason,":",host+line,"\n"   #uncomment for verbose mode
print "Scan completed at", timer()
if num == 0:
	print "Couldn't find anything.\n"
else:
	print "Found",num,"possible vulnerabilities, check manually.\n"


	