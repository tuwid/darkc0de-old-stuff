#!/usr/bin/python 
# low1z // forum.darkc0de.com // may09 
# Webserver Identification 
 
import urllib2, string, sys 
 
fpDate = 'n/a' 
fpServer = 'n/a' 
fpAR = 'n/a' 
fpV = 'n/a' 
fpCL = 'n/a' 
fpC = 'n/a' 
fpCT = 'n/a' 
fpExp = 'n/a' 
fpSC = 'n/a' 
fpTE = 'n/a' 
fpCC = 'n/a' 
 
def srvinfo(url): 
	global fpDate, fpServer, fpAR, fpV, fpCL, fpC, fpCT, fpExp, fpSC, fpTE, fpCC 
	req = urllib2.Request(url) 
	url_handle = urllib2.urlopen(req) 
	UHi = url_handle.info() 
 
	uhitmp = str(UHi).replace('\r','') 
	uhi_ready = uhitmp.split('\n') 
	for x in range(0, len(uhi_ready)): 
		if 'Date:' in uhi_ready[x]: 
			fpDate = uhi_ready[x].split('Date: ')[1] 
		if 'Server:' in uhi_ready[x]: 
			fpServer = uhi_ready[x].split('Server: ')[1] 
		if 'Accept-Ranges:' in uhi_ready[x]: 
			fpAR = uhi_ready[x].split('Accept-Ranges: ')[1] 
		if 'Vary:' in uhi_ready[x]: 
			fpV = uhi_ready[x].split('Vary: ')[1] 
		if 'Content-Length:' in uhi_ready[x]: 
			fpCL = uhi_ready[x].split('Content-Length: ')[1] 
		if 'Connection:' in uhi_ready[x]: 
			fpC = uhi_ready[x].split('Connection: ')[1] 
		if 'Content-Type:' in uhi_ready[x]: 
			fpCT = uhi_ready[x].split('Content-Type: ')[1] 
		if 'Expires:' in uhi_ready[x]: 
			fpExp = uhi_ready[x].split('Expires: ')[1] 
		if 'Set-Cookie:' in uhi_ready[x]: 
			fpSC = uhi_ready[x].split('Set-Cookie: ')[1] 
		if 'Transfer-Encoding:' in uhi_ready[x]: 
			fpTC = uhi_ready[x].split('Transfer-Encoding: ')[1] 
		if 'Cache-Control:' in uhi_ready[x]: 
			fpCC = uhi_ready[x].split('Cache-Control: ')[1] 
 
	srviDic = { 'Date:': fpDate, 
		    'Server:': fpServer, 
		    'Accept-Ranges:': fpAR, 
		    'Vary:': fpV, 
		    'Content-Lenght:': fpCL, 
		    'Connection:': fpC, 
		    'Content-Type:': fpCT, 
		    'Expires:': fpExp, 
		    'Set-Cookie:': fpSC, 
		    'Transfer-Encoding:': fpTE, 
		    'Cache-Control:': fpCC } 
	print "\n" 
	print url 
	print "\n" 
	for desc, value in srviDic.items(): 
		print desc, value 
 
if len(sys.argv) <= 1: 
	print "\n\nUniform Resource Locator bro... dont you get it?\n\n" 
        sys.exit(1) 
else: 
	usrurl = sys.argv[1] 
	if usrurl.startswith('http'): 
		srvinfo(usrurl) 
	else: 
		srvinfo('http://'+usrurl)
