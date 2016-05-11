#!/usr/bin/python 
#Attempts to crack MySQL323 hash using wordlist. 
#http://darkc0de.com/ 
#d3hydr8[at]gmail[dot]com 
#rsauron[at]gmail[dot]com 
 
import sys 
 
def mysql323(clear): 
    # Taken almost verbatim from mysql's source 
    nr = 1345345333 
    add = 7 
    nr2 = 0x12345671 
    retval = "" 
    for c in clear: 
	if c == ' ' or c == '\t': 
	    continue 
	tmp = ord(c) 
	nr ^= (((nr & 63) + add) * tmp) + (nr << 8) 
	nr2 += (nr2 << 8) ^ nr 
	add += tmp 
    res1 = nr & ((1 << 31) - 1) 
    res2 = nr2 & ((1 << 31) - 1) 
    return "%08lx%08lx" % (res1, res2) 
 
if len(sys.argv) != 3: 
	print "Usage: ./mysql323crack.py <hash> <wordlist>" 
	sys.exit(1) 
 
pw = sys.argv[1] 
if len(pw) != 16: 
	print "Improper hash length\n" 
  	sys.exit(1) 
try: 
  	words = open(sys.argv[2], "r") 
except(IOError): 
  	print "Error: Check your wordlist path\n" 
  	sys.exit(1) 
words = words.readlines() 
print "\nWords Loaded:",len(words) 
for word in words: 
	word = word.rstrip("\n") 
	if pw == mysql323(word): 
		print "\nPassword is:",word 

