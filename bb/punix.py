#!/usr/bin/env python
# -*- Python -*-
#
# brute_blocker
# made by phate <my_phate@yahoo.es>
# http://phate.hercodesigns.com
#
# 09/02/05


"""
brute_blocker


Es un script, que junto a swatch, nos ayuda a protegernos en tiempo REAL de los ataques
a passwords debiles a cualquier servidor que use el hosts.deny para el control de acceso.

Acentos omitidos intencionadamente.


English

He is script, that next to swatch, helps us to protect in real time of the attacks 
to passwords any server to us who uses hosts.deny for the access control.

Sorry for my poor English

"""

import sys
import re
black = '/etc/blacklist'
deny = '/etc/hosts.deny'


#devuelve "si", si ya se encuentra la ip dentro de la lista negra.

def existeip(ip):
	try:
		fr = open(black,'r')
		yo = fr.readline()
	except IOError, (errno, strerror):
    		print "Error de E/S(%s): %s" % (errno, strerror)
		print "El fichero blacklist debe existir y ser accesible."
		sys.exit()

	while yo != "":
		#print yo
		yo2 = yo[:(len(yo)-1)]
		if (yo2 == ip):
			print "Reintento del capullo: " + yo2
			return "si"
		else:
			yo = fr.readline()
	fr.close

#devuelve "no" si ya existe la ip en hosts.deny
#devuelve "si" si hay que agregarla en hosts.deny, pero que literal soy

def etc(ip):
	try:
		fr = open(deny,'r')
		yo = fr.readline()
	except IOError, (errno, strerror):
    		print "Error de E/S(%s): %s" % (errno, strerror)
		print "En funcion etc()"
		sys.exit()
	yo2 = ""
	if yo == "":
		return "si"
	while yo != "":
		match = re.search(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", yo)
		if match:
			yo2 = match.group()
			if yo2 in ip:
				return "no"
		else:
			yo = fr.readline()
	fr.close
	return "si"



#main() por llamarlo de alguna manera :)

argvs = ""

if len(sys.argv) <= 1:
	print "Deberia tener algun argumento no?"
	sys.exit()
for arg in sys.argv:
	argvs = argvs + arg + " "
#busca una expresion regular 
match = re.search(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", argvs)
if match:
	result = match.group()
	print "Bad login at: " + result
	if existeip(result):
		a = etc(result)
		if a == "si":
			filew = open(deny, 'a')
			filew.write("All:" + result + '\n')
			filew.close
			print "Bloqueado: "+result
	else:
		filew = open(black, 'a')
		filew.write(result + '\n')
		filew.close
else:
	print "No se encontro ninguna ip valida en los argumentos!!!"


