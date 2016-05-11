#Covered by GPL V2.0
#Coded by Carlos del Ojo Elias (deepbit@gmail.com)

from console import *
import time
import attacker
from Proxynet import *
import sys
import crllr
import threading


class ProixConsole:
	def __init__(self):
		self.c=Console("ProxyStrike:$ ")
		self.c.addCommand(Command("help",self.CHelp))
		self.c.addCommand(Command("?",self.CHelp))
		self.c.addCommand(Command("quit",self.CQuit))
		self.c.addCommand(Command("config",self.CConfig))
		self.c.addCommand(Command("xss",self.CXss))
		self.c.addCommand(Command("sql",self.CSql))
		self.c.addCommand(Command("proxyport",self.CProxyport))
		self.c.addCommand(Command("threads",self.CThreads))
		self.c.addCommand(Command("rs",self.CResultsSQL))
		self.c.addCommand(Command("rx",self.CResultsXSS))
		self.c.addCommand(Command("a",self.CAttackProgress))
		self.c.addCommand(Command("save",self.CSave))

		self.xssResults=[]
		self.sqlResults=[]

		self.proxyport=8008
		self.xss=False
		self.sql=False
		self.threads=1

		self.exit=False
	
	def timer(self):
		while not self.exit:
			self.controller.timer()
			time.sleep(1)


	def run(self):
		self.banner()

		try:
			Proxynet.init("\.(js|jpg|gif|swf|ico|png|bmp|zip|rar|pdf|css|t?gz)$")
			self.at=attacker.Attacker()
			self.at.start()
			self.controller=crllr.Controller()
		except Exception,a:
			print "<<--Error-->>\r\n",a

		print "Listening in port 8008... \r\nNow you can connect you web browser to the proxy (localhost:8008)\r\n"
		timer=threading.Thread(target=self.timer, kwargs={})
		timer.start()

		self.c.init()
		self.exit=True

		timer.join()

		sys.exit(0)

	def CSave(self,args):
		if len(args)!=2:
			raise Exception,"Use: save sql/xss xml/html"
		atck=args[0].lower()
		output=args[1].lower()

		if atck not in ["sql","xss"] or output not in ["xml","html"]:
			raise Exception,"Use: save sql/xss xml/html"

		f=raw_input("Enter filename: ")

		if atck=="xss":
			self.CResultsXSS([])
		else:
			self.CResultsSQL([])

		if output=="xml":
			if atck=="xss":
				self.controller.saveXMLXss(f)
			else:
				self.controller.saveXMLSql(f)
		else:
			if atck=="xss":
				self.controller.saveHTMLXss(f)
			else:
				self.controller.saveHTMLSql(f)


		


	def CAttackProgress(self,args):
		x,s=self.controller.getNumAttacks()
		print "- %d threads doing XSS Attacks" % (x)
		print "- %d threads doing SQL Attacks" % (s)

	def CResultsSQL(self,args):
		self.sqlResults+=self.controller.getSqlResults()
		self.printSql()

	def CResultsXSS(self,args):
		self.xssResults+=self.controller.getXssResults()
		self.printXss()

	def CThreads(self,args):
		try:
			self.threads=int(args[0])
		except:
			print "[ Using %d threads for attacks ]" % (self.threads)
			return

		self.controller.changeReqThreads(self.threads)
		print "[ Using %d threads for attacks ]" % (self.threads)
		

	def CProxyport(self,args):
		try:
			port=int(args[0])
		except:
			print "[ Proxy listening in port %d ]" % (self.proxyport)
			return
			

		print "Stopping proxy..."
		Proxynet.stop()
		print "Proxy stopped"

		Proxynet.changePort(port)
		Proxynet.init("\.(js|jpg|gif|swf|ico|png|bmp|zip|rar|pdf|css|t?gz)$")
		print "[ Listening in port %s ]" % (port)
		self.proxyport=port

	def CXss (self,args):
		dicc={True: "on", False: "off"}
		self.xss=not self.xss
		print "[ Xss attacks are toggled",dicc[self.xss],"]"
		self.controller.xssToogled(self.xss)
		
	def CSql (self,args):
		dicc={True: "on", False: "off"}
		self.sql=not self.sql
		print "[ Sql attacks are toggled",dicc[self.sql],"]"
		self.controller.sqlToogled(self.sql)

	def CQuit(self,pars):
		raise EOFError

	def CConfig (self,pars):
		dicc={True: "on", False: "off"}
		print 
		print "\t--------- Config -----------"
		print "\t  Proxy port         = %d\r\n" % (self.proxyport)
		print "\t  XSS Attacks        = %s" % (dicc[self.xss])
		print "\t  SQL Attacks        = %s\r\n" % (dicc[self.sql])
		print "\t  Number of threads  = %s" % (self.threads)
		print "\t----------------------------"
		print 

		pass

	def printXss(self):
		for i in self.xssResults:
			print " - Url: ",i[0][:66]+"..."
			for j in i[1]:
				meth,var,str,shit=j[1:]
				print "\tVariable '%s' - Method %s" % (var,meth)
				str="\r\n\t\t - ".join(str)
				print "\t\tInjactable patterns:\r\n\t\t - %s" % (str)
			


	def printSql(self):
		for i in self.sqlResults:
			print " - Url: ",i[0][:66]+"..."
			for j in i[1]:
				var,meth,inj,db,err=j
				print "\tVariable '%s' - Method %s" % (var,meth)
				if inj:
					print "\t\tInjection type:",inj
				if db:
					print "\t\tDatabase fingerprint:",db
				if err:
					print "\t\tMessage error:",err
				print
			

	def CHelp (self,pars):
		print '''
ProxyStrike is a passive proxy to perform xss and sql attacks on web
applications, you only have to connect your web browser to ProxyStrike and
it automatically will attack the webs you are on.

Commands help
-------------

proxyport port     - Change port where proxy is listening
config             - Shows configuration

xss                - Toggle xss attacks
sql                - Toggle sql attacks

threads N          - Set number of treads

rs                 - Show SQL attack results
rx                 - Show XSS attack results
a                  - Show attack status

save [sql/xss] [html/xml] - Save results to a file
'''

	def banner(self):
		print '''-----------------------------------------------------
ProxyStrike v1.0 by Carlos del Ojo Elias
Mail: cdelojo@edge-security.com

Welcome to Proishenet console verison.

!!CAUTION!! Be careful using this software, you can attack and damage web
applications involuntarily.

This software was developed for audit purposes and distributed under GPL
license.

I WON'T TAKE RESPONSIBILITY FOR ITS MISUSE.

Type 'help' or '?' for help.
-----------------------------------------------------
'''

