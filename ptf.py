#!/usr/bin/python
# ^----- change this if necessary!
# 
# PTF - Python TCP Forwarder
# Version: 0.4
# (C) 1999 T. Klausmann <klausman@incas.de>
#
# This program is covered by the GNU public license (GPL) 
#
# The old "Header Docs" will no longer be updated, read 
# the included file "README" instead.
#

import SocketServer
from SocketServer import TCPServer, BaseRequestHandler
from time import sleep
from socket import *
from os import fork
from posix import waitpid, getppid, WNOHANG, kill
from signal import SIGTERM
from errno import *
from sys import *
from string import *

# If someone can tell me how to avoid these
# global vars, go ahead!
global foreign_host
global foreign_port
global local_port

class MyTCPServer(SocketServer.TCPServer):
        def server_bind(self):
                self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
                self.socket.bind(self.server_address)

class myhandler(BaseRequestHandler):

 global foreign_host
 global foreign_port
 global local_port

 # the core request handler

 def handle (self):

	# Init server data variable (for while())
	server_input=client_input="DEADBEEF"

	# Get FD from listener
	client_fd=self.request

	# Open socket to serving machine and connect
	server_fd=socket(AF_INET,SOCK_STREAM)
	server_fd.connect (foreign_host,foreign_port)

	# Now, we fork and handle data in both directions
	CPID=fork()

	# Where are we?
	if (CPID<0):
 	  # oops, somehting went wrong
	  print "Could not fork."
	  return(0)

	if (CPID==0):
	  # This is the child, get parent pid
	  PPID=getppid()

	  # infinite loop with break condition
	  # XXX this is not elegant all
	  while(1):
	   # read 1024 bytes from FD
	   server_input=server_fd.recv(1024)

	   # if we couldn't read, back out
	   if not server_input: break;

	   # write data to client
	   client_fd.send(server_input)

	  # If we were disconnected, kill away the parent
	  kill (PPID, SIGTERM);

        else:
	  # This is the parent, child PID is CPID

	  # infinite loop with break condition 
          # XXX this is not elegant

	  while (1):
	   # Fetch signals and back out if kid is dead
	   if (not waitpid(CPID,WNOHANG)): break;

	   # Read from client FD
	   client_input=client_fd.recv(1024)

	   # Back out if we couldn't read anything
	   if not client_input: break; 

	   # Write data to server
	   server_fd.send(client_input)

	  # Get rid of the kid
	  kill (CPID, SIGTERM);

	# This actually should be a "can't happen",
	# but I am not sure
	# Close remaining FDs
	client_fd.close()
	server_fd.close()

# End of class myhandler

# Main program 
def main():
 global foreign_host
 global foreign_port
 global local_port

 # This sanity check is way too simple
 # future versions should have more pedantic checks
 if (len(argv)<4):
  print "Usage:"
  print "%s foreign_host foreign_port local_port" % argv[0]
  exit (1)

 foreign_host=argv[1]
 foreign_port=atoi(argv[2])
 local_port=atoi(argv[3])

 # Fork off daemon process and exit

 firstpid=fork()
 if (firstpid>0): 
  return (0)
 elif (firstpid<0):
  print ("Could not fork off server process")
  exit (1)
 
 # try to init the server
 try:
  myserver=MyTCPServer(('localhost',local_port),myhandler)
 except:
  print ("Could not start TCPServer. Adress already bound?")
  exit (1)


 # start the server to run forever

 myserver.serve_forever()

if __name__ == "__main__": main()

