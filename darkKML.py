#!/usr/bin/python
#
# www.darkc0de.com
# code : low1z
# name : darkKML.py
# version : 0.3
#
# this script requires GeoIP
# LINUX ONLY
#
# change the installation path of geoip after installation

import socket, sys, urllib2
try:
        import GeoIP
except:
        print "\nGeoIP Module/Database NOT found, try:"
        print "sudo apt-get install libgeoip1 && sudo apt-get install python-geoip"
        print "or visit www[.]maxmind[.]com for download"
        print "GeoIP IS REQUIRED to run this Script!\n"
	sys.exit(1)	

geoDBpath = 'GeoLiteCity.dat'
verbose = True
wwwcheck = True

geostr = ['city',
          'region_name',
          'region',
          'area_code',
          'time_zone',
          'longitude',
          'latitude',
          'country_code',
          'country_name']

srviDicStr = ['Date:',
	      'Server:',
	      'Accept-Ranges:',
	      'Vary:',
	      'Content-Length',
	      'Connection:',
	      'Content-Type:',
	      'Expires:',
	      'Set-Cookie:',
	      'Transfer-Encoding:',
	      'Cache-Control:']

def ip2geo(ip):
	gi = GeoIP.open(geoDBpath,GeoIP.GEOIP_STANDARD)
	gs = gi.record_by_addr(ip)
	return gs

def srvinfo(url):
        global fpDate, fpServer, fpAR, fpV, fpCL, fpC, fpCT, fpExp, fpSC, fpTE, fpCC
        fpDate = 'n/a'; fpServer = 'n/a'; fpAR = 'n/a'; fpV = 'n/a'
        fpCL = 'n/a'; fpC = 'n/a'; fpCT = 'n/a'; fpExp = 'n/a'
        fpSC = 'n/a'; fpTE = 'n/a'; fpCC = 'n/a'
        try:
                req = urllib2.Request(url+'/')
                url_handle = urllib2.urlopen(req)
                UHi = url_handle.info()
                uhitmp = str(UHi).replace('\r','')
                uhi_ready = uhitmp.split('\n')
                for x in range(0, len(uhi_ready)):
                        if 'Date:' in uhi_ready[x]:  # uhhh this looks awful, will be nicer in the next version
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
                                fpTE = uhi_ready[x].split('Transfer-Encoding: ')[1]
                        if 'Cache-Control:' in uhi_ready[x]:
                                fpCC = uhi_ready[x].split('Cache-Control: ')[1]
        except:
                pass
        global srviDic
        srviDic = { 'Date:': fpDate,
                    'Server:': fpServer,
                    'Accept-Ranges:': fpAR,
                    'Vary:': fpV,
                    'Content-Length:': fpCL,
                    'Connection:': fpC,
                    'Content-Type:': fpCT,
                    'Expires:': fpExp,
                    'Set-Cookie:': fpSC,
                    'Transfer-Encoding:': fpTE,
                    'Cache-Control:': fpCC }

def pmEntry(ip):
	try:
		if ip.replace('.','').isdigit():
			singledataset = ip2geo(ip)
			url2ip = ip
		else:
			url2ip = socket.gethostbyname(ip)
			singledataset = ip2geo(socket.gethostbyname(url2ip))
		descstr = 'ip : '+url2ip+'\n'
		for entry in geostr:
			if entry == 'longitude' or entry == 'latitude':
				pass
			else:
				descstr += entry+' : '+str(singledataset[entry])+'\n'
		if wwwcheck == True:
	                srvinfo('http://'+ip)
			for entry in srviDicStr:
				if srviDic.get(entry) != 'n/a':
					descstr += str(entry)+' : '+str(srviDic.get(entry))+'\n'
		if verbose == True:
			print descstr

		fnp.write('<Placemark><name>'+str(ip)+'</name>'
                          '<description>'+descstr+'</description>'
                          '<Point><coordinates>'+str(singledataset['longitude'])+','+str(singledataset['latitude'])+'</coordinates>'
                          '</Point></Placemark>\n')
	except:
		pass

def createKML(iplist):
	fname = raw_input('KML Output Filename : ')
	if fname.endswith('.kml'):
		pass
	else:
		fname += '.kml'	
	global fnp
	fnp = open(fname, 'w')
	fnp.write('<?xml version="1.0" encoding="UTF-8"?>\n'
	   	  '<kml xmlns="http://www.opengis.net/kml/2.2"><Document>\n')
	for ip in iplist: 
		if ':' in ip:
			pmEntry(ip.split(':')[0])
		else:
			pmEntry(ip[:-1])
	fnp.write('</Document></kml>\n')
	fnp.close()

if len(sys.argv) <= 1:
        print "how about python darkKML.py list_with_urls_or_ips.txt ?"
        sys.exit(1)
try:
	iplist = open(sys.argv[1], 'r').readlines()
except:
	print "something wrong with the filename?"
	sys.exit(1)
createKML(iplist)
