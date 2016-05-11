#!/usr/bin/python
#Covered by GPL V2.0
#Coded by Carlos del Ojo Elias (deepbit@gmail.com)

# This is a port of sqlibf to python, # sqlibf is a SQL injection 
# tool that was coded by Ramon Pinuaga (www.open-labs.org)


import time
import getopt
import tests
import urllib

from reqresp import *
from misc import *
from injection import *
from sqResult import *
import sys
import logging
import copy
import threading

from xml.dom.minidom import Document


#logging.basicConfig(level=logging.DEBUG,format='%(levelname)s ==> \t%(message)s')

class DynamicAbs:
	def __init__(self,var,method,req):
		self.__var=var
		self.__method=method
		self.__req=req

	def getReq(self):
		return self.__req

	def getVar(self):
		return self.__var

	def getMethod(self):
		return self.__method

	def equal(self):
		pass

	def getInfo(OrigResponse,BadResponse):
		pass

class DynamicErrWord(DynamicAbs):
	def __init__(self,var,method,req):
		DynamicAbs.__init__(self,var,method,req)
		self.word=None

	def addOrigResponse (self,OrigResponse):
		self.origWords=getRESPONSEMd5(OrigResponse)

	def getInfo(self,BadResponse):
		newWords=getRESPONSEMd5(BadResponse)

		logging.debug("\tequal Response - Orig: %s, Current: %s" % (self.origWords,newWords))
		if newWords!=self.origWords:
			return True

		
		return False

	def equalResponse(self,Response):
		return not self.getInfo(Response)

		Words=getResponseWords(Response)

		if not self.word in Words:
			return False
		return True
		



