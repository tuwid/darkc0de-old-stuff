#Covered by GPL V2.0

from TextParser import *
from urlparse import *
from time import gmtime, strftime
import pycurl
import gzip
import StringIO
import string
import re


class Request:


	def __init__ (self,tim="",url="",ip="",method="",path="",protocol=""):

		self.pathWithoutVariables=None  # /index.php                ^|
		self.path=None			# /index.php?a=4&b=8        _|

		self.url=None	  		# http://www.google.com:80
		
		self.completeUrl=""
		self.__variablesGET={}
		
		self.__postdata=""		# Datos por POST, toto el string
		self.__variablesPOST={}
		self.__headers={}		# diccionario, por ejemplo headers["Cookie"]
		
		self.response=None		# Apunta a la response que produce dicha request

		################### lo de debajo no se deberia acceder directamente

		self.time=None    		# 23:00:00
		self.ip=None	   		# 192.168.1.1
		self.method="GET" 		# GET o POST (EN MAYUSCULAS SI PUEDE SER)
		self.protocol="HTTP/1.1"	# HTTP/1.1
		self.__performHead=""
		self.__performBody=""

		self.__method=None
		self.__userpass=""

		self.description=""

		self.__proxy=None
		self.__timeout=None
		self.__totaltimeout=None

#	def __setattr__(self,name,value):
#		pass
		

	def setUrl (self, urltmp):
		self.completeUrl=urltmp

		self.__variablesGET={}

		prot,host,path,d,variables,f=urlparse(urltmp)

		self.url=prot+"://"+host


		self.__headers["Host"]=host

		if len(variables)>0:
			self.path=path+"?"+variables
			variables=variables.split("&")
			self.pathWithoutVariables=self.path.split("?")[0]
			for i in variables:
				list=i.split("=")
				if len (list)==1:
					self.addVariableGET(list[0],"")
				elif len (list)==2:
					self.addVariableGET(list[0],list[1])
		else:
			self.path=path
			headers=self.getHeaders()
			for x in headers:
				if x == "Host":
					host=1
			if host != 1:
				self.addHeader("Host",host)
			self.pathWithoutVariables=path


	def setProxy (self,prox):
		self.__proxy=prox

	def setConnTimeout (self,time):
		self.__timeout=time

	def setTotalTimeout (self,time):
		self.__totaltimeout=time
############## Autenticacion ###########################
	def setAuth (self,method,string):
		self.__method=method
		self.__userpass=string

	def getAuth (self):
		return self.__method, self.__userpass

############## TRATAMIENTO VARIABLES GET & POST #########################

	def variablesGET(self):
		return self.__variablesGET.keys()

	def variablesPOST(self):
		return self.__variablesPOST.keys()

	def addVariablePOST (self,key,value):
		self.method="POST"
		self.__variablesPOST[key]=value
		self.__updatePost()

	def addVariableGET (self,key,value):
		self.__variablesGET[key]=value
		self.__updateGet()

	def getVariableGET (self,key):
		if self.__variablesGET.has_key(str(key)):
			return self.__variablesGET[str(key)]
		else:
			return None

	def getVariablePOST (self,key):
		if self.__variablesPOST.has_key(str(key)):
			return self.__variablesPOST[str(key)]
		else:
			return None

	def __updateGet(self):
		newgetdata=[]
		for i,j in self.__variablesGET.iteritems():
			newgetdata.append(string.join([i,str(j)],"="))

		newgetdata2=string.join(newgetdata,"&")

		self.completeUrl=self.completeUrl.split("?")[0]
		self.path=self.path.split("?")[0]
		if len(newgetdata2)>0:
			self.completeUrl+=("?"+newgetdata2)
			self.path+=("?"+newgetdata2)

	def __updatePost (self):
		newpostdata=[]
		for i,j in self.__variablesPOST.items():
			newpostdata.append(string.join([i,str(j)],"="))

		self.__postdata=string.join(newpostdata,"&")
		self.__headers["Content-Length"]=str(len(self.__postdata))

	def setPostData (self,pd):
		self.__variablesPOST={}
		self.method="POST"
		self.__postdata=pd
		variables=self.__postdata.split("&")
		for i in variables:
			tmp=i.split("=",1)
			if len(tmp)==2:
				self.addVariablePOST(tmp[0],tmp[1])
			else:
				self.addVariablePOST(tmp[0],'')


	def addPostdata (self,str):
		self.method="POST"
		self.__postdata=self.__postdata+str
		variables=str.split("&")
		for i in variables:
			tmp=i.split("=",1)
			if len(tmp)==2:
				self.addVariablePOST(tmp[0],tmp[1])
			else:
				self.addVariablePOST(tmp[0],'')




