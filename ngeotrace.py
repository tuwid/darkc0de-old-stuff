#!/usr/bin/python 
##############################################################################
#                                                                            #
# PROGRAM: nGeoTrace	          	VERSION: 0.0.5 			     #
# AUTHOR: r3c0der54                   	DATE: 2009-10-17                     #
# LANGUAGE: Python                                                           #
# PLATFORM: Linux                                                            #
#                                                                            #
# r3c0der54[at]darkc0de[dot]com                                              #
#                                                                            #
##############################################################################
##############################################################################
#                                                                            #
# DESCRIPTION:                                                               #
# nGeoTrace  - 	fast traceroute tool showing IP adresses and geo             #
#		localisation information                                     #
#                                                                            #
# USAGE: 	python ngeotrace.py <ip-address> <network interface>         #
#                                                                            #
# REQUIRES:	itrace, python-geoip                                         #
#                                                                            #
##############################################################################
 
import sys, os, subprocess, traceback
import string, re 
import time 
import GeoIP
from optparse import OptionParser 

# --- GLOBAL APP VARS ---
APP_TITLE = "nGeoTrace"
APP_VERSION = "0.0.5"
APP_AUTHOR = "r3c0der54"
APP_USAGE = "usage: \n\nngeotrace.py <target domain or ip> <network interface>\n"
APP_EXAMPLE = "example: \n\nngeotrace.py www.google.com eth0"

############################################################################### 
# GEOTRACE FUNCTION                                                           #
############################################################################### 
def TraceTarget(target_ip,interface):
	results = execute_command(["itrace","-i",interface,"-d",target_ip])
	gi = GeoIP.open("/usr/local/share/GeoIP/GeoIPCity.dat",GeoIP.GEOIP_STANDARD)
	i = 0
    	for line in results: 
		if not line is "": 
			#print line
			lst = list(str(line).split())
			if not lst[1]=="Timeout":
				#remove "[" and "]" at start and end of the string
				i = i + 1				
				ipadr = str(str(lst[1]).replace("[","")).replace("]","")
				try: 				
					gir = gi.record_by_addr(ipadr)
					if gir != None:
						r = [i, ipadr, gir['country_code'], gir['city'], round(float(gir['latitude']),2), round(float(gir['longitude']),2)]
					else: 
						r = [i, ipadr, "N/A", "N/A", "N/A", "N/A"]
				except:
					r = [i, ipadr, "N/A", "N/A", "N/A", "N/A"]
				print str(r[0]).ljust(4)+str(r[1]).ljust(17)+str(r[2]).ljust(6)+str(r[3]).ljust(30)+str(r[4]).rjust(10)+str(r[5]).rjust(10)


############################################################################### 
#  PROCESS HANDLER                                                            #
############################################################################### 
def execute_command(command): 
	process = subprocess.Popen(command, stdout=subprocess.PIPE) 
	process.wait() 
    	lines =  process.stdout.read() 
    	return string.split(lines,"\n")


############################################################################### 
# MAIN ROUTINE                                                                #
############################################################################### 
if __name__ == "__main__": 
	global options, args 
	try: 
		start_time = time.time() 
          	os.system('clear') # clear terminal prompt
		if not os.geteuid()==0:
			print "[!] error: nGeoTrace needs to be run as root\n"
			sys.exit() 
          	parser = OptionParser() 
          	(options,args) = parser.parse_args() 
          	print APP_TITLE+" "+APP_VERSION+"\n"
	  	try: 
                	ip = args[0]
          	except IndexError: 
                  	print "[!] error: no target defined\n"
			print APP_USAGE
			print APP_EXAMPLE+"\n" 
                  	quit()
          	try: 
                  	iface = args[1]
          	except IndexError: 
                  	print "[!] error: no interface defined\n"
			print APP_USAGE
			print APP_EXAMPLE+"\n"  
                  	quit()
 
	  	print "[+] trace target: ", ip
	  	print "[+] interface:    ", iface
	  	print ""
	  	print "#   IP               CODE  CITY               	                LAT       LON" 
	  	try:
			TraceTarget(ip,iface)
		except:
			print "[!] error while tracing target" 
	  	time_needed = round((time.time() - start_time),3) 
	  	print "\n[+] trace completed in: ",time_needed, "sec." 
	  	print "" 
	  	quit()
     	except KeyboardInterrupt: 
          	pass 
