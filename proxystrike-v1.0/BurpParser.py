#!/usr/bin/python

import re
from TextParser import *
from reqresp import *


class BurpParser:
	separator="^"+"="*54

	def __init__ (self,file,growing=False,exclude=""):
		self.tp=TextParser()
		self.tp.setSource("file",file)
		self.tp.growing=growing

		self.reqs=[]
		self.resp=[]

		self.reqs_exclude=[]
		self.resp_exclude=[]

		self.exclude=exclude
		
#		self.readFull()


	def readFull(self):

		while True:
#			if (self.tp.readUntil(BurpParser.separator)==False):
#				return False
#
#			elif (self.tp.search("([0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2})\s+([\S]+)\s+\[([\S]+)\]")):
			if self.readRequest()==False:
				return False
#			else:
#				print "Error response without request"
#				self.readResponse("")

	def readRequest(self):
		if (self.tp.readUntil(BurpParser.separator)==False):
			return False
		self.tp.readLine()
		self.tp.search("([0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2})\s+([\S]+)")
		time=self.tp[0]
		url=self.tp[1]
		self.tp.skip(2)
		completeUrl=url
		self.tp.search("(\w+) (\/\S*) (HTTP\S*)")
		[method,path,protocol]=self.tp
		completeUrl+=path
		

		newreq=Request()
		newreq.url=url
		newreq.method=method
		newreq.path=path
		
		newreq.completeUrl=completeUrl
	
		while True:
			self.tp.readLine()
			if (self.tp.search("^([^:]+): (.*)$")):
				newreq.addHeader(self.tp[0],self.tp[1])
			else:
				break

		if newreq.method.upper()=="POST":

			bytes_read=self.tp.readFull_line()
			
			bytes_to_read=int(newreq["Content-Length"])

			while bytes_to_read>0:
				if bytes_to_read>=bytes_read:
					bytes_to_read=bytes_to_read-bytes_read
					newreq.addPostdata(self.tp.lastline)
					bytes_read=self.tp.readFull_line()
				else:
					newreq.addPostdata(self.tp.lastline[0:bytes_to_read])
					bytes_to_read=0
					
			variables=self.tp.lastline.split("&")
			for i in variables:
				if len (i.split("="))>1:
					newreq.addVariablePOST(i.split("=")[0],i.split("=")[1])
				else :
					newreq.addVariablePOST(i.split("=")[0],"")

		#elif  newreq.method.upper()=="GET":
		newreq.urlWithoutVariables=path
		if len(newreq.path.split("?"))>1:
			variables=newreq.path.split("?")[1].split("&")
			newreq.urlWithoutVariables=newreq.path.split("?")[0]
			for i in variables:
				list=i.split("=")
				if len (list)==1:
					newreq.addVariableiGET(list[0],"")
				elif len (list)==2:
					newreq.addVariableGET(list[0],list[1])
				
		excluded=False
		if len(self.exclude)>0:
			phmatch = re.search(self.exclude,newreq.urlWithoutVariables,re.I)
			if phmatch:
				self.reqs_exclude=self.reqs_exclude+[newreq]
				excluded=True
			else:	
				self.reqs=self.reqs+[newreq]

		else:
			self.reqs=self.reqs+[newreq]


				
		self.tp.readUntil(BurpParser.separator)
		
		self.tp.readLine()
		if (self.tp.search("(HTTP\S*) ([0-9]+) (.*)")):
			self.readResponse(excluded)

		if excluded==True:
			pass#	self.reqs_exclude[-1].response=self.resp_exclude[-1]
		else:
			self.reqs[-1].response=self.resp[-1]

		return True

	def readResponse(self,excluded):
		[protocol,code,message]=self.tp
		newresp=Response(protocol,code,message)
		
		while True:
			self.tp.readLine()
			if (self.tp.search("^([^:]+): (.*)$")):
				newresp.addHeader(self.tp[0],self.tp[1])
			else:
				break

	
		if newresp.has_header("Content-Length"):
			
			bytes_read=self.tp.readFull_line()
			bytes_to_read=(int)(newresp["Content-Length"])
			while bytes_to_read>0:
				if bytes_to_read>=bytes_read:
					bytes_to_read=bytes_to_read-bytes_read
					newresp.addContent(self.tp.lastline)
					bytes_read=self.tp.readFull_line()
				else:
					newresp.addContent(self.tp.lastline[0:bytes_to_read])
					bytes_to_read=0
	
		if excluded==True:
			self.resp_exclude=self.resp_exclude+[newresp]
		else:
			self.resp=self.resp+[newresp]

		self.tp.readUntil(BurpParser.separator)
		