############################################################################

	def addHeader (self,key,value):
		k=string.capwords(key,"-")
		if k!="Accept-Encoding":
			self.__headers[k]=value

	def getHeaders (self):
		return self.__headers.keys()

	def __getitem__ (self,key):
		k=string.capwords(key,"-")
		if self.__headers.has_key(k):
			return self.__headers[k]
		else:
			return ""

	def __getHeaders (self):
		list=[]
		for i,j in self.__headers.items():
			list+=["%s: %s" % (i,j)]
		return list


	def perform(self):
		self.__performHead=""
		self.__performBody=""

		conn=pycurl.Curl()
		conn.setopt(pycurl.SSL_VERIFYPEER,False)
		conn.setopt(pycurl.SSL_VERIFYHOST,1)
		conn.setopt(pycurl.URL,self.completeUrl)

		if self.__method or self.__userpass:
			if self.__method=="basic":
				conn.setopt(pycurl.HTTPAUTH, pycurl.HTTPAUTH_BASIC)
			elif self.__method=="ntlm":
				conn.setopt(pycurl.HTTPAUTH, pycurl.HTTPAUTH_NTLM)
			elif self.__method=="digest":
				conn.setopt(pycurl.HTTPAUTH, pycurl.HTTPAUTH_DIGEST)
			conn.setopt(pycurl.USERPWD, self.__userpass)

		if self.__timeout:
			conn.setopt(pycurl.CONNECTTIMEOUT, self.__timeout)
			conn.setopt(pycurl.NOSIGNAL, 1)

		if self.__totaltimeout:
			conn.setopt(pycurl.TIMEOUT, self.__totaltimeout)
			conn.setopt(pycurl.NOSIGNAL, 1)

		conn.setopt(pycurl.WRITEFUNCTION, self.body_callback)
		conn.setopt(pycurl.HEADERFUNCTION, self.header_callback)

		if self.__proxy!=None:
			conn.setopt(pycurl.PROXY,self.__proxy)
			if self.__headers.has_key("Proxy-Connection"):
				del self.__headers["Proxy-Connection"]

		conn.setopt(pycurl.HTTPHEADER,self.__getHeaders())
		if self.method=="POST":
			conn.setopt(pycurl.POSTFIELDS,self.__postdata)
		conn.perform()

		rp=Response()
		rp.parseResponse(self.__performHead)
		rp.addContent(self.__performBody)

		self.response=rp

	######### ESTE conjunto de funciones no es necesario para el uso habitual de la clase

	def getPostData (self):
		return self.__postdata

	def getAll (self):
		"Devuelve el texto de la request completa (lo que escrbirias por telnet"
		string=str(self.method)+" "+str(self.path)+" "+str(self.protocol)+"\n"
		for i,j in self.__headers.items():
			string+=i+": "+j+"\n"
		string+="\n"+self.__postdata

		return string

	def getAll_wpost (self):
		"Devuelve el texto de la request completa (lo que escrbirias por telnet"
		string=str(self.method)+" "+str(self.path)+" "+str(self.protocol)+"\n"
		for i,j in self.__headers.items():
			string+=i+": "+j+"\n"
		return string



	def header_callback(self,data):
		self.__performHead+=data

	def body_callback(self,data):
		self.__performBody+=data

	def Substitute(self,src,dst):
		prot=urlparse(self.completeUrl)[0]
		a=self.getAll()
		rx=re.compile(src)
		b=rx.sub(dst,a)
		del rx
		self.parseRequest(b,prot)

	def parseRequest (self,rawRequest,prot="http"):
		''' Aun esta en fase BETA y por probar'''
		tp=TextParser()
		tp.setSource("string",rawRequest)

		self.__postdata=""		# Datos por POST, toto el string
		self.__variablesPOST={}
		self.__headers={}		# diccionario, por ejemplo headers["Cookie"]


		tp.readLine()
		try:
			tp.search("(\w+) (.*) (HTTP\S*)")
			self.method=tp[0][0]
			self.protocol=tp[0][2]
		except:
			print "error en"
			print rawRequest
			return

		pathTMP=tp[0][1]
		pathTMP=('',)+urlparse(pathTMP)[1:]
		pathTMP=urlunparse(pathTMP)
		pathTMP=pathTMP.replace("//","/")
		self.time=strftime("%H:%M:%S", gmtime())

		while True:
			tp.readLine()
			if (tp.search("^([^:]+): (.*)$")):
				self.addHeader(tp[0][0],tp[0][1])
			else:
				break

		self.setUrl(prot+"://"+self.__headers["Host"]+pathTMP)

		if self.method.upper()=="POST":

			lastBytesread=tp.readLine()
			totalBytesRead=0
			pd=""
			while lastBytesread:
				totalBytesRead+=lastBytesread
				pd+=tp.lastFull_line
				lastBytesread=tp.readLine()

			self.__headers["Content-Length"]=str(totalBytesRead)
			self.__postdata=pd

			if string.find(self.__postdata,"\n")==-1:
				variables=self.__postdata.split("&")
				for i in variables:
					tmp=i.split("=",1)
					if len(tmp)==2:
						self.addVariablePOST(tmp[0],tmp[1])
					else:
						self.addVariablePOST(tmp[0],'')


		self.pathWithoutVariables=self.path
		if len(self.path.split("?"))>1:
			variables=self.path.split("?")[1].split("&")
			self.pathWithoutVariables=self.path.split("?")[0]
			for i in variables:
				list=i.split("=")
				if len (list)==1:
					self.addVariableGET(list[0],"")
				elif len (list)==2:
					self.addVariableGET(list[0],list[1])

		self.url="%s://%s" % (prot,self.__headers["Host"])



