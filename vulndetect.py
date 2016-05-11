#!/usr/bin/python

# VulnDetector Version 0.0.1pa
# Author: Brad Cable
# License: GPL Version 2


## basic config - these need to be changed depending on the site to be scanned ##

site="http://www.site.com/"          # URL to tree/scan
domains=[".site.com",".site2.com"]   # whitelist of domains to scan, with a "." infront, it matches all subdomains as well
pagetype="php"                       # type of code used on the site being scanned ("php" or "asp")

# log locations, all logs are stored at [the current directory]/logs/LOGFILE
vulnlogfile="gfqlog"                 # file to log all detected vulnerabilities as they are encountered
urllogfile="gfqurllog"               # file to log all urls fetched as they are fetched
reportfile="gfqreport"               # at the end of the scan, the detected vulnerabilities are compiled into a neat list, and logged to this file
usecookies=True                      # whether or not to send a cookie header value each time (True or False)
cookies=""                           # if usecookies is True, then 

## end basic config ##





## advanced config - only change these if you know what you are doing, you really shouldn't need to touch these at all... ##

xssscan=True              # scan for XSS vulns (True or False)
sqliscan=True             # scan for SQLI vulns (True or False)

checklevel=1              # checklevel:
                          #   1 = Silent SQL, Silent XSS
                          #   2 = Silent SQL, Silent XSS when possible (semi-silent when not)
                          #   3 = BLAST THE SITE! (AKA, non Silent SQL, non Silent XSS, causes tons of MySQL Errors
                          #                        on the site and could possibly flood someone's admin email)

levels=7                  # levels deep to tree the site (I recommend 6-8; 6 is shorter, and fairly thorough, while 8 is just plain crazy long and a little too thorough)
ignore_subdomain=True     # ignore subdomains for HTTP Host field and other places (should leave as True)

scanlimit=5               # times to scan the same URL with different query strings,
                          # "bob.php?id=1" and "bob.php?id=2" count as two scans,
                          # and until scanlimit is hit, it will continue to check
                          # vulnerabilities on that URL

indent="     "            # indent used when displaying the results
ignorefileext="swf,fla,gif,jpeg,jpg,tiff,png,mng,pdf,dat,mpeg,mpg,mp2,mp3,wav,mod,mov,avi,asf,asx,ogg,asc,tgz,rpm,deb,gz,bz2,zip,rar,c,cpp,h,o,ko,py,so,torrent,js,css,msi,exe,bin,dmg,x86,ut4mod,wmv,rmvb,txt,n64,cbs,max,xps,xpi" # list of file extensions that shouldn't be downloaded and scanned 

randidentlen=6            # this is so internal, you shouldn't touch it whatsoever
decapitation=True         # this is so internal, you shouldn't touch it whatsoever

## end advanced config ##


########################################
###     DO NOT TOUCH THE REST!!!     ###
########################################

## setup ##

# import modules
import socket,sre,time,random

# debugging
from sys import exit # exit() for debug
# debug mode
from sys import argv
debug=False
if len(argv)>=2: debug=(argv[1]=="1")

# declare output variables
urlfields={}
postfields={}
treedurls={}
reportvar={}

# get comment type to use
if pagetype=="asp": comnt="%2d%2d"
elif pagetype=="php": comnt="/*"
else:
	print "Unknown Page Type: "+pagetype.upper()
	print "Using Default Database Comment: --"
	comnt="%2d%2d"

# get session stuff to use
sessstr="(?i)"
if pagetype=="asp": sessstr+="aspsessionid([a-z]{8})=([a-z]{8})"
elif pagetype=="php": sessstr+="phpsessid=([a-z0-9]{32})"
else:
	print "Unknown Page Type: "+pagetype.upper()
	sessstr+=pagetype+"sessid=([a-z0-9]{32})"
	print "Using Default Session Syntax: --"

# set up the ignore file extension variable to be useable
ignorefileext=","+ignorefileext+","

## end setup ##


## function declaration ##

# function to determine if a list object is empty in any way
def listempty(listarg): return (listarg==None or listarg==[] or type(listarg)!=type([]) or len(listarg)==0)

# function to edit files easily
def filestuff(fname,body="",fptype=False):

	if not fptype:
		if body=="": fptype="r"
		else: fptype="a"

	fp=open(fname,fptype)
	fp.write(str(body))
	fp.close()

# function to remove non unique items
def uniqlist(listarg):
	if type(listarg)!=type([]): return
	newlist=[]
	for i in range(len(listarg)):
		if newlist.count(listarg[i])==0: newlist[len(newlist):len(newlist)]=[listarg[i]]
	return newlist

