#!/usr/bin/python
#Covered by GPL V2.0
#Coded by Carlos del Ojo Elias (deepbit@gmail.com)

from urlparse import *
from time import gmtime, strftime
import gzip
import StringIO
import string
import re
import sys
import logging
import threading
import time
import os
import sqPyfia
import copy
import htmlout
from Gazpacho import *

mutex=1
Semaphore_Mutex=threading.BoundedSemaphore(value=mutex)
#logging.basicConfig(level=logging.DEBUG,format='%(levelname)s ==> \t%(message)s')


class Attacker(threading.Thread):
	__reqs=[]
	__paths={}

	__sqlRESULTS=[]
	__sqlEnabled=False
	__sqlXMLres=[]
	__sqlAttacks=0

	__xssRESULTS=[]
	__xssEnabled=False
	__xssXMLres=[]
	__xssAttacks=0

	__Threads=1
	__Semaphore_Threads=None
	__threadList=[]

	__proxy=None

	def __init__ (self):
		threading.Thread.__init__(self)
		Attacker.__Semaphore_Threads=threading.BoundedSemaphore(value=Attacker.__Threads)

	@staticmethod
	def setProxy(str):
		Attacker.__proxy=str

	@staticmethod
	def setThreads(n):
		Attacker.__Threads=n
		Attacker.__Semaphore_Threads=threading.BoundedSemaphore(value=Attacker.__Threads)
	
	@staticmethod
	def getNumAttacks():
		return Attacker.__xssAttacks,Attacker.__sqlAttacks

	@staticmethod
	def resetCache(self):
		Semaphore_Mutex.acquire()
		Attacker.__paths={}
		Attacker.__reqs=[]
		Semaphore_Mutex.release()
		
	@staticmethod
	def clearCache():
		Attacker.__paths={}

	@staticmethod
	def addReq(req):
		if not (Attacker.__sqlEnabled or Attacker.__xssEnabled):
			return

		Semaphore_Mutex.acquire()
		
		if not Attacker.__paths.has_key(req.urlWithoutPath):
			Attacker.__paths[req.urlWithoutPath]={}
	
		if not Attacker.__paths[req.urlWithoutPath].has_key(req.urlWithoutVariables):
			Attacker.__paths[req.urlWithoutPath][req.urlWithoutVariables]=[]
	
	
		nomvars=req.variablesGET()+req.variablesPOST()
	
		if nomvars!=None and len(nomvars)>0:
			nomvars.sort()
	
			found=False
			for k in  Attacker.__paths[req.urlWithoutPath][req.urlWithoutVariables]:
				if k[0]==nomvars:
					found=True
	
			if found==False:
				Attacker.__paths[req.urlWithoutPath][req.urlWithoutVariables]+=[(nomvars,req)]
				Attacker.__reqs.append(req)

		Semaphore_Mutex.release()

	@staticmethod
	def getReq():
		Semaphore_Mutex.acquire()
		try:
			ret= Attacker.__reqs.pop(0)
		except:
			ret= None 

		Semaphore_Mutex.release()
		return ret

	def Joiner(self):
		while True:
			time.sleep(1)
			try:
				a=Attacker.__threadList.pop()
				a.join()
			except:
				pass
			
			



	def run(self):
		th=threading.Thread(target=self.Joiner, kwargs={})
		th.start()
		while True:
			a=self.getReq()
			while a:
				self.attack(a)
				a=self.getReq()
			time.sleep(1)

	def attack(self,req):
		req2=copy.deepcopy(req)

		req.setFollowLocation(True)
		if Attacker.__sqlEnabled:
			Attacker.__Semaphore_Threads.acquire()
			th=threading.Thread(target=self.attackSQPYFIA, kwargs={"req": req})
			th.start()
			Attacker.__threadList.append(th)
#			self.attackSQPYFIA(req)

		if Attacker.__xssEnabled:
			Attacker.__Semaphore_Threads.acquire()
			th=threading.Thread(target=self.attackGAZPACIO, kwargs={"req": req2})
			th.start()
			Attacker.__threadList.append(th)
