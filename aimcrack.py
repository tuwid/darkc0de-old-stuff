##################  Instant Aim Hash Cracker  #############################
##################   Results Not Guarunted    #############################
################## Created by Corbin Schwartz #############################
##################  Feel free to distribute,  #############################
##################But leave this banner please#############################
###########################################################################
##################     A Few Comments         #############################
##########      Parsing the html took about 6        ######################
##########      hours to get right. I was trying     ######################
##########      everything from Beautiful Soup to    ######################
##########      complex functions etc. I stripped    ######################
##########     all of the unused (failed) attempts   ######################
##########           from this final file.           ######################
##########  You might want to comment _winreg out if ######################
##########    you aren't running Windows. Good luck! ######################
##########   I also commented the source for you.    ######################
###########################################################################
####### Created: late April 10th-Early (6am) April 11th 2007 ##############
###########################################################################
##################     Contact Information     ############################
########## email: coincorbin10 [at] gmail [dot] com  ######################
###########################################################################
########## This banner took 5 minutes to make too ;-)######################
###########################################################################
##### Shouts to Scouse (wherever you are), Ipp, MC Millan and Rowtary #####
###########################################################################


import hashlib, base64, binascii, socket, re, urllib2 #Obvious
#from _winreg import *          #comment this out if you aren't on Windows

def StripTags(text):            # This is what I usesd to strip <b> tags from the password to make it correct
    finished = 0                
    while not finished:         
        finished = 1            
                                # check if there is an open tag left
        start = text.find("<")
        if start >= 0:
            # if there is, check if the tag gets closed
            stop = text[start:].find(">")
            if stop >= 0:
                # if it does, strip it, and continue loop
                text = text[:start] + text[start+stop+1:]
                finished = 0
    return text

eord= raw_input("Are we cracking a hash or generating hashes today? (c/g/base64):").lower()  #What are we doing?

if eord == "c":                 #Then we CRACK!
    aom= raw_input("Is it an AIM Hash or an MD5 hash?").lower()
    if aom== 'aim':             #Then its an aim hash, surprise surprise
        provided=raw_input("Is the hash in the local PC registry or is it handy? (local/handy)").lower()
        if provided == "handy":
            a = base64.b64decode(raw_input("What is your Hash? \nEnter Here: "))                                    #asking for the hash and getting the base64 of it
            b = binascii.b2a_hex(a)                                                                                 #converting it to a egible format
            c= b[0:32]                                                                                              #takes the first half of b and there's the md5!
            url= "http://www.gdataonline.com/qkhash.php?mode=txt&hash=" + c                                         #Using gdata's great quickhash script for this
            def Parse(url):                                                                                         #You wouldn't believe how long it took me to get this right
                html = urllib2.urlopen(url).read()                                                                  #grabs the data from the page
                regex = re.compile("<b>.*[^<]<\/b>")                                                                #searches for anything in <b>
                myresult = regex.findall(html)                                                                      
                myresult = myresult[1]                                                                              #grabs the second string (the password)
                print "The password is: ", StripTags(myresult)                                                      #stripping the tags from it so you don't get <b>password</b>
            Parse(url)                                                                                              #do it
        elif provided == "local":
            screenname = raw_input( "Screen name? ")                                                                #setting the variable for the registry location later
            x= ConnectRegistry(None, HKEY_CURRENT_USER)                                                             #setting the stage for registry reading
            passkey = OpenKey(x, r"Software\America Online\AOL Instant Messenger (TM)\CurrentVersion\Users\\" + screenname + "\Login")      #opening the location of the key
            hash1= QueryValueEx(passkey, "Password1")                                                                                       #opening the key
            hash1= hash1[0]                                                                                         #cleaning the output
            print "AIM Hash: " ,hash1

            a = base64.b64decode(hash1)                                                                             #see above for everything until algorithm
            b = binascii.b2a_hex(a)
            c = b[0:32]
            print "AIM Hash in MD5: ",c
            url="http://www.gdataonline.com/qkhash.php?mode=txt&hash=" + c

            def Parse(url):
                html = urllib2.urlopen(url).read()
                regex = re.compile("<b>.*[^<]<\/b>")
                myresult = regex.findall(html)
                myresult = myresult[1]
                print "The password is: ", StripTags(myresult)
            Parse(url)
    elif aom=='md5':
        url="http://www.gdataonline.com/qkhash.php?mode=txt&hash=" + raw_input("md5?")
        def Parse(url):
            html = urllib2.urlopen(url).read()
            regex = re.compile("<b>.*[^<]<\/b>")
            myresult = regex.findall(html)
            myresult = myresult[1]
            print "The password is: ", StripTags(myresult)
        Parse(url)
elif eord == "g":
    algorithm= raw_input("What algorithm to hash with? \n (de)MD5, SHA1, SHA224, SHA256, SHA384, or SHA512: ").lower()  #what are we using?

    if algorithm=="md5":
        a= hashlib.md5(raw_input("String? :")).hexdigest()
        print a
    elif algorithm== "demd5":
        a = base64.b64decode(raw_input("What is your Hash? \nEnter Here: "))                                    #asking for the hash and getting the base64 of it
        b = binascii.b2a_hex(a)                                                                                 #converting it to a egible format
        c= b[0:32]
        print c
    elif algorithm=="sha1":
        a= hashlib.sha1(raw_input("String? :")).hexdigest()
        print a
    elif algorithm=="sha224":
        a= hashlib.sha224(raw_input("String? :")).hexdigest()
        print a
    elif algorithm=="sha256": 
        a= hashlib.sha256(raw_input("String :?")).hexdigest()
        print a
    elif algorithm=="sha384":
        a= hashlib.sha384(raw_input("String? :")).hexdigest()
        print a
    elif algorithm=="sha512":
        a= hashlib.sha512(raw_input("String? :")).hexdigest()
        print a

elif eord == "base64":
    todo=raw_input("Encoding Base64 or Decoding Base64? (e/d):").lower()
    if todo == "e":
        print base64.b64encode(raw_input("String? :"))
    elif todo == "d":
        print base64.b64decode(raw_input("What is your Hash? \nEnter Here: "))