# function to get the page name of a url
def pagename(url):
	if url[:7]=="http://": url=url[7:]
	slash=url.find("/")
	if slash!=-1: url=url[slash:]
	else: url="/"
	return url

# function to fix urls like "http://www.google.com" or "www.google.com" into "http://www.google.com/"
def urlfix(url):
	if url[:7]!="http://": url="http://"+url
	slash=url[7:].find("/")
	if slash==-1: url+="/"
	return url

# function to get the server name of a url
def servername(url,ig_subd=ignore_subdomain):
	url=urlfix(url)[7:]
	url=url[:url.find("/")]
# 	if ig_subd: url=sre.sub("^.*?([^\.]*\.[^\.]*)$","\\1",url)
	return url

def checkserver(server):
	global domains
	for domain in domains:
		if domain[:1]==".":
			if server[-len(domain)+1:]==domain[1:]: return True
		else:
			if server==domain: return True
	return False

# function to fix the headers so they don't contain %25's (%'s) or the xxploit code
def headerfupr(hdr,explt):
	hdr=hdr.replace("%25","%")
	hdr=hdr.replace(explt,"")
	return hdr

# function to remove urls from the body of a page
def removeurls(body): return sre.sub("http://([^ \"\']+)","",body)

# function to retreive the full path of a url based on the current page url
def fullpath(url,pageurl):

	if url.lower()[:7]=="http://": return url

	if pageurl.count("?")!=0: pageurl=pageurl[:pageurl.find("?")]

	if url.count("?")>0:
		if url[:1]=="?": return pageurl+url
		pageurl=pageurl[:pageurl.find("?")]

	#pageurl=pageurl[:pageurl.find("?")]

	pagedomain=pageurl[:pageurl[7:].find("/")+7]
	if url[:1]=="/": return pagedomain+url

	pagepath=pageurl[pageurl[7:].find("/")+7:]
	pagepath=pagepath[:pagepath.rfind("/")+1]
	path=pagepath+url
	path=sre.sub("\.\/","\/",path)
	path=sre.sub("\/([^\/]+)\/..\/","\/",path)

	return pagedomain+path

# function to get the value of HTML attribute before a ">"
def getattrval(body,attr):
	body=sre.sub("([^\>]*)\>([^\000]*)","\\1",body)
        if sre.search(attr+"=(\"|'|)([^\\1\ \>]*)\\1",body)!=None:
		delim=sre.sub("[^\>]* "+attr+"=(\"|'|)([^\\1\ \>]*)\\1([^\>]*)","\\1",body)
		exp="[^\>]* "+attr+"=(\\"+delim+")([^"
		if delim=="": exp+="\ "
		else: exp+=delim
		exp+="\>]*)\\"+delim+"([^\>]*)"
		return sre.sub(exp,"\\2",body)
	else: return ""

# function to retreive a page based on input
def getpage(url,dheaders=1,redir=0,realpage=0,poststring="",exceptions=0):

	# function to recurse and try getpage() again with new values
	def recurse(exceptions):

		sock.close()
		exceptions+=1

		if exceptions<=6: return getpage(url,dheaders,redir,realpage,poststring,exceptions)
		else:
			print "Too many recursions, skipping..."
			return


	global usecookies,urllogfile,debug,ignorefileext
	if not checkserver(servername(url)): return

	if url.find("#")!=-1: url=url[:url.find("#")]

	# file extensions that need to be ignored code
	fileext=sre.sub(".*(http\://[^/]*/).*","\\1",url)
	if url==fileext: fileext="None"
	else: fileext=sre.sub("^.*\/[^/]*\.([^\&\#\?\/]*)[^/]*$","\\1",url)
	if ignorefileext.count(","+fileext+",")!=0: return

	try:

		sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		sock.connect((servername(url,False),80))

		workurl=pagename(url)
		theurl=url
		if redir!=1: theurl=workurl

		qrytype="GET"
		if poststring!="": qrytype="POST"
		out=(qrytype+" "+theurl+" HTTP/1.1\n"
		     "Host: "+servername(url,False)+"\n"
		     "Connection: close\n")
		if usecookies:
			global cookies
			out+="Cookie: "+cookies+"\n"
		if poststring!="":
			out+="Content-Type: application/x-www-form-urlencoded\n"
			out+="Content-Length: "+str(len(poststring))
			out+="\n\n"+poststring+"\n"
		out+="\r\n\r\n"
		sock.send(out)

		# get response type and log the page
		response=sock.recv(12)[-3:]
		fp=open("logs/"+urllogfile,"a")
		fp.write(url+": "+response+" "+str(realpage)+"\n")
		if poststring!="": fp.write(indent+"POST: "+poststring+"\n")
		fp.close()


		# at 404 response, close connection and fail
		if response=="404" or response=="500":
			sock.close()
			return

		# at 30[1237] response types, recurse new page
		if sre.search("30[1237]",response):
			while 1:
				chunk=""
				byte=sock.recv(1)
				while byte!="\r":
					chunk+=byte
					byte=sock.recv(1)
				sock.recv(1)
				if chunk.lower()[:9]=="location:":
					location=chunk.lower()[9:].strip()
					if location=="http://"+servername(url,False)+url: location="/"
					locpage=fullpath(location,url)
					sock.close()
