#!/usr/bin/python
# md5 MySQL Database BruteForce AllinOne python v 1.1
# python by low1z feb2009
# idea & php design froz3n @ darkc0de
# special thanks to d3hydr8 from darkc0de for inspiring me to learn python
#
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import MySQLdb, sys, re, md5, time

host	 = 'YOUR-MYSQLSERVER-IP-HERE'
username = 'YOUR-MYSQLUSERNAME-HERE'
password = 'YOUR-MYSQLPASSWD-HERE'
dbname   = 'md5db'

onloadDBstatus = 0
version = '1.1_feb09'

db = MySQLdb.connect(host=host, user=username, passwd=password)

def dbconnect():
	csr = db.cursor()
	return(csr)

def timer():
	now = time.localtime(time.time())
	return time.asctime(now)

def setupdb():
	csr = dbconnect()
	try:
		csr.execute("CREATE DATABASE "+dbname)
		print "Database:", dbname, "created"
	except MySQLdb.Error, e:
		print "Error %s" % (e.args[1])
		sys.exit(1)
	try:
		csr.execute("CREATE TABLE "+dbname+".data (id INT( 255 ) NOT NULL AUTO_INCREMENT ,plain TEXT NOT NULL ,md5 VARCHAR( 255 ) NOT NULL ,PRIMARY KEY ( id ) , UNIQUE ( md5 )) ENGINE = MYISAM;")
		print "Tables in db:", dbname, "created, Database ready to use!"
	except MySQLdb.Error, e:
		print "Error %s" % (e.args[1])		
		sys.exit(1)

def insertwl():
	counter = 0
	try:
		words = open(wordlist, "r")
	except(IOError):
		print "Error: check", wordlist
		sys.exit(1)
	dupes = 0
	print "Inserting Wordlist, Skipping Dupes....may take ages"
	print "\nStart :", timer()
	for word in words.read().split('\n'):
		hash = md5.new(word).hexdigest()
		counter = counter+1
		try:
			csr = dbconnect()
			csr.execute("INSERT INTO "+dbname+".data (plain, md5)VALUES ('"+str(word)+"', '"+str(hash)+"');")
		except MySQLdb.Error, e:
			dupes = dupes+1	
	print "\nDupes :", dupes
	print "\nDone  :", timer()

def statusdb():
	try:
		csr = dbconnect()
		csr.execute("SELECT COUNT(id) AS num FROM "+dbname+".data")
		dbcount = csr.fetchone()
		return dbcount[0]
		csr.close()
	except MySQLdb.Error, e:
		print "Error %s" % (e.args[1])
		sys.exit(1)

def dropdb():
	csr = dbconnect()
	try:
		csr.execute("DROP DATABASE "+dbname)
		print "Database:", dbname, "deleted"
	except MySQLdb.Error, e:
		print "Error %s" % (e.args[1])
		sys.exit(1)	

def single(sshash):
	csr = dbconnect ()
	csr.execute("SELECT plain FROM "+dbname+".data WHERE md5 = '"+sshash+"'")	
	dset = csr.fetchone()
	if dset == None:
		print sshash, " : ", "not in DB"
	else:
		print sshash, " : ", dset[0]
	csr.close()

def multi():
	try:
		sshashs = open(md5file, "r").readlines()
		for sshash in sshashs:
			sshash = sshash.replace("\n","")
			single(sshash)
	except(IOError):
		print "Check your Filepath!!\n"

def helpme():
	print "HELP - Args\n"
	print " -h / -help      |   bring up this screen"
	print " -s / -setupdb   |   initial db installation"
	print " -w / -wordlist  |   insert wordlist into db eg. -w <wordlist.txt>"
	print " -d / -dropdb    |   delete database"
	print " -ss / -single   |   search db for given hash eg. >python md5db.py -ss <hash>"
	print " -ms / - multi   |   takes a list of md5's for cracking eg. >python md5db -ms <hashfile>"
	print " -c / -count     |   count database entries\n"
print "                 _ ___     _ _     "
print "        _ __  __| | __| __| | |__  "
print "       | '  \/ _` |__ \/ _` | '_ \ "
print "       |_|_|_\__,_|___/\__,_|_.__/ "                      
print "+--------------------------------------+"
print "| + Python/MySQL Bruteforce AllinOne + |"
print "| 				       |"
print "| + md5db11.py", version, "              |"
print "| + php & concept by froz3n            |"
print "| + python by low1z         	       |"
print "| 				       |"
print "| + use -h for help		       |"
print "+--------------------------------------+\n"
if onloadDBstatus == 1:
	try:
		print "\t",statusdb(), " Sets in DB\n"
	except MySQLdb.Error, e:
		print "Error, Database is not in place, use -s option to create it"
if len(sys.argv) <= 1:
	print "\tuse -help to get options\n"
	sys.exit(1)
for arg in sys.argv[1:]:
	if arg.lower() == "-h" or arg.lower() == "-help":
		helpme()
	if arg.lower() == "-s" or arg.lower() == "-setupdb":
		setupdb()
	if arg.lower() == "-d" or arg.lower() == "-dropdb":
		dropdb()
	if arg.lower() == "-c" or arg.lower() == "-count":
		print "\t",statusdb(), " Sets in DB\n"
	if arg.lower() == "-ss" or arg.lower() == "single":
		try:
			sshash = sys.argv[2]
			if len(sshash) != 32:
				print "invalid md5 supplied, check your input!\n"
				sys.exit(1)
			single(sshash)
		except(IndexError):
			print "Error: check hash ...\n"
	if arg.lower() == "-w" or arg.lower() == "-wordlist":
		try:
			wordlist = sys.argv[2]
			insertwl()
		except(IndexError):
			print "Error: check wordlist file\n"
	if arg.lower() == "-ms" or arg.lower() == "-multi":
		try:
			md5file = sys.argv[2]
			multi()
		except(IndexError):
			print "Error: check md5 plain import file...\n"
