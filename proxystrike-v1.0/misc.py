#Covered by GPL V2.0
#Coded by Carlos del Ojo Elias (deepbit@gmail.com)
# This is a port of sqlibf to python, # sqlibf is a SQL injection 
# tool that was coded by Ramon Pinuaga (www.open-labs.org)


import re
import md5

REWORDS=re.compile("([a-zA-Z]{3,})")
SCRIPTS=re.compile("(<script[^>]*>([^<]|<[^s]|<s[^c]|<sc[^r]|<scr[^i]|<scri[^p])*</script>)",re.I)
TAG=re.compile("<[^>]*>")

def getResponseWords (resp):   ### Divide una response en las palabras que la componen
	words={}
	str=resp.getContent()

	

	for i,j in SCRIPTS.findall(str):
		str=str.replace(i,"")
	str=TAG.sub("",str)

	for j in REWORDS.findall(str):
		if len(j)>3:
			words[j]=True
	words=words.keys()
	words.sort()
	return words

def getRESPONSEMd5 (resp):      ### Obtiene el MD5 de una response
	return md5.new(" ".join(getResponseWords(resp))).hexdigest()