# 					if url[len(url)-2:]=="" and locpage[len(locpage)-4:]=="": break
					redir=1
					if locpage!=url:
						redir=0
						if pagename(sre.sub("\\\\(\"|\')","\\1",locpage))==pagename(url):
							print "QUOTE REDIR"
							return
					print "OLD:",url
					print "NEW:",chunk.lower()
					print "REDIR:",locpage
					return getpage(locpage,redir=redir,realpage=realpage)
			if realpage==1:
				sock.close()
				return

		elif realpage==1:
			sock.close()
			return url

		# get headers, ignoring certain HTTP headers
		headers=""
		type=0
		while 1:
			chunk=""
			byte=sock.recv(1)
			if byte=="\r":
				sock.recv(1)
				break
			while byte!="\r":
				chunk+=byte
				byte=sock.recv(1)
			sock.recv(1)

			if chunk.lower()[:11]!="set-cookie:" and chunk.lower()[:5]!="date:" and chunk.lower()[:15]!="content-length:" and chunk.lower()[:11]!="keep-alive:" and chunk.lower()[:18]!="transfer-encoding:" and chunk.lower()[:11]!="connection:":
				headers+=chunk

#			if chunk.lower()[:15]=="content-length:":
#				type=1
#				conlen=int(chunk[16:])

			if chunk.lower()[:26]=="transfer-encoding: chunked": type=2

		# no special type specified, just get the page
		if type==0:
			body=""
			while 1:
				chunk=sock.recv(200)
				body+=chunk
				if chunk=="": break


		# set it up if it does have a type
#		else:
#			byte=sock.recv(1)
#			if byte=="\r": sock.recv(1)
#			else:
#				while 1:
#					i=-1
#					while byte!="\r":
#						i+=1
#						byte=sock.recv(1)
#					nbytes=sock.recv(3)
#					if nbytes=="\n\r\n": break

#		# content-length
#		if type==1:
#			body=""
#			for i in range(conlen):
#				chunk=sock.recv(1)
#				body+=chunk

		# transfer-encoding: chunked
		if type==2:
			body=""
			chunksize=""
			while chunksize!=0:
				byte=""
				chunk=""
				while byte!="\r":
					chunk+=byte
					byte=sock.recv(1)
				sock.recv(1)
				chunksize=int(chunk,16)
				wchunksz=chunksize
				while wchunksz>=1:
					subchunk=sock.recv(wchunksz)
					body+=subchunk
					wchunksz-=len(subchunk)
				sock.recv(2)

		# clean up and return
		sock.close()
		if dheaders!=1: headers=""

		return [headers,body,urlfix(url)]

	# catch socket errors, such as "connection reset by peer" - trys again until it gives up and goes on to the next page
	except socket.error:
		print "Socket Error, Recursing..."
		return recurse(exceptions)

# function to remove everything in the "<head>" tag from a server response
def decapitate(body):

	if body==None: return

	global decapitation
	if decapitation==True: body=sre.sub("<head>(.+?)</head>","",body)

	return body


# function to generate a random identification string
def randident(thelen=randidentlen,randchars="Bghi3rj9uwEFabTGH1ImnL4xpCstUOvoPYk25qVJK8Z0Q67lWXefMRSDcdyzAN"):
# 	global randidentlen
	rndidnt=""
	while len(rndidnt)<thelen:
		random.seed(time.time())
		rand=random.random()
		rndidnt+=randchars[int(round(rand*(len(randchars)-1)))]
	return rndidnt

def randident_num(thelen=None):
	if not thelen:
		global randidentlen
		thelen=randidentlen
	return int(randident(thelen,"3490168257"))

# function to initiate a single exploit
def exploit(url,qry,namval,explt,post,poststring="",randstr=""):

	def removeexplt(body,explt):
	
		def removeit(body,explt): return body.replace(explt,"")
		remove=lambda:removeit(body,explt)

		try:
			explt=str(int(explt))
			body=sre.sub("(?<![0-9])"+explt+"(?![0-9])","",body)

		except ValueError:

			body=remove()
			explt=parsebody(explt)
			body=remove()
	
