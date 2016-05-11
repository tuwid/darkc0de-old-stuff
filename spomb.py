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
#                                         www.beenuarora.com   #
################################################################
#Thanks to low1z for initial script
#Greetz to all darkc0de memeber

import os, smtplib, mimetypes,time,sys
from email.MIMEMultipart import MIMEMultipart 
from email.MIMEText import MIMEText 
 
def sendMail(gmailUser,gmailPassword,recipient,subject,text): 
        
        msg = MIMEMultipart() 
        msg['From'] = gmailUser 
        msg['To'] = recipient 
        msg['Subject'] = subject 
        msg.attach(MIMEText(text)) 
        mailServer = smtplib.SMTP('smtp.gmail.com', 587) 
        mailServer.ehlo() 
        mailServer.starttls() 
        mailServer.ehlo() 
        mailServer.login(gmailUser, gmailPassword) 
        mailServer.sendmail(gmailUser, recipient, msg.as_string()) 
        mailServer.close() 
        print('[-] Sent email to %s :' % recipient) 
if sys.platform == 'linux-i386' or sys.platform == 'linux2' or sys.platform == 'darwin':
	SysCls = 'clear'
elif sys.platform == 'win32' or sys.platform == 'dos' or sys.platform[0:5] == 'ms-dos':
	SysCls = 'cls'
else:
	SysCls = 'unknown'

os.system(SysCls)

print "\n|---------------------------------------------------------------|"
print "| beenudel1986[@]gmail[dot]com                                  |"
print "| Spomb v1.0                                                    |"
print "|   Do Visit     www.BeenuArora.com      &        darkc0de.com  |"
print "|---------------------------------------------------------------|\n"
 
if len(sys.argv) < 2: 
	print "\nUsage: ./spammer.py list.txt" 
	print "Ex: ./spomb.py list.txt\n" 
	sys.exit(1)

list= sys.argv[1] 
try:

	hosts= open(list,'r')
except (IOError):
	print " \n\nSpamming List Missing ..Exiting :("
	sys.exit(0)


count= raw_input('Enter the Number of mails :')
gmailUser = raw_input('Enter Your Email ID :') 
if sys.platform == 'linux-i386' or sys.platform == 'linux2' or sys.platform == 'darwin':
	os.system('stty -echo')
gmailPassword = raw_input('Enter Your Gmail Password :') 
list= sys.argv[1]
if sys.platform == 'linux-i386' or sys.platform == 'linux2' or sys.platform == 'darwin': 
	os.system('stty echo')
subject = raw_input('\nSubject :') 
text = raw_input('Text :')
for a in range (0,int(count)):
	for host in hosts:
 		recipient=host[:-1]
		try: 
		        sendMail(gmailUser,gmailPassword,recipient,subject,text) 
		        time.sleep(10)
		except(urllib2.URLError, socket.timeout, socket.gaierror, socket.error): 
				print ('Something Went Wrong ..Check Manually for Error\n') 
		except(KeyboardInterrupt): 
				pass 
print ('\n\nDone Mailing...')