#			self.attackGAZPACIO(req)
#		self.attackSHITSQL(req)

	def attackSHITSQL(req):
		pars=""
		pypars=""
		if req["Cookie"]:
			pars+=" -H \"Cookie: "+req["Cookie"]+"\""
			pypars+=" -c \"%s\"" % (req["Cookie"])

		print "Launching sqlibf"

		sqlout=""

		if req.method=="GET":
			sqlout=os.popen ("./sqlibf \"%s\" %s" % (req.completeUrl,pars) )
			sqlout=("#### ./sqlibf \"%s\" %s ####\r\n" % (req.completeUrl,pars)) + "".join(sqlout.readlines())
			pyfiaout=os.popen ("./sqPyfia.py %s  \"%s\"" % (pypars,req.completeUrl) )
			sqlout+="\r\n#### ./sqPyfia.py %s  \"%s\" #### \r\n%s" % (pypars,req.completeUrl,"".join(pyfiaout.readlines()) )
		else:
			sqlout=os.popen ("./sqlibf \"%s\" \"%s\" %s" % (req.completeUrl, req.getPostData(),pars) )
			sqlout=("#### ./sqlibf \"%s\" \"%s\" %s  ####\r\n" % (req.completeUrl, req.getPostData(),pars)) + "".join(sqlout.readlines())
			pyfiaout=os.popen ("./sqPyfia.py %s -d \"%s\"  \"%s\"" % (pypars,req.getPostData(),req.completeUrl) )
			sqlout+="\r\n#### ./sqPyfia.py %s -d \"%s\"  \"%s\" ####\r\n%s" % (pypars,req.getPostData(),req.completeUrl,"".join(pyfiaout.readlines()))


		f=open("/tmp/sql.out","a")
		f.write(sqlout)
		f.close()
		print "sqlibf ended"

############################################################################################################################
######################################## XSS OPS ###########################################################################
############################################################################################################################

	def attackGAZPACIO(self,req):
		if Attacker.__proxy:
			req.setProxy(Attacker.__proxy)

		Attacker.__xssAttacks+=1
		c=crossiter(req,"gp")
		try:
			c.launch()
	
			res=c.getRAWResults()
			xml=c.getXMLResults()
			if res:
				Attacker.__xssXMLres.append(xml.childNodes[0].childNodes[0])
				Attacker.__xssRESULTS.append([req.completeUrl,res])
	
		except Exception,a:
			print "Fallo en XSS, REQ=",str(req)
			print a

		Attacker.__xssAttacks-=1
		try:
			Attacker.__Semaphore_Threads.release()
		except:
			pass

	@staticmethod
	def getXssResults():
		res=Attacker.__xssRESULTS[:]
		Attacker.__xssRESULTS=[]
		return res

	@staticmethod
	def enableXSS(bool):
		Attacker.__xssEnabled=bool

		
		

	@staticmethod
	def getXMLXss():
		return Attacker.__xssXMLres
		

############################################################################################################################
######################################## SQL OPS ###########################################################################
############################################################################################################################

	def attackSQPYFIA(self,req):
		if Attacker.__proxy:
			req.setProxy(Attacker.__proxy)

		Attacker.__sqlAttacks+=1
		sq=sqPyfia.sqPyfia(req)
		sq.setThreaded(10)
		#ry:
		sq.launch()

		res=sq.getRAWResults()
		xml=sq.getXMLResults()

		if res:
			Semaphore_Mutex.acquire()
			Attacker.__sqlRESULTS.append(res)
			Attacker.__sqlXMLres.append(xml.childNodes[0].childNodes[0])
			Semaphore_Mutex.release()

		#except Exception,a:
	#		print "Fallo en SQL, REQ=",str(req)
	#		print a

		Attacker.__sqlAttacks-=1
		try:
			Attacker.__Semaphore_Threads.release()
		except:
			pass

	@staticmethod
	def getXMLSql():
		return Attacker.__sqlXMLres

	@staticmethod
	def getSqlResults():
		res=Attacker.__sqlRESULTS[:]
		Attacker.__sqlRESULTS=[]
		return res

	@staticmethod
	def enableSQL(bool):
		Attacker.__sqlEnabled=bool