# 			if pagetype=="asp":
# 				explt=explt.replace("%2D","-")
# 				body=remove()
# 	
# 			explt=explt.replace("+"," ")
# 			body=remove()
# 	
# 			explt=explt.replace("%20"," ")
# 			body=remove()
# 	
# 			explt=explt.replace("%2b","+")
# 			body=remove()

# 		body=body.replace(explt.replace("+"," "),"")
# 			body=body.replace(explt.replace("%2D","-"),"")
# 			body=body.replace(explt.replace("+"," ").replace("%2D","-"),"")
		return body

	explt=str(explt)
	randstr=str(randstr)

	if randstr!="" and explt!=randstr: explt+=randstr # explt!=randstr possibly not needed

	expltqry=sre.sub(namval+"[^\&]*(?=\&|$)",namval+explt,qry)
	if not post: hab=getpage(url+expltqry,poststring=poststring)
	else: hab=getpage(url,poststring=expltqry)
	if listempty(hab): return

# 	headers=hab[0]
	body=hab[1]

	##### ? # sre for all this crap? #####
	if len(explt)>=4:
		body=removeexplt(body,explt)
		body=parsebody(body)
		body=removeexplt(body,explt)
	else: body=parsebody(body)
	if randstr!="": body=removeexplt(body,randstr)

	return body

# function to parse the body for checking agsinst others
def parsebody(body):

	global sessstr,pagetype

	body=body.replace("%2d","-")
	body=body.replace("%2D","-")
	body=body.replace("%25","%")
	body=body.replace("%20"," ")
	body=body.replace("+"," ")
	body=body.replace("%2b","+")
	body=body.replace("%2B","+")
	body=body.replace("%22","\"")
	body=body.replace("\\\"","\"")
	body=body.replace("\\'","'")
	body=body.replace("\n","")
	body=body.replace("\r","")
	body=sre.sub(sessstr,"",body)

	# These might cause problems
	body=sre.sub("\<script([^\>]*)\>(.*?)\</script\>","",body)
	body=sre.sub("\<!--(.*?)--\>","",body)

	if pagetype=="php":
		body=sre.sub("(?i)\<input type=\"hidden\" name=\"phpsessid\" value=\"([a-z0-9]{32})\"( /|)\>","",body)
	body=sre.sub(" alt=(\"|\')([^\\1\>]*)\\1","",body)
	body=removeurls(body)

	return body

# function to check a value for SQL Injection
def sqli_check(body,theurl,qry,namval,quot,post,poststring):
	if sqli_intcheck(body,theurl,qry,namval,post,poststring): return True
	if sqli_stringcheck(body,theurl,qry,namval,quot,post,poststring): return True
	return

# function to check an integer value for SQL Injection, this is a near 100% sure way to test integers for SQLI
def sqli_intcheck(body,theurl,qry,namval,post,poststring):

	name=namval[:namval.find("=")]
	rvalue=namval[namval.find("=")+1:]
	try: rvalue=int(rvalue)
	except ValueError: return # Not an integer, sorry :(

	while True:
		xtrm=randident_num(5)
		if rvalue!=xtrm: break
	bodyxtrm=exploit(theurl,qry,name+"=",xtrm,post,poststring,xtrm) # integer is random 5 characters, creating an "extreme" page to check against

	i_s=[0,4,6]
	i_s.sort()
	i_s.reverse()
	for i in i_s:
		if i==0:
			value=rvalue
			body=exploit(theurl,qry,name+"=",str(value-1)+"%2b1",post,poststring)
			if body!=bodyxtrm: break
			return

		value=randident_num(i)
		body=exploit(theurl,qry,name+"=",str(value-1)+"%2b1",post,poststring)
		if body!=bodyxtrm: break

	bodyplus=exploit(theurl,qry,name+"=",str(value-2)+"%2b2",post,poststring)

	filestuff("1",body,"w")
	filestuff("2",bodyplus,"w")
	filestuff("3",bodyxtrm,"w")

	# if the addition occurs and the extreme case is different, it's vulnerable
	if bodyplus==body and body!=bodyxtrm:
		print "INTEGER VULN:",theurl,namval
		return True
	return