class Response:

	def __init__ (self,protocol="",code="",message=""):
		self.protocol=protocol         # HTTP/1.1
		self.code=code			# 200
		self.message=message		# OK
		self.__headers=[]		# bueno pues las cabeceras igual que en la request
		self.__content=""		# contenido de la response (si i solo si Content-Length existe)
		self.md5=""             # hash de los contenidos del resultado
		self.charlen=""         # Cantidad de caracteres de la respuesta

	def addHeader (self,key,value):
		k=string.capwords(key,"-")
		if k!="Transfer-Encoding":
			self.__headers+=[(k,value)]


	def addContent (self,text):
		self.__content=self.__content+text

	def __getitem__ (self,key):
		for i,j in self.__headers:
			if key==i:
				return  j
		print "Error al obtener header!!!"

	def getCookie (self):
		str=[]
		for i,j in self.__headers:
			if i.lower()=="set-cookie":
				str.append(j.split(";")[0])
		return  "; ".join(str)


	def has_header (self,key):
		for i,j in self.__headers:
			if i==key:
				return True
		return False

	def header_equal (self,header,value):
		for i,j in self.__headers:
			if i==header and j==value:
				return True
		return False

	def getHeaders (self):
		return self.__headers


	def getContent (self):
	#	if self.header_equal("Content-Encoding","gzip"):
	#		compressedstream = StringIO.StringIO(self.__content)
	#		gzipper = gzip.GzipFile(fileobj=compressedstream)
	#		return gzipper.read()

		return self.__content

	def getAll (self):
		string=str(self.protocol)+" "+str(self.code)+" "+str(self.message)+"\r\n"
		for i,j in self.__headers:
			string+=i+": "+j+"\r\n"
		string+="\r\n"+self.getContent()
		return string

	def Substitute(self,src,dst):
		a=self.getAll()
		rx=re.compile(src)
		b=rx.sub(dst,a)
		del rx
		self.parseResponse(b)

	def getAll_wpost (self):
		string=str(self.protocol)+" "+str(self.code)+" "+str(self.message)+"\r\n"
		for i,j in self.__headers:
			string+=i+": "+j+"\r\n"
		return string


	def parseResponse (self,rawResponse):
		tp=TextParser()
		tp.setSource("string",rawResponse)

		tp.readLine()
		tp.search("(HTTP\S*) ([0-9]+)")

		try:
			self.protocol=tp[0][0]
		except:
			self.protocol="unknown"

		try:
			self.code=tp[0][1]
		except:
			self.code="0"

#		try:
#			self.message=tp[2]
#		except:
#			self.message="unknown"

		self.code=int(self.code)

		while True:
			tp.readLine()
			if (tp.search("^([^:]+): ?(.*)$")):
				self.addHeader(tp[0][0],tp[0][1])
			else:
				break

		while tp.skip(1):
			self.addContent(tp.lastFull_line)


class ReqrespException(Exception):
	def __init__ (self,value):
		self.__value=value

	def __str__ (self):
		return self.GetError()

	def GetError(self):
		if self.__value==1:
			return "Attribute not modificable"
