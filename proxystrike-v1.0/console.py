#Covered by GPL V2.0
#Coded by Carlos del Ojo Elias (deepbit@gmail.com)

import sys

class Console:
	def __init__(self,prompt):
		self.prompt=prompt
		self.commands={}

	def init(self):
		while True:
			try:
				command=raw_input(self.prompt)
				self.execCommand(command)
			except KeyboardInterrupt:
				break
			except EOFError:
				break
			except Exception,a:
				self.printError (a)

		print "\r\n\r\nBye!..."


	def printError(self,err):
		sys.stderr.write("-- Error: %s\r\n" % (str(err)))

	def addCommand(self,cmd):
		name=cmd.getName().lower()
		if name in self.commands:
			raise Exception,"El comando ya existe"
		else:
			self.commands[name]=cmd
	
	def execCommand(self,cmd):
		words=cmd.split(" ")
		words=[i for i in words if i]
		if not words:
			return
		cmd,parameters=words[0].lower(),words[1:]

		if not cmd in self.commands:
			sys.stderr.write("\r\nCommand '"+cmd+"' not found.\r\n")
			return
		self.commands[cmd].execute(parameters)


class Command:
	def __init__(self,name,func):
		self.__name=name
		self.__func=func
		pass

	def getName(self):
		return self.__name

	def execute(self,pars):
		self.__func(pars)

