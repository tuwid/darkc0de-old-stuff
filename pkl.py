#! /usr/bin/python
# ~ Perfect Keylogger Admin Password Decrypt0r & Sett0r ~

# ~~JUST FOR FUN PROJECT! ~
# First of all:
# I DONT take ANY responsibility for this code. 
# You use it by YOUR OWN RISK!
# If you NOT accept it delete this file now!
# If you accept it have fun and backup your pk.bin file befor editing!

# [TARGET_INFO]
# Application  : Perfect Keylogger Demo\Fullversion 
# Version      : Tested with version 1.6.8.2
# Vendor       : BlazingTools - BlazingTools.com

# [SCRIPT_INFO]
# Autor        : Iman Karim
# Date         : 28. Jan. 2008
# E-Mail       : iman.karim \x40 smail \x2E inf \x2E fh-bonn-rhein-sieg \x2E de
# Additional   : Python OS Independent Code
# Greets       : SenoRita, Invisible, Exorzist, Xplosive

# [HOWTO]
# 1. Close Perfect Keylogger (Terminate it or Exit it)
#     Don't forget this step because PKL is rewriting the pk.bin OnExit.
# 2. Write down where the pk.bin file is located.
#     Usually its on c:\program files\bpk\pk.bin
#     Of corse you can copy the file at your favorite destination.
#     But dont forget to copy it back to the location if you set a new password ;)
# 3. Run this script over the pk.bin
#     See USAGE for more information about this step.
# 4. Enjoy to have back the control over your System :)

# [USAGE]
# ./pkl_tool.py (decrypt|encrypt) (/path/to/pk.bin) [new_password]
# Reallife examples:
#
# **On Linux:
# ./pkl_tool.py decrypt /home/jackd/pk.bin
#     - This will try to extract and decrypt the AdminPassword from your pk.bin.
# ./pkl_tool.py encrypt /home/jackd/pk.bin "I AM ADMIN"
#    - This will try to open the pk.bin file and change the password to "I AM ADMIN".
#
# **On Windows:
# c:\pythonpath\python.exe pkl_tool.py decrypt "c:\program files\bpk\pk.bin"
#     - This will try to extract and decrypt the AdminPassword from your pk.bin.
# c:\pythonpath\python.exe pkl_tool.py encrypt "c:\program files\bpk\pk.bin" "I AM ADMIN"
#    - This will try to open the pk.bin file and change the password to "I AM ADMIN".

import sys, os

def createTable():
    table = []
    table.append(0xA)
    table.append(0xB)
    table.append(0x8)
    table.append(0x9)
    table.append(0xE)
    table.append(0xF)
    table.append(0xC)
    table.append(0xD)
    table.append(0x2)
    table.append(0x3)
    table.append(0x0)
    table.append(0x1)
    table.append(0x6)
    table.append(0x7)
    table.append(0x4)
    table.append(0x5)
    for i in range(0, len(table)):
        table.append(table[i] + 0x10)    

    ret = {}
    num = 0
    for i in range(32, 63 +1):
        ret[chr(i)] = table[num] + 0x80
        num += 1

    num = 0
    for i in range(64, 95 +1):
        ret[chr(i)] = table[num] + 0xE0
        num += 1

    num = 0
    for i in range(96, 127 +1):
        ret[chr(i)] = table[num] + 0xC0
        num += 1

    return(ret)

table = createTable()

def Decrypt(Ascii):
    for char, value in table.items():
        if Ascii == value:
            return(char)
    print "Undecryptable Byte: %i" %(Ascii)
    return("?")

def Encrypt(Char):
    for char, value in table.items():
        if Char == char:
            return(chr(value))
    print "Uhmm! You have a strange Char in your Password! Aborting!"
    sys.exit(0)

def getFileObj(path):

    try:
        pkbin = open(path, "r+")
    except:
        print "Failed to open '%s'! Aborting." %path
        sys.exit(0)
    size = os.path.getsize(path)
    if size    != 4204:
        print "Your pkl.bin have an invalid filesize! The File should have 4204 bytes but have %i! Aborting." %size
        sys.exit(0)
    print "File seems to be OK."
    return(pkbin)

if len(sys.argv) >= 3:
    cmd = sys.argv[1]
    if cmd == "decrypt":
        path = sys.argv[2]
        print "Trying to open '%s' to extract and decrypt AdminPassword..." %path
        pkbin = getFileObj(path)
        pkbin.seek(1812)

        byte = ""
        pw   = ""
        while byte != 0xAA:
            byte = ord(pkbin.read(1))
            if byte != 0xAA:
                pw += Decrypt(byte)

        pkbin.close()

        if pw != "":
            print "Admin PW is: '%s'." %(pw)
        else:
            print "Password not found. However, it could mean that there is no Adminpassword set."

    elif cmd == "encrypt":
        path = sys.argv[2]
        newpw = ""        
        if len(sys.argv) == 4:
            newpw = sys.argv[3]
            if len(newpw) >= 84:
                print "Your password is too long! C'Mon choose a shorter password."
                sys.exit(0)
        else:
            print "Invalid count of params."
            print "If you want to set a new password you should provide one, shouldnt you? :)"
            sys.exit(0)
        print "Trying to open '%s' to write the AdminPassword '%s'..." %(path, newpw)
        pkbin = getFileObj(path)
        pkbin.seek(1812)
        pw = ""
        for char in newpw:
            pw += Encrypt(char)
        pw += chr(0xAA) * (84-len(pw))
        pkbin.write(pw)
        pkbin.close()
        print "Operation Done. The new password should be set!"
else:
    print "Invalid count of params!"
    print "Open this script with a Texteditor for more Details."
