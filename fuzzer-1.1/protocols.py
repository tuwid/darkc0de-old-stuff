#!/usr/bin/env python

"""
#  (C) COPYRIGHT SERGIO ALVAREZ 
#	SECURITY RESEARCH & DEVELOPMENT, 2000-2004
#	Covered under GPL v 2.0
#
#  TITLE:       PROTOCOLS.PY
#
#  VERSION:     1.00
#
#  AUTHOR:      Sergio 'shadown' Alvarez
#
#  DATE:        25 SEP 2004
"""

"""
Para agregar un protocolo nuevo simplemente:
	agregarlo en protoname -> 'xxxx' : xxxx
	y luego declararlo como xxxx
	y that's all baby (u wanted it simplier?? u're fucking kidding..., aren't u???)

NOTE: best view with 'tabstop=3'
"""

# declaracion de protocolo 'ftp'
ftp = {
		'proto'	:	'tcp'																			,
		'banner'	:	1																				,
		'comm'	:	[
							{	'command'	: 'USER '		, 'datatype'	: 'string'	, 'default'	: 'ftp'	, 'recv'	: 1	, 'endw' : '\r\n'	,'mustuse'	: 1	},
							{	'command'	: 'PASS '		, 'datatype'	: 'string'	, 'default'	: 'ftp'	, 'recv'	: 1	, 'endw' : '\r\n'	,'mustuse'	: 1	},
							{	'command'	: 'ACCT '		, 'datatype'	: 'string'	, 'default'	: None	, 'recv'	: 1	, 'endw' : '\r\n'	,'mustuse'	: 0	},
							{	'command'	: 'CWD '			, 'datatype'	: 'string'	, 'default'	: None	, 'recv'	: 1	, 'endw' : '\r\n'	,'mustuse'	: 0	},
							{	'command'	: 'SMNT '		, 'datatype'	: 'string'	, 'default'	: None	, 'recv'	: 1	, 'endw' : '\r\n'	,'mustuse'	: 0	},
							{	'command'	: 'TYPE L '		, 'datatype'	: 'int'		, 'default'	: None	, 'recv'	: 1	, 'endw' : '\r\n'	,'mustuse'	: 0	},
							{	'command'	: 'RETR '		, 'datatype'	: 'string'	, 'default'	: None	, 'recv'	: 1	, 'endw' : '\r\n'	,'mustuse'	: 0	},
							{	'command'	: 'STOR '		, 'datatype'	: 'string'	, 'default'	: None	, 'recv'	: 1	, 'endw' : '\r\n'	,'mustuse'	: 0	},
							{	'command'	: 'APPE '		, 'datatype'	: 'string'	, 'default'	: None	, 'recv'	: 1	, 'endw' : '\r\n'	,'mustuse'	: 0	},
							{	'command'	: 'ALLO '		, 'datatype'	: 'int'		, 'default'	: None	, 'recv'	: 1	, 'endw' : '\r\n'	,'mustuse'	: 0	},
							{	'command'	: 'REST '		, 'datatype'	: 'string'	, 'default'	: None	, 'recv'	: 1	, 'endw' : '\r\n'	,'mustuse'	: 0	},
							{	'command'	: 'RNFR '		, 'datatype'	: 'string'	, 'default'	: None	, 'recv'	: 1	, 'endw' : '\r\n'	,'mustuse'	: 0	},
							{	'command'	: 'RNTO '		, 'datatype'	: 'string'	, 'default'	: None	, 'recv'	: 1	, 'endw' : '\r\n'	,'mustuse'	: 0	},
							{	'command'	: 'DELE '		, 'datatype'	: 'string'	, 'default'	: None	, 'recv'	: 1	, 'endw' : '\r\n'	,'mustuse'	: 0	},
							{	'command'	: 'RMD '			, 'datatype'	: 'string'	, 'default'	: None	, 'recv'	: 1	, 'endw' : '\r\n'	,'mustuse'	: 0	},
							{	'command'	: 'MKD '			, 'datatype'	: 'string'	, 'default'	: None	, 'recv'	: 1	, 'endw' : '\r\n'	,'mustuse'	: 0	},
							{	'command'	: 'LIST '		, 'datatype'	: 'string'	, 'default'	: None	, 'recv'	: 1	, 'endw' : '\r\n'	,'mustuse'	: 0	},
							{	'command'	: 'NLST '		, 'datatype'	: 'string'	, 'default'	: None	, 'recv'	: 1	, 'endw' : '\r\n'	,'mustuse'	: 0	},
							{	'command'	: 'SITE '		, 'datatype'	: 'string'	, 'default'	: None	, 'recv'	: 1	, 'endw' : '\r\n'	,'mustuse'	: 0	},
							{	'command'	: 'STAT '		, 'datatype'	: 'string'	, 'default'	: None	, 'recv'	: 1	, 'endw' : '\r\n'	,'mustuse'	: 0	},
							{	'command'	: 'HELP '		, 'datatype'	: 'string'	, 'default'	: None	, 'recv'	: 1	, 'endw' : '\r\n'	,'mustuse'	: 0	},
							{	'command'	: 'MDTM '		, 'datatype'	: 'int'		, 'default'	: None	, 'recv'	: 1	, 'endw' : '\r\n'	,'mustuse'	: 0	},
							{	'command'	: 'MDTM '		, 'datatype'	: 'string'	, 'default'	: None	, 'recv'	: 1	, 'endw' : '\r\n'	,'mustuse'	: 0	},
							{	'command'	: 'MLSD '		, 'datatype'	: 'string'	, 'default'	: None	, 'recv'	: 1	, 'endw' : '\r\n'	,'mustuse'	: 0	},
							{	'command'	: 'MLST '		, 'datatype'	: 'string'	, 'default'	: None	, 'recv'	: 1	, 'endw' : '\r\n'	,'mustuse'	: 0	},
							{	'command'	: 'QUOTE '		, 'datatype'	: 'string'	, 'default'	: None	, 'recv'	: 1	, 'endw' : '\r\n'	,'mustuse'	: 0	},
							{	'command'	: 'SIZE '		, 'datatype'	: 'string'	, 'default'	: None	, 'recv'	: 1	, 'endw' : '\r\n'	,'mustuse'	: 0	},
							{	'command'	: 'OPTS '		, 'datatype'	: 'string'	, 'default'	: None	, 'recv'	: 1	, 'endw' : '\r\n'	,'mustuse'	: 0	},
							{	'command'	: 'SITE CPWD '	, 'datatype'	: 'string'	, 'default'	: None	, 'recv'	: 1	, 'endw' : '\r\n'	,'mustuse'	: 0	},
							{	'command'	: 'QUIT'			, 'datatype'	: None		, 'default'	: None	, 'recv'	: 0	, 'endw' : '\r\n'	,'mustuse'	: 0	}
						]
		}
