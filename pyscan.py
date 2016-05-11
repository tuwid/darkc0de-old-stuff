#!/usr/bin/python

import socket as sk
import sys
import threading

MAX_THREADS = 50

def usage():
    print "\npyScan 0.1"
    print "usage: pyScan <host> [start port] [end port]"
    
class Scanner(threading.Thread):
    def __init__(self, host, port):
        threading.Thread.__init__(self)
        # host and port
        self.host = host
        self.port = port
        # build up the socket obj
        self.sd = sk.socket(sk.AF_INET, sk.SOCK_STREAM)

    def run(self):
        try:
            # connect to the given host:port
            self.sd.connect((self.host, self.port))
            print "%s:%d OPEN" % (self.host, self.port)
            self.sd.close()
        except: pass

class pyScan:
    def __init__(self, args=[]):
        # arguments vector
        self.args = args
        # start port and end port
        self.start, self.stop = 1, 1024
        # host name
        self.host = ""

        # check the arguments
        if len(self.args) == 4:
            self.host = self.args[1]
            try:
                self.start = int(self.args[2])
                self.stop = int(self.args[3])
            except ValueError:
                usage()
                return
            if self.start > self.stop:
                usage()
                return
        elif len(self.args) == 2:
            self.host = self.args[1]
        else:
            usage()
            return

        try:
            sk.gethostbyname(self.host)
        except:
            print "hostname '%s' unknown" % self.host
        self.scan(self.host, self.start, self.stop)

    def scan(self, host, start, stop):
        self.port = start
        while self.port <= stop:
            while threading.activeCount() < MAX_THREADS:
                Scanner(host, self.port).start()
                self.port += 1
        
if __name__ == "__main__":
    pyScan(sys.argv)