# function to check a string value for SQL Injection, this is not as precise as the integer check, but it's still good
def sqli_stringcheck(body,theurl,qry,namval,quot,post,poststring):
	randstr=randident()
	bodyemp=exploit(theurl,qry,namval,quot+"+"+comnt,post,poststring)
	pbodyq=exploit(theurl,qry,namval,quot+"+"+comnt,post,poststring,randstr)
	if bodyemp!=pbodyq:
		randstr=""
		pbodyq=bodyemp

	firsttrue=True
	if body!=pbodyq:
		ordtest=pbodyq
		pbodyand=exploit(theurl,qry,namval,quot+"+and+1%3D1+"+comnt,post,poststring,randstr)
		if body!=pbodyand:
			ordtest=pbodyand
			pbodyord=exploit(theurl,qry,namval,quot+"+order+by+1+"+comnt,post,poststring,randstr)
			if body!=pbodyord:
				ordtest=pbodyord
				pbodynb=exploit(theurl,qry,namval,quot+"+and+"+quot+"1"+quot+"%3D"+quot+"1",post,poststring)
				if body!=pbodynb:
					firsttrue=False
	else:
		pbodyord=exploit(theurl,qry,namval,quot+"+order+by+1+"+comnt,post,poststring,randstr)
		if body!=pbodyord:
			ordtest=pbodyord
		else:
			pbodyand=exploit(theurl,qry,namval,quot+"+and+1%3D1+"+comnt,post,poststring,randstr)
			if body!=pbodyand:
				ordtest=pbodyand
			else:
				ordtest=body


	if firsttrue:
		nbodyrand=exploit(theurl,qry,namval,quot+"+"+randident(),post,poststring,randstr)
		if body!=nbodyrand and ordtest!=nbodyrand:
			nbodyq=exploit(theurl,qry,namval,"'\"",post,poststring,randstr)
			if body!=nbodyq and ordtest!=nbodyq:
				nbodyord=exploit(theurl,qry,namval,quot+"+order+by+999+"+comnt,post,poststring,randstr)
				if body!=nbodyord and ordtest!=nbodyord:
					print "STRING VULN:",theurl,namval
					return True

	return

#	nbodynb=exploit(theurl,qry,namval,quot+"+and+"+quot+"1"+quot+"%3D"+quot+"0",post,poststring)
#	if (body==pbodyq or body==pbodyand or body==pbodyord or body==pbodynb) and (body!=nbodyq and body!=nbodyord):

# function to fully exploit a url, and return the results
def fullxplt(worldbody,theurl,vars,qry,post,poststring=""):

	global pagetype,xssscan,sqliscan,checklevel

	sqlivulns=[]
	xssvulns=[]
	worldbody=decapitate(worldbody)

	for i in range(len(vars)):

		namval=vars[i]
		name=namval[:namval.find("=")]
# 		if name=="xss": return
		value=namval[namval.find("=")+1:]

		if pagetype=="php" and name.lower()=="phpsessid":
			continue

		# SQLI (SQL Injection) Vulnerability Checker
		if sqliscan:
			worldbody=parsebody(worldbody)
			if checklevel<=2:
				if sqli_intcheck(worldbody,theurl,qry,namval,post,poststring): sqlivulns.append(name)
			else:
				bodychk=decapitate(exploit(theurl,qry,namval,"'\"",post,poststring))
				if worldbody!=bodychk:
					if sqli_check(worldbody,theurl,qry,namval,"",post,poststring): sqlivulns.append(name)
					elif sqli_check(worldbody,theurl,qry,namval,"'",post,poststring): sqlivulns.append(name)
					elif sqli_check(worldbody,theurl,qry,namval,'"',post,poststring): sqlivulns.append(name)

		# XSS (Cross Site Scripting) Vulnerability Checker
		if xssscan:

			if checklevel<=2:
				try:
					value=int(value)
					xssplt=str(randident_num())
				except ValueError:
					if checklevel==1: continue
					xssplt=randident()

				xssplt+="<script>"

				if post==0: body=getpage(theurl+sre.sub(namval+"[^\&]*(?=\&|$)",namval+xssplt,qry),poststring=poststring)
				else: body=getpage(theurl,poststring=sre.sub(namval+"[^\&]*(?=\&|$)",namval+xssplt,qry))
				if not listempty(body):
					body=body[1]
					if body.count(xssplt)!=0:
						xssvulns.append(name)
						continue


			else:
				xssplt=randident()+"<d>"
				#xssplt=randident()+randident() # old method
				if post==0: body=getpage(theurl+sre.sub(namval+"[^\&]*(?=\&|$)",namval+xssplt,qry),poststring=poststring)
				else: body=getpage(theurl,poststring=sre.sub(namval+"[^\&]*(?=\&|$)",namval+xssplt,qry))
				if not listempty(body):
					body=body[1]
					if body.count(xssplt)!=0:
						xssvulns.append(name)
						continue
	
				xssplt=randident()+'"fg'
				if post==0: body=getpage(theurl+sre.sub(namval+"[^\&]*(?=\&|$)",namval+xssplt,qry),poststring=poststring)
				else: body=getpage(theurl,poststring=sre.sub(namval+"[^\&]*(?=\&|$)",namval+xssplt,qry))
				if not listempty(body):
					body=body[1]
					if body.count(xssplt)!=0:
						xssvulns.append(name)
						continue

	return [sqlivulns,xssvulns]

