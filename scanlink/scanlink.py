import httplib,re,sys,optparse
def make_request(host,page):
	try :
		connection = httplib.HTTPConnection(host)
		connection.request("GET",page)
		r1 = connection.getresponse()
		if r1.status != 404:
			print "Trying :  "+ host + page , "-->", r1.status , r1.reason
		connection.close()
	except(),msg:
		print "Error ",msg
		pass
def main():
	usage = "Usage: %prog [Options]\nCoded by CKJ [at] HCE & VBF"
	parser = optparse.OptionParser(usage=usage, version="%prog 1.0")
	parser.add_option("-H","--host" , action="store",type = "string" ,dest="host", default="",help= "Host name")
	parser.add_option("-p","--path",action="store",type = "string" , dest="path",default="/", help="path")
	parser.add_option("-f","--file",action="store",type="string", dest="file",default="linkadmin.db",help="dictionary to bruteforce")
	options,args = parser.parse_args()
	if options.host =="" :
		parser.print_help()
		sys.exit(1)
	host = options.host.replace("http://","")
	path = options.path
	file = options.file
	f = open(sys.path[0]+"/"+file,"r")
	if path !="/":
		path = "/" + path
	print "Scanning ...."
	for line in f:
		page = path + line.strip()
		if re.match("^(.*)(.php|.asp|.aspx|.jsp|.py|.pl)$",line.strip()):

			make_request(host, page)
		else :
			make_request(host,page +"/")
	f.close()
	print "Done !"
if __name__=="__main__"	:
	main()
	