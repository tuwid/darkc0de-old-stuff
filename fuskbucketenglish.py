#!/usr/bin/python
import urllib
import urllib2
import httplib
import os
import os.path

#Made by lauchazombie ---> grindcorizado@gmail.com and the help of the good people at http://python-forum.org,
#if you have any questions find me in 6-chan.org or /server irc.cl /j #6-chan.org
#licensed under gpl (any version) please if you improve it or use it e-mail to check your work
#test it with http://i105.photobucket.com/albums/m210/cute_curlz/,,1,5,jpg
#i never tested this on winbugs

#check if there is a "fuskbucket" folder in home. If after running the script you don't have one
#create it to have the photos saved somewhere
os.chdir(os.environ['HOME'])
if os.path.exists('fuskbucket') == False:
	os.mkdir('fuskbucket')
os.chdir(os.environ['HOME']+'/fuskbucket/')

#Use the first function if -for example- you know the filename starts with "DSC0"
#it also lets you determine where to start and end the fusk

def fuskingconocido():
	print "input separated with , : url , file name (like DSC0 or IMG_00), in what number start the fusk, where to stop, file extension"

	valores = raw_input('> ')
	(sitio, nomenclatura, rangoinicio, rangofin, formatoimagen, ) = valores.split(',')
	if sitio.endswith("/") == False:
		sitio = sitio + '/'
	if formatoimagen.startswith(".") == False:
		formatoimagen = "." + formatoimagen

	while float(rangoinicio) <= float(rangofin):
		objetivo = sitio + nomenclatura + str(rangoinicio) + formatoimagen
		subobjetivo = nomenclatura + str(rangoinicio) + formatoimagen		
		f = urllib.urlopen(objetivo, None, headers)
		x = f.read() 
		asdf = f.headers.type
		if asdf.find("image/jpeg") >=0: #Checks for an image in the URL and tries to download it
			z = open(str(os.environ['HOME']) + '/fuskbucket/' + subobjetivo, "wb")
			z.write(x)
			z.close
			print str(rangoinicio) + ' <-----------------------------> saved! <-----------------------------> '
		rangoinicio = int(rangoinicio) + 1
	
	print "%s has been fusked" % sitio

""" second function this one tries several formats from the file "fusklist1.txt", this file must be in '/home/user/fuskbucket/fuskflist1.txt' """

def fuskingscaneado():
	if os.path.exists('fusklist1.txt') == False:
		z = open('fusklist1.txt', 'w')
		z.write("""DSC0####\nDSCN####\nDSCF####\nP101####\nIMAG####\nIMG_####\n_MG_####\nPICT####\nImage###\nPicture###\nPhoto###\nPicture#\nPhoto#\n#\nme#\nDSCF####\nIMAG####\nIMG_####\nIMG_#####\nPICT####\nPICT###\nImage###\nPicture###\nPhoto###\nPhoto####\nPicture#\nPhoto#\nme#\n100_####\nnew###\nnew#\nCIMG####\nnudes#\nnudes###\nnude#\nnude###\npictures###\nPicture-###\nPhoto-####\nCAMERA####\nbutt#\nass#\nboobs#\nsexy#\nmyphotos###\nnaked###""") 
		z.close()	
	fuskfile = file("fusklist1.txt","r")     
	fusklist = [line.split() for line in fuskfile] #imports the fusklist	

	inicio = 0
	fin = len(fusklist) - 1
	print "input site url"
	url = raw_input('> ')
	print "input where to stop the scan"
	termino = raw_input('> ')	
	rangoinicio = 0	
	if url.endswith("/") == False:
		url = url + '/'
	
	userAgent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
	headers = {'User-Agent' : userAgent}

	while int(rangoinicio) <= int(termino):	
	
		while inicio <= fin:				
			nomenclaturalist = fusklist[inicio]
			nomenclatura = str(nomenclaturalist)
			a = str(nomenclatura).find('#')
			b = len(nomenclatura)
			c = b - a
			nomenclatura = nomenclatura.replace("#", "") # This is used to rename the files replacing '#' with '000'
			nomenclatura = nomenclatura.replace("[", "")
			nomenclatura = nomenclatura.replace("]", "")
			nomenclatura = nomenclatura.replace("'", "")
			nomenclatura = nomenclatura + str(rangoinicio).zfill(c - 2)
			imagen = nomenclatura + '.jpg'
			objetivo = url + str(imagen)	
			chequeo = urllib.urlopen(objetivo, None, headers)
			x = chequeo.read()
			asdf = chequeo.headers.type			
			if asdf.find("image/jpeg") >=0:
				z = open(str(os.environ['HOME']) + '/fuskbucket/' + imagen, "wb")
				z.write(x)
				z.close()
				print str(imagen) + ' <-----------------------------> saved! <-----------------------------> '			
			inicio = inicio + 1
		inicio = 0
		rangoinicio = rangoinicio +1

print " a.- to fusk if you already know the file name \n b.- to fusk using the name on fusklist1.txt" #choose the function you want to run
decision = raw_input('> ')

if decision == 'a':
	fuskingconocido()
elif decision == 'b':
	fuskingscaneado()
else:
	print "choose a or b"




