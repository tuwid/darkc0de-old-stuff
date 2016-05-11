# Wordlist Muncher: wMunch.Py
# by rattle//awarenetwork//org
# munches a bunch of wordlists into one big wordlist.

from os import listdir,sep
import sys

accept = "abcdefghijklmnopqrstuvwxyz0123456789!\"$%&/()=?*'_:;><,.-#+|~\\}][{"
isword = lambda s: reduce(lambda x,i: x and i in accept, s, True)
hashes = {}

def readWord(s):
	s = s.strip().lower()
	if isword(s):
		h = hash(s)
		if not hashes.has_key(h): hashes[h] = [s,]
		elif not s in  hashes[h]: hashes[h].append(s)

def readFile(path):
	for line in open(path,"r"): readWord(line.strip())

if len(sys.argv) < 2: 
	print "$ python %s <dir> <out>" % sys.argv[0]
	print "  where: <dir> is a directory with wordlists"
	print "         <out> is the output file."
	sys.exit(1)
else:
	print "[+] beginning to munch files from '%s' ..." % sys.argv[1]

for t in listdir(sys.argv[1]):
	try: readFile(sys.argv[1]+sep+t)
	except: pass
	else: print "[+] munched file: '%s'" % t

print "[+] generating unsorted output ...",
o = open(sys.argv[2],"w")
for v in hashes.values():
	for s in v: o.write(s+"\n")
o.close()
del hashes

print "done.\n[+] reading output back in ...",
words = open(sys.argv[2],"r").readlines()

print "done.\n[+] sorting words ...",
words.sort()

print "done.\n[+] writing sorted output ...",
open(sys.argv[2],"w").writelines(words)

print "done, all done!"


