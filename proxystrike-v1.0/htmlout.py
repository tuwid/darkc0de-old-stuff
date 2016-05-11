#Covered by GPL V2.0
#Coded by Carlos del Ojo Elias (deepbit@gmail.com)


class Table:
	def __init__(self):
		self.title=""
		self.url=""
		self.rows=[]

	def setTitle(self,str):
		self.url=str
		str=str.replace("/","/<wbr/>")
		str=str.replace("&","&<wbr/>")
		self.title=str

	def addRow(self,row):
		self.rows.append(row)

class SqlTable(Table):
	def __init__(self):
		Table.__init__(self)
		self.rowstitles=["Method","Variable Name","Injection type","Fingerprint","Database Error"]

	def __str__ (self):     # ['http://www.game.es/tiendas/centros.aspx?CodProvincia=43', [['CodProvincia', 'GET', 'Single Quoted Injection', 'MS Sql Server', None]]]
		rows="<tr class='tits'><td>%s</td></tr>" % ("</td><td>".join(self.rowstitles))

		for variables in self.rows[1]:
			name,method,injt,fing,err=variables
			if not injt:
				injt="&nbsp;"
			if not fing:
				fing="&nbsp;"
			if not err:
				err="&nbsp;"
			rows+="<tr class='rs'><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (method,name,injt,fing,err)

		rows="<div class='url'>%s</div><table>%s</table>" % (self.rows[0],rows)
	
		return rows



class XssTable(Table):
	def __init__(self):
		Table.__init__(self)
		self.rowstitles=["Method","Variable Name","Allowed injections"]
	def __str__ (self):
		if not self.rows:
			return ""

		post=False               # MIRANDO SI EXISTEN PARAMETROS POR POST
		for i in self.rows:
			if i[1]=="POST":
				post=True
				break

		if post:
			rows="<form action='%s' method='POST'><tr class='tits'><td>%s</td><td>%s</td><td>%s</td><td>Value</td></tr>" % (self.url,self.rowstitles[0],self.rowstitles[1],self.rowstitles[2])
		else:
			rows="<form action='%s' method='GET'><tr class='tits'><td>%s</td><td>%s</td><td>%s</td><td>Value</td></tr>" % (self.url,self.rowstitles[0],self.rowstitles[1],self.rowstitles[2])

		for successfull,met,nvar,set,val in self.rows:
			if successfull:
				rows+="<tr class='rs' valign='top'><td>%s</td><td>%s</td><td>" % (met,nvar)
				for j in set:
					rows+="%s<br>" % (j)
	
				if post:
					if met=="POST":
						rows+="</td><td><input type=text name='%s' value='%s'></td>" % (nvar,val)
					else:
						rows+="</td><td>&nbsp;</td>"
				else:
					rows+="</td><td><input type=text name='%s' value='%s'></td></tr>\n" % (nvar,val)

			elif met=="POST" or (met=="GET" and not post) :
					rows+="<input type=hidden name='%s' value='%s'>" % (nvar,val)

		if post:	
			rows="<div class='url'>%s</div><table>%s</table><input type='submit' value='Enviar'><br><br><br></form>" % (self.title,rows)
		else:
			rows="<div class='url'><a href=%s>%s</a></div><table>%s</table><input type='submit' value='Enviar'><br><br><br></form>" % (self.url,self.title,rows)

		return rows

class html:
	STYLE='''<style type="text/css">
body { text-align: center; }
.container { width: 800px; margin-right:auto; margin-left:auto; text-align: left; }
.url { background-color: #ffc9be; margin: 2px 2px 0px 2px; padding: 5px; }
table { width: 100%; border-collapse: collapse; }
tr.tits { background-color: #beffcd; }
tr.rs { background-color: #ffe6be; }
td { border-style: solid; border-width: 2px; border-color: #ffffff; padding: 3px; }
</style>\n'''

	def __init__(self,file=None,title="None"):
		self.tables=[]
		self.file=file
		self.HEADER='''<h1>ProxyStrike results<h5>by Carlos del Ojo</h5></h1><h1>%s</h1>''' % (title)
		self.output="<html>\n<head>\n%s\n</head>\n<body>\n%s<div class='container'>" % (html.STYLE,self.HEADER)
	
	def appendTable(self,table):
		self.tables.append(table)

	def setFile(self,str):
		self.file=str
	
	def flush(self):
		tables=""
		for i in self.tables:
			tables+=str(i)

		self.output+=tables

		if self.file:
			f=open(self.file,"a")
			f.write(self.output)
			self.output=""
			self.tables=[]
			f.close()

	def __str__(self):
		return "".join(self.output)
