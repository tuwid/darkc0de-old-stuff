#!/usr/bin/env python

import md5, sys, hashlib

def main():
	if len(sys.argv) == 4:
		if sys.argv[1] == '-e':
			encriptar()
		else:
			uso()
	elif len(sys.argv) == 5:
		if sys.argv[1] == '-c':
			crakeo()
		else:
			uso()
	else:
		uso()

def uso():
	print "Encriptador y crakeador:"
	print "Forma de uso:"                
	print "Para encriptar: %s y -e -opcion palabra" % sys.argv[0]
	print "Para crakear: python %s -c -opcion hash diccionario.txt" % sys.argv[0]
	print "opciones: -md5 || -sha1"
	print "Kalith: Kalith.9[at]gmail[dot]com"
	print "http://0x59.es"

def crakeo():
	a = False
	hash= sys.argv[3]
	try:
		dicc= open((sys.argv[4]), 'r')
		if sys.argv[2] == '-md5':
			crak_md5(a, hash, dicc)
		elif sys.argv[2] == '-sha1':
			crak_sha1(a, hash, dicc)
		else:
			uso()
	except IOError:
		print "Debe ser un archivo de texto valido... verificalo porfavor"
			
def crak_md5(a, hash, dicc):
	if len(hash) == 32:
		print "El hash esta siendo crakeado... espera porfavor.."
		for i in dicc.read().split():
			PalabraEn= md5.new(i).hexdigest()
			if PalabraEn==hash:
				print "%s es el producto encriptado de %s" % (hash, i)
				a= True
				break
		if not a:
			print "El hash no se pudo crakear..."
		dicc.close()
	else:
		print "Debe estar en md5"
	
def crak_sha1(a, hash, dicc):
	if len(hash) == 40:
		print "El hash esta siendo crakeado... espera porfavor.."
		for i in dicc.read().split():
			PalabraEn= hashlib.sha1(i).hexdigest()
			if PalabraEn==hash:
				print "%s es el producto encriptado de %s" % (hash, i)
				a= True
				break
		if not a:
			print "El hash no se pudo crakear..."
		dicc.close()
	else:
		print "Debe estar en sha1.."

def encriptar():
	if sys.argv[2] == '-md5':
		print encr_md5()
	elif sys.argv[2] == '-sha1':
		print encr_sha1()
	else:
		uso()

def encr_md5():
	return "El resultado es: %s" % md5.new(sys.argv[3]).hexdigest()
	
def encr_sha1():
	return "El resultado es: %s" % hashlib.sha1(sys.argv[3]).hexdigest()

main()
