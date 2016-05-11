#!/usr/bin/python 
# 
# insidepro md5 collector 
# low1z // forum.darkc0de.com 
# 
# this script is more like a generic downloader, using d3hydr8's pywget function to 
# get a list of files from a location like www.xyt.com/download.php?id=NUMBER 
# scripts asks for start & end numbers, to download from -> to. all downloaded files 
# will be parsed + combined into a single file. only simple checks, split by ':', check 
# if first value has a length of 32 (md5) then takes the second value as the password. 
# 
# note: its a good thing providing a md5 database for download 
 
import sys, urllib2, shutil, os 
 
newfilelist = [] 
dlurl = 'http://forum.insidepro.com/download.php?id=' 
 
 
def getFile(link): 
	try: 
		source = urllib2.urlopen(link) 
	except(urllib2.HTTPError),msg: 
		print "\nError:",msg 
		sys.exit() 
	num = 1 
	file = 'tmp_insidepropw_'+link.split('=')[1]+'.txt' 
	while os.path.isfile(file) == True: 
		file = link.rsplit("/",1)[1]+"."+str(num) 
		num+=1 
	try: 
		shutil.copyfileobj(source, open(file, "w+")) 
	except(IOError): 
		print "\nCannot write to `"+file+"' (Permission denied)." 
		sys.exit(1) 
	print "File downloaded", file 
	newfilelist.append(file) 
 
start = raw_input('Start : ') 
end = raw_input('End :') 
 
for x in range(int(start),int(end)): 
	getFile(dlurl+str(x)) 
 
print len(newfilelist), "Files downloaded, now combining Files" 
bigfile = raw_input('Filename : ') 
bfp = open(bigfile, "w") 
 
for entry in newfilelist: 
	tmp_open = open(entry, "r").readlines() 
	for entry in tmp_open: 
		tmp_e = entry.split(':') 
		if len(tmp_e[0]) == 32: 
			try: 
				if len(tmp_e[1]) != 32: bfp.write(tmp_e[1]) 
			except: 
				pass 
 
for entry in newfilelist: 
	os.remove(entry) 

