#!/usr/local/bin/python

#Covered by GPL V2.0
#Coded by Carlos del Ojo Elias (deepbit@gmail.com)

from reqresp import *
from OpenSSL import SSL
import threading
import re

mutex=1
Semaphore_Mutex=threading.BoundedSemaphore(value=mutex)


import BaseHTTPServer, select, socket, SocketServer, urlparse

class ProxyHandler (BaseHTTPServer.BaseHTTPRequestHandler):
	__base = BaseHTTPServer.BaseHTTPRequestHandler
	__base_handle = __base.handle

	server_version = "Vapwn PROXY"
	rbufsize = 0						# self.rfile Be unbuffered

	def _connect_to(self, netloc, soc):
		i = netloc.find(':')
		if i >= 0:
			host_port = netloc[:i], int(netloc[i+1:])
		else:
			host_port = netloc, 80
		try: soc.connect(host_port)
		except socket.error, arg:
			try: 
				msg = arg[1]
			except: 
				msg = arg
				try:
					self.send_error(404, msg)
				except:
					pass
			return 0
		return 1



	def do_CONNECT(self):
		soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			self.wfile.write(self.protocol_version + " 200 Connection established\r\n")
			self.wfile.write("Proxy-agent: %s\r\n" % self.version_string())
			self.wfile.write("\r\n")

			ctx = SSL.Context(SSL.SSLv23_METHOD)
			ctx.set_timeout(5)
  			fpem = 'server.pem'
   			ctx.use_privatekey_file (fpem)
			ctx.set_verify(SSL.VERIFY_NONE,self.test)
			ctx.use_certificate_file(fpem)
			sok=SSL.Connection(ctx,self.connection)
			sok.set_accept_state()
		
#			try:
			ssldat=self._read(sok,300)
#			except:
#				sok.close()
#				return
				
			sslreq=Request()
			sslreq.parseRequest(ssldat,"https")
	#		sslreq.completeUrl="https://%s%s" % (self.path,sslreq.completeUrl)
			#sslreq.host=self.path

			######## PRE PROCESS ###############################

			if Proxynet.get_signGET():
				sslreq.addVariableGET(Proxynet.get_signGET(),"")

			if Proxynet.get_headersign():
				h,v=Proxynet.get_headersign()
				sslreq.addHeader(h,v)

			if Proxynet.get_limitpath():
				if not re.findall(Proxynet.get_limitpath(),sslreq.completeUrl):
					if sslreq['Referer']:
						if not re.findall(Proxynet.get_limitpath(),sslreq['Referer']):
							sok.send("HTTP/1.1 200 OK\r\nServer: gws\r\n\r\n\r\nAccess denied by Proxy (Proxynet)\r\n")
							sok.close()
							return
					else:
						sok.send("HTTP/1.1 200 OK\r\nServer: gws\r\n\r\n\r\nAccess denied by Proxy (Proxynet)\r\n")
						sok.close()
						return

			#####################################################

			if Proxynet.getProxy():
				sslreq.setProxy(Proxynet.getProxy())

			#####################################################

			sslreq.perform()

			if Proxynet.getProxy():
				nr=Response()
				nr.parseResponse(sslreq.response.getContent())
				sok.sendall(nr.getAll())
				sslreq.response=nr

			else:
				sok.sendall(sslreq.response.getAll())

			sok.close()

			Proxynet.addRequest(sslreq)


				
		finally:
			soc.close()
			self.connection.close()

	def test():
		return ok

	def do_GET(self):
			
		(scm, netloc, path, params, query, fragment) = urlparse.urlparse( self.path, 'http')

		######## PRE PROCESS ###############################

		if Proxynet.get_signGET():
			query+=Proxynet.get_signGET()

		if Proxynet.get_headersign():
			h,v=Proxynet.get_headersign()
			self.headers[h]=v

		if Proxynet.get_limitpath():
			if not re.findall(Proxynet.get_limitpath(),self.path):
				if 'Referer' in self.headers:
					if not re.findall(Proxynet.get_limitpath(), self.headers['Referer']):
						self.connection.send("HTTP/1.1 200 OK\r\nServer: gws\r\n\r\n\r\nAccess denied by Proxy (Proxynet)\r\n")
						return
	
				elif 'referer' in self.headers:
					if not re.findall(Proxynet.get_limitpath(), self.headers['referer']):
						self.connection.send("HTTP/1.1 200 OK\r\nServer: gws\r\n\r\n\r\nAccess denied by Proxy (Proxynet)\r\n")
						return
				else:
						self.connection.send("HTTP/1.1 200 OK\r\nServer: gws\r\n\r\n\r\nAccess denied by Proxy (Proxynet)\r\n")
						return

		#####################################################
	
		
		if scm != 'http' or fragment or not netloc:
			self.send_error(400, "bad url %s" % self.path)
			return
		soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			if Proxynet.getProxy():
				netloc=Proxynet.getProxy()

			if self._connect_to(netloc, soc):
				if Proxynet.getProxy():
					rawrequest="%s %s %s\r\n" % ( self.command, self.path, self.request_version)
			#		self.headers['Proxy-Connection']='Keep-Alive'
				else:
					rawrequest="%s %s %s\r\n" % ( self.command, urlparse.urlunparse(('', '', path, params, query, '')), self.request_version)
				
				self.headers['Connection'] = 'close'
				del self.headers['Proxy-Connection']
				for key_val in self.headers.items():
					rawrequest+="%s: %s\r\n" % key_val
				rawrequest+="\r\n"
				soc.send(rawrequest)
				try:
					self._read_write(soc,200,rawrequest)
				except:
					pass			
		finally:
			soc.close()
			self.connection.close()

	def _read(self, soc, max_idling=20):
		iw = [soc]
		ow = []
		count = 0
		rawrequest=""
		while 1:
			count += 1
			(ins, _, exs) = select.select(iw, ow, iw, 0.5)
			if exs: break
			if ins:
				rawrequest+= soc.recv(8192)
			else:
				break
			if count == max_idling:
				break

		return rawrequest
	

	def _read_write(self, soc, max_idling=20,rawrequest=""):
		iw = [self.connection, soc]
		ow = []
		count = 0
		rawresponse=""
		while 1:
			count += 1
			(ins, _, exs) = select.select(iw, ow, iw, 3)
			if exs: break
			if ins:
				for i in ins:
					if i is soc:
						out = self.connection
						data = i.recv(8192)
						rawresponse+=data
					else:
						out = soc
						data = i.recv(8192)
						rawrequest+=data
					if data:
						out.send(data)
						count = 0

			if count == max_idling:
				break

		if len(rawresponse)>0 and len(rawrequest)>0:
			req=Request()
			req.parseRequest(rawrequest)
			#req.completeUrl=self.path
			req.response=Response()
			req.response.parseResponse(rawresponse)
			Proxynet.addRequest(req)


	do_HEAD = do_GET
	do_POST = do_GET
	do_PUT  = do_GET
	do_DELETE=do_GET