# function to prepare for fullxplt()
def checkvars(url,poststring=""):

	print "( __ )",url

	global pagetype,comnt
	post=0
	if poststring!="": post=1
	getvars=[]
	postvars=[]

	qloc=url.find("?")
	if qloc!=-1:
		theurl=url[:qloc]+"?"
		qry=url[qloc+1:].replace("&amp;","&")
		getvars=qry.split("&")
	elif post==0: return

	if post==1:
		postvars=poststring.split("&")
		hab=getpage(url,poststring)
	else: hab=getpage(url)

	print "PP"

	if listempty(hab): return

	getvars=uniqlist(getvars)
	postvars=uniqlist(postvars)

	worldbody=hab[1]
	getvulns=[]
	postvulns=[]

	print "QQ",getvars,postvars

	if not listempty(getvars): getvulns=fullxplt(worldbody,theurl,getvars,qry,0,poststring)
	if not listempty(postvars): postvulns=fullxplt(worldbody,url,postvars,poststring,1)

	print "ZAP!"

	if not listempty(getvulns): getvulns=[uniqlist(getvulns[0]),uniqlist(getvulns[1])]
	if not listempty(postvulns): postvulns=[uniqlist(postvulns[0]),uniqlist(postvulns[1])]

	return [hab[2],getvulns,postvulns]

# function to display the results of a single exploit, and record the results to the reportvar variable
def dispvulns(vulns,url):

	global indent,reportvar,vulnlogfile

	if url.find("?")!=-1: url=url[:url.find("?")]
	output=url+":"

	if not listempty(vulns):

		getvulns=vulns[1]
		postvulns=vulns[2]

		gvtest=not listempty(getvulns)
		if gvtest: gvtest=not listempty(getvulns[0]) or not listempty(getvulns[1])

		pvtest=not listempty(postvulns)
		if pvtest: pvtest=not listempty(postvulns[0]) or not listempty(postvulns[1])

		if gvtest or pvtest:

			output+="\n"

			if gvtest:
				getvulns[0].sort()
				getvulns[1].sort()
				output+=indent+"GET: "
				if not listempty(getvulns[0]):
					output+="SQLI - "+str(getvulns[0])
					if not listempty(getvulns[1]):
						output+=" | "
				if not listempty(getvulns[1]):
					output+="XSS - "+str(getvulns[1])
				output+="\n"

			if pvtest:
				postvulns[0].sort()
				postvulns[1].sort()
				output+=indent+"POST: "
				if not listempty(postvulns[0]):
					output+="SQLI - "+str(postvulns[0])
					if not listempty(postvulns[1]):
						output+=" | "
				if not listempty(postvulns[1]):
					output+="XSS - "+str(postvulns[1])
				output+="\n"

			output=output[:-1]

			# record results to the reportvar variable
			if reportvar.has_key(url):
				getlist=reportvar[url][0]
				if not listempty(getvulns):
					if listempty(getlist): getlist=getvulns
					else:

						if not listempty(getlist[0]):
							getlist[0][len(getlist[0]):len(getvulns[0])]=getvulns[0]
							getlist[0]=uniqlist(getlist[0])
						else: getlist[0]=getvulns[0]

						if not listempty(getlist[1]):
							getlist[1][len(getlist[1]):len(getvulns[1])]=getvulns[1]
							getlist[1]=uniqlist(getlist[1])
						else: getlist[1]=getvulns[1]

				postlist=reportvar[url][1]
				if not listempty(postvulns):
					if listempty(postlist): postlist=postvulns
					else:

						if not listempty(postlist[0]):
							postlist[0][len(postlist[0]):len(postvulns[0])]=postvulns[0]
							postlist[0]=uniqlist(postlist[0])
						else: postlist[0]=postvulns[0]

						if not listempty(postlist[1]):
							postlist[1][len(postlist[1]):len(postvulns[1])]=postvulns[1]
							postlist[1]=uniqlist(postlist[1])
						else: postlist[1]=postvulns[1]
			else:
				reportvar[url]=[getvulns,postvulns]
		else: return
	else: return

	filestuff("logs/"+vulnlogfile,output+"\n")
	print output

treeglob=1

