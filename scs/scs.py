#!/usr/bin/python 

 ###############################################################################
 #                    Simple Conficker Scanner
 #
 #
 #
 # Copyright (C) 2009  Felix Leder & Tillmann Werner
 # 
 # This program is free software; you can redistribute it and/or
 # modify it under the terms of the GNU General Public License
 # as published by the Free Software Foundation; either version 3
 # of the License, or (at your option) any later version.
 # 
 # This program is distributed in the hope that it will be useful,
 # but WITHOUT ANY WARRANTY; without even the implied warranty of
 # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 # GNU General Public License for more details.
 # 
 # You should have received a copy of the GNU General Public License
 # along with this program; if not, write to the Free Software
 # Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
 # 
 # 
 #             contact {leder,werner}@cs.uni-bonn.de
 #
 #
 #  thanks to Dan Kaminsky for tricking us into writing this tool
 #
 ###############################################################################



import mutex
import re
import scanner
import sys
from threading import Thread
import thread
import time


FRESH=0
SCANNING=1
IDLE=2


THREAD_COUNT=100

class ScannerEngine(Thread):
    
    def __init__ (self, mtx):
        Thread.__init__(self)
        self.status = FRESH
        self.lock = mtx

    def get_next_ip(self):            
        self.lock.acquire()
        self.ip = get_next_ip()
        self.lock.release()

    def run(self):
        self.get_next_ip()
        while self.ip!=None:
            #print "Looking at IP", self.ip
            scanner.test_infection(self.ip)            
            #print self.ip
            time.sleep(0.1)
                
            self.get_next_ip()



current_ip=None
max_ip=None
ip_list=[]
ip_pos=0

def get_next_ip():
    global current_ip, max_ip, ip_list, ip_pos

    ret = None

    if (not current_ip) or (not max_ip): 
        
        if ip_pos>=len(ip_list): return None
        
        ret = ip_list[ip_pos]
        ip_pos+=1
        
    else:
        if current_ip > max_ip: return None

        ret = repr(current_ip)
        current_ip.plusone()

    return ret


class ip_addr(object):
    
    def __init__(self, ip_str):
        self.value = ip_str

    def to_ints(self):
        return [int(v) for v in self.value.split(".")]

    def plusone(self):
        vals = self.to_ints()
        vals[3]+=1
        if vals[3]>255:
            vals[3]=0
            vals[2]+=1
            if vals[2]>255:
                vals[2]=0
                vals[1]+=1
                if vals[1]>255:
                    vals[1]=0
                    vals[0]+=1
                    if vals[0]>255:
                        vals[0] = 0

        self.value="%i.%i.%i.%i" % (vals[0], vals[1], vals[2],vals[3])

    def __repr__(self):
        return self.value

    def __cmp__(self, other):
        me = self.to_ints()
        ot = other.to_ints()

        for i in xrange(4):
            if me[i]<ot[i]: return -1
            elif me[i]>ot[i]: return 1
        
        return 0


def is_ip(addr):
    ip = addr.split(".")
    if len(ip)!=4: return False

    for i in ip:
        num = int(i)
        if  num<0 or num>255: return False

    return True
    


def usage():
    print """Usage:
%s <start-ip> <end-ip> | <ip-list-file>""" % sys.argv[0]

    sys.exit(1)
    

if __name__=="__main__":
    threads = []

    scanner.print_creds()
    
    if len(sys.argv)==3:
        if not is_ip(sys.argv[1]): usage()
        if not is_ip(sys.argv[2]): usage()    

        current_ip = ip_addr(sys.argv[1])
        max_ip = ip_addr(sys.argv[2])

        if current_ip > max_ip:
            hlp = max_ip
            max_ip = current_ip
            current_ip = hlp

    elif len(sys.argv)==2:
        ip_list = [x.replace("\n","") for x in file(sys.argv[1],"r").readlines()]
        ip_pos = 0

    else:
        usage()
    

    lock = thread.allocate_lock()

    for i in xrange(THREAD_COUNT):
        t = ScannerEngine(lock)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print "Done"
