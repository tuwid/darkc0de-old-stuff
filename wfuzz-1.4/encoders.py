import urllib
import base64
import re
import binascii
import md5
import sha
import random


# SUPERCLASS

class encoder:
	def __init__(self):
		pass
	
	def encode (self,string):
		return string


#######################################################
######################################################
######## Inheritances
#######################################################
######################################################

class encoder_urlencode (encoder):
	text="Urlencode"
	def __init__(self):
		encoder.__init__(self)

	def encode(self,string):
		return urllib.quote(string)

class encoder_double_urlencode (encoder):
	text="Double urlencode"
	def __init__(self):
		encoder.__init__(self)

	def encode(self,string):
		return urllib.quote(urllib.quote(string))

class encoder_base64 (encoder):
	text="Base64"
	def __init__(self):
		encoder.__init__(self)

	def encode(self,string):
		return base64.standard_b64encode(string)

class encoder_uri_hex (encoder):
	text="Uri hexadecimal"
	def __init__(self):
		encoder.__init__(self)
	
	def encode(self,string):
		strt = ""
		con = "%%%02x"
		s=re.compile(r"/|;|=|:|&|@|\\|\?")	
		for c in string:
			if s.search(c):
				strt += c
				continue
			strt += con % ord(c)
		return strt


class encoder_random_upper (encoder):
	text="Random Uppercase"
	def __init__(self):
		encoder.__init__(self)
	
	def encode(self,string):
		strt = ""
		for c in string:
			x = int(random.uniform(0,10))
			x = x % 2
			if x == 1:
				strt += c.upper()
			else:
				strt += c
		return strt   


class encoder_doble_nibble_hex (encoder):
	text="Double nibble Hexa"
	def __init__(self):
		encoder.__init__(self)
	
	def encode(self,string):
		strt = ""
		fin = ""
		con = "%%%02x"
# first get it in straight hex
		s=re.compile(r"/|;|=|:|&|@|\\|\?")	
		enc=encoder_uri_hex()
		strt = enc.encode(string)
		for c in strt:
			if not c == "%":
				if s.search(c):
					fin += c
					continue
				fin += con % ord(c)
			else:
				fin += c
		return fin

class encoder_sha1 (encoder):
	text="Sha1"
	def __init__(self):
		encoder.__init__(self)

	def encode(self,string):
		s=sha.new()
		s.update(string)
		res =s.hexdigest()
		return res
		
class encoder_md5 (encoder):
	text="Md5"
	def __init__(self):
		encoder.__init__(self)

	def encode(self,string):
		m=md5.new()
		m.update(string)
		res = m.hexdigest()
		return res
		
class encoder_binascii (encoder):
	text="Binary Ascii"
	def __init__(self):
		encoder.__init__(self)

	def encode(self,string):
		res = binascii.hexlify(string)		
		return res

class encoder_html (encoder):
	text="Html encoder"
	def __init__(self):
		encoder.__init__(self)

	def encode(self,string):
		res=string
		res=res.replace("<","&lt;")
		res=res.replace(">","&gt;")
		res=res.replace("\"","&quot;")
		res=res.replace("'","&apos;")
		#res=res.replace("&","&amp;")
		return res

class encoder_html_decimal (encoder):
	text="Html encoder decimal"
	def __init__(self):
		encoder.__init__(self)

	def encode(self,string):
		new=""
		for x in string:
			new+="&#"+str(ord(x))+";"
		return new

class encoder_html_hexadecimal (encoder):
	text="Html encoder Hexa"
	def __init__(self):
		encoder.__init__(self)

	def encode(self,string):
		new=""
		for x in string:
			val="%02x" % ord(x)
			new+="&#x"+str(val)+";"
		return new

class encoder_utf8_binary (encoder):
	text="UTF8 Binary"
	def __init__(self):
		encoder.__init__(self)

	def encode(self,string):
		new=""
		for x in string:
			val="%02x" % ord(x)
			new+="\\x"+str(val)
		return new

class encoder_utf8 (encoder):
	text="UTF8"
	def __init__(self):
		encoder.__init__(self)

	def encode(self,string):
		new=""
		for x in string:
			val="%02x" % ord(x)
			if len(val)==2:
				new+="\\u00"+str(val)
			else:
				new+="\\u"+str(val)
		return new


class encoder_mysqlchar (encoder):
	text="Mysql Char"
	def __init__(self):
		encoder.__init__(self)

	def encode(self,string):
		new="CHAR("
		for x in string:
			val=str(ord(x))
			new+=str(val)+","
		new=new.strip(",")
		new+=")"
		return new

class encoder_mssqlchar (encoder):
	text="Mssql Char"
	def __init__(self):
		encoder.__init__(self)

	def encode(self,string):
		new=""
		for x in string:
			val=str(ord(x))
			new+="CHAR("+str(val)+")+"
		new=new.strip("+")
		return new