# function to tree a site and initiate vulnerability checks on the pages found
def treepages(url,level):

	global treeglob,urlfields,postfields,treedurls,levels,server,vulnlogfile,scanlimit,ignorefileext
	print ">>>>>>>>",level,"<<<<<<<<"

	print " ---> "+url

	pageinfo=getpage(url)
	if listempty(pageinfo): return

	body=pageinfo[1].lower()

	print "AA"

	# select/option, textarea
	# check for forms
	bodyarr=sre.split("<form",body)
	for i in range(len(bodyarr)):

		frmsect=bodyarr[i][:bodyarr[i].find(">")]
		frmbody=bodyarr[i][bodyarr[i].find(">"):][:bodyarr[i].find("</form>")]

		actionurl=getattrval(frmsect,"action")
		if actionurl=="" or actionurl==frmsect or actionurl=="\"\"": actionurl=pageinfo[2]
		if actionurl.count(";")>0: actionurl=actionurl[actionurl.find(";")+1:]
		if actionurl[:11].lower()=="javascript:": continue
		actionurl=fullpath(actionurl,pageinfo[2])

		print "ACTION:",actionurl

		# get the input variables
		poststring=""
		inputarr=sre.sub("(.*?)\<input([^\>]*)\>(.*?)","\\2|ZZaaXXaaZZ|",frmbody).split("|ZZaaXXaaZZ|")
		for j in range(len(inputarr)):

			name=getattrval(inputarr[j],"name")
			if name==inputarr[j] or name=="" or name=="\"\"": continue

			value=getattrval(inputarr[j],"value")
			if value==inputarr[j] or value=="" or value=="\"\"": value=""

			if poststring!="": poststring+="&"
			poststring+=name+"="+value

		# get select/option tags
		selectarr=sre.sub("(.*?)\<select([^\>]*)\>(.*?)","\\2|ZZaaXXaaZZ|",frmbody).split("|ZZaaXXaaZZ|")
		for j in range(len(selectarr)):

			name=getattrval(selectarr[j],"name")
			if name==selectarr[j] or name=="" or name=="\"\"": continue

			value=sre.sub("(.*?)\<option([^\>]*)value=(\"|'|)([^\\3\ ]*)\\3([^\>]*)\>(.*?)","\\2",selectarr[j])
			if value==selectarr[j] or value=="" or value=="\"\"": value=""

			if poststring!="": poststring+="&"
			poststring+=name+"="+value
			print "sel/opt: "+name+"="+value

		if poststring=="": continue

		if sre.search("method=([\'\"]|)post([\'\"]|)",frmsect[:frmsect.find(">")].lower())==None:
			if actionurl.find("?")!=-1: actionurl+="&"
			else: actionurl+="?"
			actionurl+=poststring
			body+='<a href="'+actionurl+'">'
			print 'GETT <a href="'+actionurl+'">'
			continue

		# determine if it needs to be scanned, and if so, scan it
		postscan=0
		postvars=poststring.split("&")
		if postfields.has_key(actionurl):
			for j in range(len(postvars)):
				postvars[j]=postvars[j][:postvars[j].find("=")]
				if postfields[actionurl].count(postvars[j])==0:
					postfields[actionurl].append(postvars[j])
					postscan=1
		else:
			for j in range(len(postvars)): postvars[j]=postvars[j][:postvars[j].find("=")]
			postfields[actionurl]=postvars
			postscan=1

		if postscan==1:
			vulns=checkvars(actionurl,poststring)
			if not listempty(vulns): dispvulns(vulns,actionurl)

	print "BB"

	# check for urls in "href" tags
	# ? # part of 3? (src|href|location|window.open)= and http://
	urlreg="(\'|\")(?!javascript:)(([^\>]+?)(?!\.("+ignorefileext.replace(",","|")+"))(.{3,8}?)(|\?([^\>]+?)))"
	urlarr=sre.sub("(?s)(?i)(.+?)((src|href)=|location([\ ]*)=([\ ]*)|window\.open\()"+urlreg+"\\6","\\7|ZZaaXXaaZZ|",body).split("|ZZaaXXaaZZ|")
	del urlarr[len(urlarr)-1]
	urlarr.append(sre.sub("(?s)(?i)(.+?)(src|href)="+urlreg+"\\3","\\4|ZZaaXXaaZZ|",body).split("|ZZaaXXaaZZ|"))
	del urlarr[len(urlarr)-1]
	for i in range(len(urlarr)):

		theurl=fullpath(urlarr[i],pageinfo[2])
		if not checkserver(servername(theurl)): continue

		# determine if it needs scanned and/or treed, and if so, scan and/or tree it
		getscan=0
		if theurl.count("?")!=0:
			nqurl=theurl[:theurl.find("?")]
			query=theurl[theurl.find("?")+1:]
			query=sre.sub("\&amp\;","\&",query)
			qryvars=query.split("&")
			if urlfields.has_key(nqurl):
				for j in range(len(qryvars)):
					qryvars[j]=qryvars[j][:qryvars[j].find("=")]
					if urlfields[nqurl].count(qryvars[j])==0:
						urlfields[nqurl].append(qryvars[j])
						getscan=1
			else:
				for j in range(len(qryvars)): qryvars[j]=qryvars[j][:qryvars[j].find("=")]
				urlfields[nqurl]=qryvars
				getscan=1
		else:
			if urlfields.has_key(theurl)==False: urlfields[theurl]=[]
			nqurl=theurl

		if getscan==1:
			vulns=checkvars(theurl)
			if not listempty(vulns): dispvulns(vulns,theurl)
		tree=treeglob
		if treedurls.has_key(nqurl):
			if treedurls[nqurl].count(theurl)==0 and len(treedurls[nqurl])<=scanlimit:
				treedurls[nqurl].append(theurl)
			else: tree=0

		else: treedurls[nqurl]=[theurl]
		if tree==1 and level<levels:
			realurl=getpage(theurl,realpage=1)
			if theurl!=realurl and realurl!=None:
				body+=' href="'+realurl+'" '
			print "treeee"
			try: treepages(theurl,level+1)
			except KeyboardInterrupt:
				treeglob=0
				print "TREEGLOB CHANGED TO ZERO"
				treepages(theurl,level+1)


