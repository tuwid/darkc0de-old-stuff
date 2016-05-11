#Covered by GPL V2.0
#Coded by Carlos del Ojo Elias (deepbit@gmail.com)
# This is a port of sqlibf to python, # sqlibf is a SQL injection 
# tool that was coded by Ramon Pinuaga (www.open-labs.org)


class sqResult:
	def __init__(self,DynObj):
		self.__DynObj=DynObj

		self.type=None
		self.error=None
		self.Database=None
		self.state="Dynamic"

	def Dynamic(self):
		return self.__DynObj

	def getVar(self):
		return self.__DynObj.getVar()

	def getMethod(self):
		return self.__DynObj.getMethod()

	def getReq(self):
		return self.__DynObj.getReq()

	def equalResponse(self,Response):
		return self.__DynObj.equalResponse(Response)

	def setDB(self,string):
		self.state="FingerPrint"
		self.Database=string

	def getDB(self):
		return self.Database

	def getType(self):
		return self.type

	def setType(self,type):
		self.state="Injection"
		self.type=type

	def setError(self,error):
		self.error=error

	def getError(self):
		return self.error

	def __str__ (self):
		str="%s [\n\tVariable method: '%s'\n\tVariable name: '%s' " % (self.state,self.__DynObj.getMethod(),self.__DynObj.getVar())
		if self.type:
			str+="\n\tInjection type: '%s'" % (self.type)
		if self.Database:
			str+="\n\tDatabase Fingerprint: '%s'" % (self.Database)
		if self.error:
			str+="\n\tError string found: '%s'" % (self.error)
		str+="\n]"
		return str

	def getXML(self,doc):
		variable=doc.createElement("variable")
		variable.setAttribute("name",self.__DynObj.getVar())
		variable.setAttribute("method",self.__DynObj.getMethod())
		variable.setAttribute("result",self.state)

		if self.type:
			it=doc.createElement("InjectionType")
			it.appendChild(doc.createTextNode(str(self.type)))
			variable.appendChild(it)
		if self.Database:
			it=doc.createElement("DatabaseFingerPrint")
			it.appendChild(doc.createTextNode(str(self.Database)))
			variable.appendChild(it)
		if self.error:
			it=doc.createElement("DatabaseError")
			it.appendChild(doc.createTextNode(str(self.error)))
			variable.appendChild(it)

		return variable
