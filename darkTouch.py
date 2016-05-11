#!/usr/bin/python
#
# website structure fingerprinting ...the dirty way
# thanks to baltazar/adminfinder for inspiration
#
# low1z // www.darkc0de.com

import urllib2, sys, httplib, threading, sets, socket, time, re

site = sys.argv[1].replace("http://","").split("/",1)[0] 
timeout = 2
socket.setdefaulttimeout(timeout)

threads = []
numthreads = 8
extensions = ['php','asp','aspx','cfm','html','htm']
tmptable = []
found = []
final = []
collected = []
ldm = 'apr-24-09'
version = '0.2'

fuzztable = ['index', 'Index', 'About', 'view', 'access', 'account', 'act_hit', 'activate', 'adclick', 
	     'add_channel', 'addfeed', 'addtestimonial', 'adentry', 'ad_link', 'admin', 'admin_upload', 'adn_count', 
	     'adverclick', 'affi', 'afgb', 'afi', 'agt', 'album', 'albums', 'animation', 'annonces-add', 'announce_detail', 
	     'announcement_content', 'apply', 'apricot', 'ARead', 'art', 'art_desc', 'article', 'article2', 'article_detail_parse', 
	     'ArticleInfo', 'article_read', 'Article_Show', 'article_show_full', 'article_view', 'ArticleView', 'author', 
	     'author_album', 'author_price', 'base', 'basket', 'batch', 'bbs', 'bbs_detail', 'bencandy', 'billboard01', 'b_link', 
	     'blog', 'blogdetails', 'blog-entry', 'bloggermeet', 'blog_groups', 'blogind', 'blog_show', 'blog_story', 'board', 
	     'board1', 'board_detail', 'book', 'bookmark', 'Books', 'browse', 'browse_image', 'BusinessReport', 
	     'button', 'camp_detail', 'candidatedetails', 'cardshow', 'catalog', 'categories', 'category', 'cfidata', 'channel', 
	     'Checkout', 'checkout_shipping', 'clanek_ukaz', 'clap', 'class_04', 'click', 'clickin', 'clickprod', 'CollectionList', 
	     'collegeprice', 'columns', 'comeoncool', 'comment', 'comments', 'Community', 'company', 'company_search', 'contact', 
	     'content', 'Content', 'content_new', 'contestant', 'control', 'coolfreelist', 'countblogstar', 'counter', 
	     'examine_list', 'external', 'ExtLink', 'faculty_profile', 'fair_homepage', 'faq', 'features_show2a', 'file', 'files', 
	     'films', 'form', 'formular', 'forum', 'forumdisplay', 'forumhome', 'forummessage', 'forum_messageDetail', 'forum_posts', 
	     'forum_sub_posts', 'frame', 'fullstory', 'gbook', 'get', 'getInPageTarget', 'GetRelease', 
	     'gocity', 'goodh', 'goods_comment', 'goout', 'goto', 'goto_freetel', 'gp_nl', 'graduate', 'group_page', 'group_topic', 
	     'guest', 'guestbook', 'guestbook_new', 'GuestMagBN', 'heihei', 'help', 'hitlink', 'home', 'hrbclick', 'iboard', 
	     'idevaffiliate', 'iframe', 'Image', 'img', 'include', 'index1', 'index2', 'index4', 'index_fo', 
	     'indexmain', 'indexnew', 'index_u', 'Individual', 'info', 'infoadd', 'infopage', 'infoshow2', 'insert_post', 
             'institutiondetail', 'international', 'into', 'invitation', 'inviteshow', 'isomil_valentine2_detail', 'item', 
	     'item_detail', 'item_groups', 'j140s', 'Job', '_jobposting', 'jobs', 'join', 
	     'newsmain', 'news_show', 'news_view', 'newthread', 'noscript', 'noticedet', 'notify', 'ocean-tracking', 'ocitview', 
	     'offices-ser_news', 'OpenAd', 'optionmmi', 'original_index', 'out', 'page', 'pages', 
	     'page-sanmin2', 'pageShw', 'parking', 'partydetails', 'permalink', 'PersonalSpace', 'plan', 'play', 'Play', 'player', 
	     'pleasure', 'plugin', 'plugins', 'point', 'poll', 'pollbooth', 
	     'pollsshow', 'post', 'postcard', 'posting', 'price', 'PriceList', 'print',
	     'pro_def', 'product', 'product_detail', 'ProductDetails', 'product_info', 'products', 'profile', 
             'profilesdetail', 'programimglist', 'projectdetails', 'projects', 'providepassword', 'psview', 
	     'publicrelationView', 'publisher_titles', 'pub-stats', 'qk_qklx', 'qoblog', 'quickadd', 'quotations', 'rank', 'ranking', 
	     'ranklink', 'read', 'readarticle', 'ReadNews', 'read_user', 'recruit', 'redir', 'redirect', 
	     'regdom', 'regist', 'register', 'report_get', 'req', 'RequestQuote', 'Results', 'ribbon_link', 'rin', 'rsd', 'rss', 
	     'rssFeed_it', 'rwcomments', 'sch', 'schedule', 'scielo', 'search', 'Search', 'search2', 
	     'search_form', 'searchpicsnap', 'searchresults', 'selectintro', 'select_tokucho', 'sendemail', 'sendmessage', 'serve', 
	     'shop', 'shop_fair', 'shopper_new', 'shopping_cart', 'show', 'ShowArtiChannel', 'showarticle', 
	     'showblog', 'showcard', 'showclass', 'showhistory', 'show_miniworld', 'shownews', 'showNews', 'ShowNewsDetail', 
	     'show_oc', 'showpage', 'show_photo', 'showpkn', 'showpost', 'showprofile', 'showquestion', 'showsp', 'showstats', 
	     'showthread', 'showtrackback', 'show_want', 'signup', 'single', 'site', 'sitecome', 'smsmain', 
	     'snapshots', 'soft_detail', 'sondages', 'sort', 'source', 'space', 'spacecp', 'special', 'specials', 
	     'spip', 'spurl', 'start', 'stat', 'statistics', 'statistik', 'stats', 'sub', 'subcate_list', 'subforum', 
	     'submit', 'subscribe', 'subscription', 'support', 'survey', 'tags', 'takeinfo_more', 'tana', 'task', 'tbh_sub', 
	     'tblogread', 'tchinfo', 'teacher', 'tech_details', 'tenders', 'terms', 'T_examinat', 'thread', 'thumbnails', 'tier', 
	     'top', 'topic', 'topicdetail', 'topics', 'topsites', 'tradeinfo', 'training', 'transfer', 'trip_detail',
	     'trpSupport', 'tr_set', 'tryout_item', 'two', 'type', 'Type', 'ucp', 'user', 
	     'User', 'userblog', 'userinfo', 'user_profile', 'user_register', 'usersettings', 
	     'user_view', 'vanessa_video', 'vbimghost', 'video', 'videoByTag', 'videos', 'View', 'viewad', 
	     'viewall', 'view_all_gallery', 'view_clip', 'viewdoc', 'viewEvent', 'viewfaculty', 
	     'viewforum', 'viewinfo', 'view_inside', 'ViewItem', 'viewmessage', 'viewnews', 'view_news', 'ViewNews', 'viewphotos', 
	     'viewpro', 'viewscat', 'viewstory', 'viewthread', 'viewtop', 'viewtopic', 'viewuser', 'view_video', 'viewwz', 
	     'VIP_showLawyer_article', 'visit', 'vote', 'votealbum', 'voteArticle', 'wall', 'webarticle', 'webarticle2', 'webboard', 
	     'webcounter', 'websearch', 'weekend_news_detail', 'welcome', 'wenji', 'whoischeck', 'worldwide', 'wp-login', 
	     'wp-profile1', 'xiti', 'zoom']

