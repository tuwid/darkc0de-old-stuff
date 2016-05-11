################################################################
  #
  #  Enumerate known hostnames for a given IP address.
  #
  #  This script automates a search on live search of the form
  #  ip:<ip address>.  It  will crawl through  the results and 
  #  give you  the hostnames of  all sites  that live knows to
  #  resolve to this ip address. 
  #
  #                                            rattle | .aware
  #                                http://www.awarenetwork.org
  #

import sys,os
from urllib2 import *
from socket import gethostbyname
from urlparse import *
from urllib import quote_plus as quote
from HTMLParser import HTMLParser

host     = "search.live.com"
sequence = ['li','h3','a']

class live(HTMLParser):
	
	def __init__(self, q, start, proxy=None, check=True, callback=None):
		HTMLParser.__init__(self)
		self.__q = quote(q)
		self.__start = int(start)
		self.__s = 0
		self.__callback = callback
		self.__check = check
		self.__buffer = ""
		self.__proxy = proxy

	def handle_startendtag(self, tag, attrs):
		return self.handle_starttag(tag,attrs)

	def handle_starttag(self, tag, attrs):

		tag = tag.lower()

		if tag == sequence[self.__s]: 
			self.__s += 1
			if self.__s == len(sequence):
				self.__s = 0
				for v in filter(lambda x: x[0]=='href',attrs):
		
					host = urlparse(v[1])[1]
					try:
						if self.__check and gethostbyname(host) != self.__q:
							continue
					except: continue

					if self.__callback: 
						self.__callback(host)
		else:
			self.__s = 0
			
  
	def resolve(self):
		try:
			r = Request("http://%s/results.aspx?q=ip%%3a%s&first=%d&FORM=PERE" % (host,self.__q,self.__start))
			if (self.__proxy):
				r.set_proxy(self.__proxy,"http")
			req = urlopen(r)	  
			line = req.read(512)
			while line:
				try: self.feed(line)
				finally: line = req.read(512)

		except: 
			pass


if __name__ == '__main__':
	def usage():
		from os.path import split as sp
		print """
%s [-c COUNT] [-d] [-p PROXY:PORT] <ip|host>

    <ip|host>    IP address you'd like to enumerate 
                 (you can also specify a known host for this address).
    -c COUNT     Only output up to COUNT hosts
    -d           Disable double checking via gethostbyname().
    -p PROXY     Allows you to access live via proxy.
""" % sp(os.sys.argv[0])[1]
		sys.exit(1)


	hashdb = []
	if len(sys.argv) < 2: usage()
	check = True
	maxop = None
	proxy = None

	while sys.argv[1].startswith('-'):
		if sys.argv[1][1] == 'd':
			check = False
		elif sys.argv[1][1] == 'c':
			if len(sys.argv) < 2: usage()
			else: maxop = int(sys.argv[2])
			del sys.argv[1]
		elif sys.argv[1][1] == 'p':
			if len(sys.argv) < 2: usage()
			else: proxy = sys.argv[2]
			del sys.argv[1]			
		del sys.argv[1]


	def outP(x):
		h = hash(x)
		if h in hashdb: return
		elif not maxop is None and len(hashdb)>=maxop: return
		hashdb.append(h)
		print "--> %s" % x

	sys.argv[1] = gethostbyname(sys.argv[1])
			

	i,j = 1L,-1

	while j != len(hashdb):
		j = len(hashdb)
		henry = live(sys.argv[1],i,proxy,check,outP)
		henry.resolve()
		henry.close()
		i += 10
