#Covered by GPL V2.0
#Coded by Carlos del Ojo Elias (deepbit@gmail.com)

from Proxynet import *
from attacker import *
import htmlout



class Controller:

	def __init__(self):
		self.variableStats={}
		self.reqStats={}
		self.requests=[]
		self.newRequests=[]

		self.xssResults=[]
		self.sqlResults=[]

	def clearAttackerCache(self):
		Attacker.clearCache()

	def getVariableStats(self):
		return self.variableStats

	def getReqStats(self):
		return self.reqStats

	def updateAllStats(self):
		self.variableStats={}
		self.reqStats={}

		for i in self.requests:
			self.updateStats(i)


	def updateStats(self,req):
		i=req

		######### ACTUALIZAMOS VARIABLE STATS ####################
		if not self.variableStats.has_key(i.urlWithoutPath):
			self.variableStats[i.urlWithoutPath]={}
		if  not self.variableStats[i.urlWithoutPath].has_key(i.path):
			self.variableStats[i.urlWithoutPath][i.path]={}

		for j in i.variablesGET():
			if not self.variableStats[i.urlWithoutPath][i.path].has_key(j):
				self.variableStats[i.urlWithoutPath][i.path][j]={}
			self.variableStats[i.urlWithoutPath][i.path][j][i.getVariableGET(j)]=True

		for j in i.variablesPOST():
			if not self.variableStats[i.urlWithoutPath][i.path].has_key(j):
				self.variableStats[i.urlWithoutPath][i.path][j]={}
			self.variableStats[i.urlWithoutPath][i.path][j][i.getVariablePOST(j)]=True
			
		######## ACTUALIZAMOS REQUEST STATS ######################
		if not self.reqStats.has_key(i.urlWithoutPath):
			self.reqStats[i.urlWithoutPath]={}
	
		if not self.reqStats[i.urlWithoutPath].has_key(i.path):
			self.reqStats[i.urlWithoutPath][i.path]=[]
	

		nomvars=i.variablesGET()
	
		if nomvars!=None and len(nomvars)>0:
			nomvars.sort()
	
			found=False
			for k in  self.reqStats[i.urlWithoutPath][i.path]:
				if k[0]==nomvars:
					found=True
	
			if found==False:
				self.reqStats[i.urlWithoutPath][i.path]+=[(nomvars,i.variablesGET())]


		nomvars=i.variablesPOST()
	
		if nomvars!=None and len(nomvars)>0:
			nomvars.sort()
	
			found=False
			for k in  self.reqStats[i.urlWithoutPath][i.path]:
				if k[0]==nomvars:
					found=True
	
			if found==False:
				self.reqStats[i.urlWithoutPath][i.path]+=[(nomvars,i.variablesPOST())]

		##########################################################


	def timer(self):
		size=Proxynet.getNumberRequests()
		if size:
			for n in range(size):
				i=Proxynet.getRequest()
				self.requests+=[i]
				self.updateStats(i)
				self.newRequests.append(i)
				Attacker.addReq(i)


	def xssToogled(self,int):
		Attacker.enableXSS(int)

	def sqlToogled(self,int):
		Attacker.enableSQL(int)


	def getRequests(self):
		return self.requests
	
	def getNewRequests(self):
		x=self.newRequests[:]
		self.newRequests=[]
		return x

	def getSqlResults(self):
		res=Attacker.getSqlResults()
		if res:
			self.sqlResults+=res
		return res


	def getXssResults(self):
		res=Attacker.getXssResults()
		if res:
			self.xssResults+=res
		return res

	def getNumAttacks(self):
		return Attacker.getNumAttacks()

	def changeReqThreads(self,n):
		Attacker.setThreads(n)

	def saveXMLSql(self,file):
		a=Attacker.getXMLSql()
		doc=Document()
		wml=doc.createElement("ProxyStrikeResults")
		doc.appendChild(wml)
		for i in a:
			wml.appendChild(i)

		f=open(file,"w")
		f.write(doc.toprettyxml())
		f.close()


	def saveXMLXss(self,file):
		a=Attacker.getXMLXss()
		doc=Document()
		wml=doc.createElement("ProxyStrikeResults")
		doc.appendChild(wml)
		for i in a:
			wml.appendChild(i)

		f=open(file,"w")
		f.write(doc.toprettyxml())
		f.close()


	def saveHTMLXss(self,file):
		output=htmlout.html(title="Xss results")

		for r in self.xssResults:
			t=htmlout.XssTable()
			t.setTitle(r[0])
			for j in r[1]:
				t.addRow(j)
			output.appendTable(t)
			output.flush()

		f=open(file,"w")
		f.write(str(output))
		f.close()


	def saveHTMLSql(self,file):
		output=htmlout.html(title="Sql injection results")

		for r in self.sqlResults:
			t=htmlout.SqlTable()
			t.setTitle(r[0])
			for j in r:
				t.addRow(j)
			output.appendTable(t)
			output.flush()

		f=open(file,"w")
		f.write(str(output))
		f.close()