def pContent(url):
        try:
                request_web = urllib2.Request(url);agent = 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6)'
                request_web.add_header('User-Agent', agent);opener_web = urllib2.build_opener()
                text = opener_web.open(request_web).read();strreg = re.compile('(?<=href=")(.*?)(?=")')
                names = strreg.findall(text);opener_web.close()
                for name in names:
			if site in name or '=' in name or name.startswith('/'):
				global collected
				collected.append(name)
			elif site in name and EXT in name:
				collected.append(name)
			elif 'http://' in name:
				collected.append(name)
	except:
		pass
def Fuzz(entry):
	try:
		entry = "/" + entry
		connection = httplib.HTTPConnection(site)
		connection.request("GET",entry)
		response = connection.getresponse()
		if response.status == 200:
			str = 'http://'+site+entry
			print "Found : %s " % (str)
			found.append(str)
		else:
			pass
	except(KeyboardInterrupt,SystemExit):
			raise
	except:
			pass	

cnt = 1
print "   _         _   _____             _ "
print " _| |___ ___| |_|_   _|___ _ _ ___| |_   author : low1z"
print "| . | .'|  _| '_| | | | . | | |  _|   |    date :",ldm
print "|___|__,|_| |_,_| |_| |___|___|___|_|_| version :",version
print "\n Website Structure Fingerprinting *beta*"
print "- keep in mind, we only collect = links here -\n"
for val in extensions: print cnt,":", val;cnt += 1
EXTnr = raw_input('\nChoose Server FileExtension [1-5]:')
EXT = extensions[int(EXTnr)-1]

for entry in fuzztable:
	tmptable.append(entry+'.'+EXT)
print "\n>> Fuzzing for ."+EXT+" Files....\n"
for entry in tmptable: Fuzz(entry)
for entry in found: pContent(entry)	

for entry in collected:
	if entry.startswith('/') and EXT in entry and '=' in entry:
		final.append('http://'+site+entry)
	elif entry.startswith('http://') and site in entry and EXT in entry:
		final.append(entry)
	else:
		pass

if len(final) > 2:
	final.sort();lastEntry = final[-1]
	for e in range(len(final)-2, -1, -1):
		try:
	        	LE = lastEntry.split('?')
	                fURLS = final[e].split('?')
			if LE[0] == fURLS[0]:
	        		del final[e]
		        else:
	        		lastEntry = final[e]
	        except(IndexError):
			pass

print "\n>> Found :", len(final), "Strings\n"
for entry in final:
	print entry