class ThreadingHTTPServer (SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer): 
	pass

	
	
class proxy (threading.Thread):
	def __init__ (self,port):
		threading.Thread.__init__(self)
		self.exclude=""
		self.stop=False
		self.server_address = ('', port)
		self.httpd = ThreadingHTTPServer(self.server_address, ProxyHandler)


	def run(self):
		while not self.stop:
			self.httpd.handle_request()
		del self.httpd


class Proxynet:
	__PROXY_REQUESTS=[]
	__nreqs=0
	exclude=None
	__header={}
	__get_sign=""
	__limitpath=""
	__USEPROXY=None

	__port=8008
	__prox=None
	__exclude=None
	__start=False

	@staticmethod
	def changePort(port):
		if port!=Proxynet.__port:
			if not Proxynet.__prox:
				Proxynet.__port=port
			else:
				Proxynet.stop()
				Proxynet.__port=port
				Proxynet.__prox=proxy(Proxynet.__port)
				Proxynet.__prox.start()



	@staticmethod
	def init (exclude=""):
		Proxynet.__prox=proxy(Proxynet.__port)
		Proxynet.exclude=exclude.lower()

		Proxynet.__prox.start()

	@staticmethod
	def stop ():
		if Proxynet.__prox:
			Proxynet.__prox.stop=True
			a=Request()
			a.setUrl("http://localhost:%d"%(Proxynet.__port))
			a.perform()
			Proxynet.__prox.join()	
			del Proxynet.__prox
			Proxynet.__prox=None
	
############ LIMITACION Y FIRMAS ##################

	@staticmethod
	def signGET(var):
		Proxynet.__get_sign=var

	@staticmethod
	def signHeaders(var,value):
		Proxynet.__header={}
		if not var:
			Proxynet.__header={}
		else:
			Proxynet.__header[var]=value


	@staticmethod
	def limitPath(regexp):
		Proxynet.__limitpath=regexp


	@staticmethod
	def get_signGET():
		return Proxynet.__get_sign

	@staticmethod
	def get_headersign():
		if len  (Proxynet.__header):
			return  Proxynet.__header.items()[0]
		else:
			return ()

	@staticmethod
	def get_limitpath():
		return Proxynet.__limitpath


################################################

	@staticmethod
	def setProxy(p):
		Proxynet.__USEPROXY=p

	@staticmethod
	def getProxy():
		return Proxynet.__USEPROXY
################################################

	@staticmethod
	def addRequest(r):
		if not re.search(Proxynet.exclude,r.urlWithoutVariables.lower()):	
			Semaphore_Mutex.acquire()
			Proxynet.__PROXY_REQUESTS+=[r]
			Proxynet.__nreqs+=1
			Semaphore_Mutex.release()
		
		
	@staticmethod
	def getRequest():
		Semaphore_Mutex.acquire()
		if Proxynet.__nreqs:
			Proxynet.__nreqs-=1
			a=Proxynet.__PROXY_REQUESTS.pop(0)
			Semaphore_Mutex.release()
			return a
		else:
			Semaphore_Mutex.release()
			return None

	@staticmethod
	def getNumberRequests ():
		return Proxynet.__nreqs

	@staticmethod
	def clearRequests ():
			Semaphore_Mutex.acquire()
			Proxynet.__PROXY_REQUESTS
			Proxynet.__nreqs=0
			Semaphore_Mutex.release()

	@staticmethod
	def addRequests (reqs):
		Semaphore_Mutex.acquire()
		for i in reqs:
			if not re.search(Proxynet.exclude,i.urlWithoutVariables.lower()):	
				Proxynet.__PROXY_REQUESTS+=[i]
				Proxynet.__nreqs+=1
		Semaphore_Mutex.release()
			
	

		
