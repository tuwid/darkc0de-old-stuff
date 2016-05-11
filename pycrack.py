#!/usr/bin/python
# PyCrack 0.1
# Matthew Ranostay <mranostay@saberlogic.com>

import os, sys
from ctypes import *
from datetime import datetime,timedelta

libcrypt = cdll.LoadLibrary("libcrypt.so")

crypt = libcrypt.crypt
crypt.restype = c_char_p
today = datetime.today()

def parseShadowFile(filename):
    data = []
    file = open(filename,"r")
    for line in file.readlines():
        line = line.replace("\n","").split(":")
        if len(line) == 10 and not line[1] in [ 'x', '*' ]:
            line[1] = [ x for x in line[1].split("$") if x ]
            if line[1][0] == '1':
                data += [ [ line[0] ] + line[1][1:] ]
    return data

def getPassword(password,salt,hash):
    result = crypt(password,salt).split("$")
    return result[-1] == hash
    

def process(wordlist,hashes):
    file = open(wordlist,"r")
    for word in file.readlines():
        word = word[:-1]
        if not hashes:
            break
        
        for hash in hashes:
            password = getPassword(word,"$1$" + hash[1],hash[2])
            
            if password:
                time = str(datetime.today() - today)
                print "PASSWORD FOUND: ","Username: ", hash[0], "Password: ", word, "Time: ", time
                print
                del hashes[hashes.index(hash)]

if __name__ == '__main__':
    print "PyCrack v1.0"

    if len(sys.argv) == 3:
        print "\nStarting cracking..."
        data = parseShadowFile(sys.argv[1])
        process(sys.argv[2],data)

        time = str(datetime.today() - today)
        print "\nFinished in %s..." % time
    else:
        print "Usage: ./pycrack /etc/shadow dictionary"