## end function declaration ##

## initialize the script ##

# setup
# server=servername(site)
starttime=time.time()
treedurls[site]=[site]

# url="http://www.omnipen.net/vuln.php?id=2&xss=1"
# domains=[".omnipen.net"]
# usecookies=False
#http://client.gamecenter.com/pages/gamespace/story.php?sid=6127385&pid=199212"
# exit()
# url="http://blogs.bnet.com/smallbusiness/index.php?p=21?tag=bnet.blogdoor" # diff tests
# url="http://blogs.bnet.com/"
#url="http://www.mp3.com/games/soundtrack.php?game_id=68" # NO
#url="http://www.mp3.com/faq/terms.php?tag=mp3.ft.no" # NO
#url="http://www.gamespot.com/cgi/gumclik.html?id=11917&s=6117511&p=5" # SQLI - id
#url="http://forums.gamespot.com/gamespot/report_abuse.php?message_id=202371898&topic_id=19054979&board_id=909100112" # SQLI - all 3
# print checkvars(url,"")
# print getpage(url)
# print treepages(url,0)
# print "FINAL QUIT"
# exit()

# initiate treeing, and handle keyboard interrupts
if debug: treepages(site,0)
else:
	try: treepages(site,0)
	except KeyboardInterrupt: print "\nKeyboard Interrupt, exiting..."

## end initialization ##


# get time elapsed, write it, and print it

endtime=time.time()
timeelapsed=endtime-starttime
timeout="Time Elapsed: "+str(timeelapsed)+" Seconds\n"

filestuff("logs/"+vulnlogfile,"\n"+timeout+"\n")

print timeout


## write report ##

urls=reportvar.keys()
urls.sort()
if not listempty(urls):

	fp=open("logs/"+reportfile,"w")

	for i in range(len(urls)):

		fp.write(urls[i]+":\n")
		reporturl=reportvar[urls[i]]
		if not listempty(reporturl):

			if not listempty(reporturl[0]):
				if not listempty(reporturl[0][0]) or not listempty(reporturl[0][1]):
					reporturl[0][0].sort()
					reporturl[0][1].sort()

					fp.write(indent+"GET: ")
					if not listempty(reporturl[0][0]):
						fp.write("SQLI - "+str(reporturl[0][0]))
						if not listempty(reporturl[0][1]):
							fp.write(" | ")
					if not listempty(reporturl[0][1]):
						fp.write("XSS - "+str(reporturl[0][1]))
					fp.write("\n")

			if not listempty(reporturl[1]):
				if not listempty(reporturl[1][0]) or not listempty(reporturl[1][1]):
					reporturl[1][0].sort()
					reporturl[1][1].sort()

					fp.write(indent+"POST: ")
					if not listempty(reporturl[1][0]):
						fp.write("SQLI - "+str(reporturl[1][0]))
						if not listempty(reporturl[1][1]):
							fp.write(" | ")
					if not listempty(reporturl[1][1]):
						fp.write("XSS - "+str(reporturl[1][1]))
					fp.write("\n")


			fp.write("\n")

	fp.write("\n"+timeout+"\n")

	fp.close()

print "Report Written: "+reportfile

## end write report ##

### END ###