# declaracion de protocolo 'smtp'
smtp =	{
			'proto'	:	'tcp'																			,
			'banner'	:	1																				,
			'comm'	:	[
	{	'command'	: 'EHLO '		, 'datatype'	: 'string'	, 'default'	: None								, 'recv'	: 1, 'endw' : '\r\n'	,'mustuse'	: 0	},
	{	'command'	: 'HELO '		, 'datatype'	: 'string'	, 'default'	: 'fuzzer.net-twister.com.ar'	, 'recv'	: 1, 'endw' : '\r\n'	,'mustuse'	: 1	},
	{	'command'	: 'MAILFROM: '	, 'datatype'	: 'string'	, 'default'	: 'vulndev@net-twister.com.ar', 'recv'	: 1, 'endw' : '\r\n'	,'mustuse'	: 1	},
	{	'command'	: 'RCPTTO: '	, 'datatype'	: 'string'	, 'default'	: 'vulndev@net-twister.com.ar', 'recv'	: 1, 'endw' : '\r\n'	,'mustuse'	: 1	},
	{	'command'	: 'RSET'			, 'datatype'	: None		, 'default'	: None								, 'recv'	: 1, 'endw' : '\r\n'	,'mustuse'	: 0	}
							]
			}
# declaracion de protocolo 'pop3'
pop3 =	{
			'proto'	:	'tcp'																			,
			'banner'	:	1																				,
			'comm'	:	[
								{	'command'	: 'USER '		, 'datatype'	: 'string'	, 'default'	: 'ftp'	, 'recv'	: 1	, 'endw' : '\r\n'	,'mustuse'	: 1	},
								{	'command'	: 'PASS '		, 'datatype'	: 'string'	, 'default'	: 'ftp'	, 'recv'	: 1	, 'endw' : '\r\n'	,'mustuse'	: 1	},
								{	'command'	: 'STAT '		, 'datatype'	: None		, 'default'	: None	, 'recv'	: 1	, 'endw' : '\r\n'	,'mustuse'	: 0	},
								{	'command'	: 'LIST '		, 'datatype'	: 'int'		, 'default'	: None	, 'recv'	: 1	, 'endw' : '\r\n'	,'mustuse'	: 0	},
								{	'command'	: 'RETR '		, 'datatype'	: 'int'		, 'default'	: None	, 'recv'	: 1	, 'endw' : '\r\n'	,'mustuse'	: 0	},
								{	'command'	: 'DELE '		, 'datatype'	: 'int'		, 'default'	: None	, 'recv'	: 1	, 'endw' : '\r\n'	,'mustuse'	: 0	},
								{	'command'	: 'NOOP '		, 'datatype'	: None		, 'default'	: None	, 'recv'	: 1	, 'endw' : '\r\n'	,'mustuse'	: 0	},
								{	'command'	: 'APOP '		, 'datatype'	: 'string'	, 'default'	: None	, 'recv'	: 1	, 'endw' : '\r\n'	,'mustuse'	: 0	},
								{	'command'	: 'TOP '			, 'datatype'	: 'int'		, 'default'	: None	, 'recv'	: 1	, 'endw' : '\r\n'	,'mustuse'	: 0	},
								{	'command'	: 'UIDL '		, 'datatype'	: 'int'		, 'default'	: None	, 'recv'	: 1	, 'endw' : '\r\n'	,'mustuse'	: 0	},
								{	'command'	: 'RSET '		, 'datatype'	: None		, 'default'	: None	, 'recv'	: 1	, 'endw' : '\r\n'	,'mustuse'	: 0	},
								{	'command'	: 'QUIT'			, 'datatype'	: None		, 'default'	: None	, 'recv'	: 0	, 'endw' : '\r\n'	,'mustuse'	: 0	}
							]
			}
# protocolos conocidos por net-twister
protoname =	{
				'smtp'	: smtp,
				'ftp'		: ftp,
				'pop3'	: pop3
				}
