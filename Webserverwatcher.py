#!usr/bin/python 
 
import httplib, socket, time, re, os, sys, datetime 
 
# Hello world! 
os.system('clear') 
print "===================================================" 
print "== Webserverwatcher.py | www.ethicalhack3r.co.uk ==" 
print "===================================================" 
print 
url = raw_input("Enter the URL you want to keep an eye on: ") 
 
# Check URL 
http = "http://" 
 
if http in url: 
	print 
	print "ERROR! Remove http:// from the URL." 
	url = raw_input("Enter the URL you want to keep an eye on: ") 
 
count = 0 
 
while 1: 
 
	# Count how many times the script has run 
	count = count + 1 
 
	# Get todays date/time 
	getdate = datetime.datetime.today() 
	today = getdate.strftime("%d/%m/%Y %H:%M:%S") 
 
	# Get webserver IP 
	socket.setdefaulttimeout(15) 
 
	try: socket.gethostbyname(url) 
	except socket.error: 
		os.system('clear') 
		print "===================================================" 
		print "== Webserverwatcher.py | www.ethicalhack3r.co.uk ==" 
		print "===================================================" 
		print 
		print "SOCKET ERROR! 1)Check the URL 2)Check your internet connection 3)Try again." 
		print 
		sys.exit() 
 
	# HTTP HEAD request 
	conn = httplib.HTTPConnection(url, 80) 
 
	try: conn.request("HEAD", "/") 
	except socket.timeout: 
		print "Webserver has timed out. Check URL and internet connection." 
 
	# Read HTTP response 
	res = conn.getresponse() 
 
	# Close HTTP connection 
	conn.close() 
 
	# Turn headers into variables 
	ip = socket.gethostbyname(url) 
	server = res.getheader('Server') 
	xpoweredby = res.getheader('x-powered-by') 
	date = res.getheader('date') 
 
	# Print some output 
	os.system('clear') 
	print "===================================================" 
	print "== Webserverwatcher.py | www.ethicalhack3r.co.uk ==" 
	print "===================================================" 
	print 
	print res.status, res.reason 
	print 
 
	if xpoweredby == None: 
		print ip + " " + server + " " + date 
	else: 
		print ip + " " + server + " " + xpoweredby + " " + date 
 
	print 
	print "The script has run", count, "time/s." 
 
	if (count < 2): 
 
		# Save header data to log file 
		outfile = file('log.txt', 'w') 
		outfile.write("Started on " + today + "\n") 
		outfile.write(ip + " ") 
		outfile.write(server + " ") 
 
		# Check if xpoweredby header exists, if it does save to log 
		if xpoweredby != None: 
			outfile.write(xpoweredby + " ") 
			outfile.write(date + "\n") 
			outfile.close() 
		else: 
			outfile.write(date + "\n") 
			outfile.close() 
 
		# Print some output 
		print 
		print "Logged!" 
		print 
	else: 
 
		# Read file to compare old/new headers 
		readfile = open('log.txt', "r") 
		text = readfile.read() 
 
		# Check if log file IP is same as new IP 
		if ip not in text: 
			outfile = file('log.txt', 'a') 
			outfile.write('IP address has been changed! New IP is ' + ip + ' ' + date + '\n') 
			outfile.close() 
 
		# Check if log file server is same as new server 
		if server not in text: 
			outfile = file('log.txt', 'a') 
			outfile.write('Web Server software has been changed! New server is ' + server + ' ' + date + '\n') 
			outfile.close() 
 
		# Check if log file x-powered-by header is same as new one 
		if xpoweredby != None and xpoweredby not in text: 
			outfile = file('log.txt', 'a') 
			outfile.write('X-powered-by header has been changed! New header is ' + xpoweredby + ' ' + date + '\n') 
			outfile.close() 
 
	# Time to wait between HTTP requests (3600 seconds = 1hr) 
	try: time.sleep(3600) 
	except KeyboardInterrupt: 
			outfile = file('log.txt', 'a') 
			outfile.write("Finished on " + today) 
			outfile.close() 
			print 
			print "Check log.txt." 
			print 
			sys.exit() 

