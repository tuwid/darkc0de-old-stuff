#!usr/bin/python
# dpc-FTPhunt.py v1.0
# FTP checker in specific IP range, try checking anonymous account & save it
# to file
#
# special thanks to: d3hydr8, xco, ch3cksum, gat3w4y, Dr_EIP
# thanks to community: depredac0de & darkc0de
#
#                                                          c0ded by: 5ynL0rd
#-----------------------------------------------------------------------------
import os, sys, socket, ftplib

def banner():
   if os.name == "posix":
      os.system("clear")
   else:
      os.system("cls")
   print '''
.--------------------------------------------------------.
|                    dpc-FTPhunt.py                      |
|                    ``````````````                      |
| for depredac0de & darkc0de community        by:5ynL0rd |
'--------------------------------------------------------'
'''
def iptolist(ip):
   listip = []
   count = 0
   v4check = 0
   while count < len(ip):
      if ip[count] == ".":
         v4check += 1
      count += 1
   if int(v4check) != 3:
      print "stupid fuckin IP version dude!"
      sys.exit(0)
            
   count = 0
   dot = 0
   while count < len(ip):
      if ip[count] == ".":
         dot += 1
         if dot == 1:
            a = ip[0:count]
            if int(a) > 255:
               print "stupid fuckin IP version dude!"
               sys.exit(0)
            listip.append(a)
            bcd = ip[count+1:]
      count += 1
   count = 0
   dot = 0
   while count < len(bcd):
      if bcd[count] == ".":
         dot += 1
         if dot == 1:
            b = bcd[0:count]
            if int(b) > 255:
               print "stupid fuckin IP version dude!"
               sys.exit(0)
            listip.append(b)
            cd = bcd[count+1:]
      count += 1
   count = 0
   dot = 0
   while count < len(cd):
      if cd[count] == ".":
         dot += 1
         if dot == 1:
            c = cd[0:count]
            if int(c) > 255:
               print "stupid fuckin IP version dude!"
               sys.exit(0)
            listip.append(c)
            d = cd[count+1:]
            if int(d) > 255:
               print "stupid fuckin IP version dude!"
               sys.exit(0)
            listip.append(d)
      count += 1
   return listip


def ftp(ip):
   socket.setdefaulttimeout(5)
   try:
      sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
      sock.connect((ip,21))
      sock.close()
   except(socket.error):
      print "[-] %s"%ip
      pass
   else:
      saving = open(logfile,"a")
      print "[o] %s w00t!"%ip
      saving.write("[o] %s w00t!"%ip,)
      print "    trying anonymous authentication...",
      sys.stdout.flush()
      try:
         ftplib.FTP(ip).login("anonymous","anonymous")
      except:
         print "[-] no anonymous"
         saving.write(" -> no anonymous!\n")
         pass
      else:
         print "[o] anonymous available!"
         saving.write(" -> anonymous available!\n")
         ftplib.FTP(ip).quit()
      saving.close()

if "__main__" == __name__:
   banner()
   firstip = raw_input("start IP: ")
   lastip = raw_input("end IP: ")
   logfile = raw_input("logfile name(default ftphunt.log): ")
   if logfile == "":
      logfile = "ftphunt.log"
   ipawal = iptolist(firstip)
   ipakhir = iptolist(lastip)
   z1 = int(ipawal[3])
   z2 = int(ipakhir[3])
   y1 = int(ipawal[2])
   y2 = int(ipakhir[2])
   x1 = int(ipawal[1])
   x2 = int(ipakhir[1])
   w1 = int(ipawal[0])
   w2 = int(ipakhir[0])
   strip1 = "%.3i%.3i%.3i%.3i"%(w1,x1,y1,z1)
   strip1 = int(strip1)
   strip2 = "%.3i%.3i%.3i%.3i"%(w2,x2,y2,z2)
   strip2 = int(strip2)
   if strip2 - strip1 < 0:
      print "Stupid range IP dude!.."
      sys.exit(0)
   else:
      c3 = z1
      c2 = y1
      c1 = x1
      c0 = w1
      print "\nplease wait.. scanning progress!"
      while 1:
         ipl0rd = "%s.%s.%s.%s"%(c0,c1,c2,c3)
         ftpcheck = ftp(ipl0rd)
         if c0 == w2 and c1 == x2 and c2 == y2 and c3 == z2:
            break
         c3 += 1
         if c3 > 255:
            c3 = 0
            c2 += 1
         if c2 > 255:
            c2 = 0
            c1 += 1
         if c1 > 255:
            c1 = 0
            c0 += 1
      print "finished...\nYou can view result in %s"%logfile

# depredator-c0de [04-01-2010]