class sqPyfia:

	def __init__(self,req):
		self.req=req
		self.MD5Orig=""
		self.origWords=False

		self.dynamics=[]
		self.injResults=[]
		self.fingerResults=[]

		self.threads=1
		self.threaded=False
		self.semMUTEX=threading.BoundedSemaphore(value=1)


	def setThreaded(self,THREADS):
		self.threaded=True
		self.nthreads=THREADS
		self.semTHREADS=threading.BoundedSemaphore(value=THREADS)
		

	def stability (self):              ### Comprueba la estabilidad de la URL y establece el MD5 de la response Original
		self.req.perform()
		logging.debug("Stab 1 - DONE")
	
		resp1=self.req.response
		time.sleep(1.5)
		self.req.perform()
		logging.debug("Stab 2 - DONE")
		resp2=self.req.response
	
		if getRESPONSEMd5(resp1)!=getRESPONSEMd5(resp2):
			logging.debug("Stability FAILED - "+str(self.req))
			return False

		self.origResponse=resp1
		logging.debug("URL is STABLE")
		return True

	def dynamism (self):
		for i in self.req.variablesGET():
			self.tryDynamic(i,"GET",self.req)

		for i in self.req.variablesPOST():
			self.tryDynamic(i,"POST",self.req)

	def THDynamism(self):
		threadList=[]

		for i in self.req.variablesGET():
			self.semTHREADS.acquire()
			th=threading.Thread(target=self.tryDynamic, kwargs={"i": i,"method": "GET","Request": self.req})
			th.start()
			threadList.append(th)
			threadList.append(th)

		for i in self.req.variablesPOST():
			self.semTHREADS.acquire()
			th=threading.Thread(target=self.tryDynamic, kwargs={"i": i,"method": "POST","Request": self.req})
			th.start()
			threadList.append(th)
			threadList.append(th)

		for i in threadList:
			i.join()

	def tryDynamic(self,i,method,Request):
		try:
			req=copy.deepcopy(Request)
			req.response=None
	
			logging.debug("Trying dynamic parameter - "+method+" - "+i)
	
			if method=="GET":
				tmp=req.getVariableGET(i)
				req.addVariableGET(i,tmp+"'\"QnoVale")
			else:
				tmp=req.getVariablePOST(i)
				req.addVariablePOST(i,tmp+"'\"QnoVale")
	
			req.perform()
	
	
			HTMLNew=req.response
			HTMLNew.Substitute("'\"QnoVale","")
	
			DynObj=DynamicErrWord(i,method,req)
			DynObj.addOrigResponse(self.origResponse)
			
			if method=="GET":
				req.addVariableGET(i,tmp)
			else:
				req.addVariablePOST(i,tmp)
	
			if DynObj.getInfo(HTMLNew):
				logging.debug("Parameter - "+method+" - "+i+" is dynamic")
				dynres=sqResult(DynObj)
				self.dynamics.append(dynres)
				if self.MakeTest(dynres,tests.INJECTIONTESTS):
					self.injResults.append(dynres)
					self.dynamics.remove(dynres)
					if self.MakeTest(dynres,tests.FINGERTESTS):
						self.fingerResults.append(dynres)
						self.injResults.remove(dynres)
	
			if self.threaded:
				self.semTHREADS.release()
		except Exception,a:
			if self.threaded:
				self.semTHREADS.release()
			print a

		logging.debug("END WITH PARAMETER - "+method+" - "+i)
			

			

	def MakeTest (self,result,test):   # Cada result es siempre un ObjetoDinamico, por lo tanto se acumulan los resultados en la variable results

		if test.launch(result):
			return True

		return False

	def launch(self):
		if self.threaded:
			self.launchThreads()
		else:
			self.launchSerial()

	def launchThreads(self):
		if not self.stability():
			return
		
		self.THDynamism()
		

	def launchSerial(self):
		if not self.stability():
			return
		self.dynamism()

	def getRAWResults(self):
		res=["",[]]
		if self.injResults or self.fingerResults:
			res[0]=self.req.completeUrl
			for i in self.injResults:
				var=[i.getVar(),i.getMethod(),str(i.getType()),str(i.getDB()),i.getError()]
				res[1].append(var)
			for i in self.fingerResults:
				var=[i.getVar(),i.getMethod(),str(i.getType()),str(i.getDB()),i.getError()]
				res[1].append(var)

		else:
			return None
		return res


	def getTXTResults(self):
		TXT=""
		if self.injResults or self.fingerResults:
			TXT+="##==-- sqPyfia Results --==##\r\n"
			TXT+=str(self.req)+"\r\n"
			for i in self.injResults:
				TXT+=str(i)
			for i in self.fingerResults:
				TXT+=str(i)

		return TXT

	def getXMLResults(self):
		if self.injResults or self.fingerResults:
			doc=Document()
			wml = doc.createElement("sqPyfiaResults")
			doc.appendChild(wml)
			result=doc.createElement("SqlInjResult")
			wml.appendChild(result)
			result.appendChild(self.req.getXML(doc))
			if self.injResults or self.fingerResults:
				for i in self.injResults:
					result.appendChild(i.getXML(doc))

				for i in self.fingerResults:
					result.appendChild(i.getXML(doc))

			return doc
		else:
			return None
		
	def getDynamics(self):
		return self.dynamics

	def getInjections(self):
		return self.injResults

	def getFingerPrints(self):
		return self.fingerResults

if __name__=="__main__":
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hb:d:x:D",["xml"])
		optsd=dict(opts)

		a=Request()
		a.setUrl(args[0])

		if "-D" in optsd:
			logging.basicConfig(level=logging.DEBUG,format='%(levelname)s ==> \t%(message)s')
		if "-d" in optsd:
			a.setPostData(optsd["-d"])
		if "-c" in optsd:
			a.addHeader("Cookie",optsd["-c"])
		if "-x" in optsd:
			a.setProxy(optsd["-x"])

	except:
		print "Usage: ./sqPyfia [--xml] [-D(ebug)] [-d POSTDATA] [-b COOKIE] [-x PROXY] URL"
		sys.exit(-1)
	attacker=sqPyfia(a)
	attacker.setThreaded(4)
	attacker.launch()
	if "--xml" in optsd:
		print attacker.getXMLResults().toprettyxml(indent="\t")
	else:
		print attacker.getTXTResults()


