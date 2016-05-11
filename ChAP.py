#! /usr/bin/env python
"""
Script that tries to select the EMV Payment Systems Directory on all inserted cards.

Copyright 2008 RFIDIOt
Author: Adam Laurie, mailto:adam@algroup.co.uk
	http://rfidiot.org/ChAP.py

This file is based on an example program from scard-python.
  Originally Copyright 2001-2007 gemalto
  Author: Jean-Daniel Aussel, mailto:jean-daniel.aussel@gemalto.com

scard-python is free software; you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation; either version 2.1 of the License, or
(at your option) any later version.

scard-python is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with scard-python; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""

from smartcard.CardType import AnyCardType
from smartcard.CardRequest import CardRequest
from smartcard.CardConnection import CardConnection
from smartcard.CardConnectionObserver import ConsoleCardConnectionObserver
from smartcard.Exceptions import CardRequestTimeoutException

import getopt
import sys

# default global options
BruteforcePrimitives= False
BruteforceAID= False
BruteforceEMV= False
Debug= False
Protocol= CardConnection.T0_protocol
RawOutput= False
Verbose= False

# known AIDs
# please mail new AIDs to aid@rfidiot.org
KNOWN_AIDS= 	[
		['VISA',0xa0,0x00,0x00,0x00,0x03],
		['VISA Debit/Credit',0xa0,0x00,0x00,0x00,0x03,0x10,0x10],
		['VISA Credit',0xa0,0x00,0x00,0x00,0x03,0x10,0x10,0x01],
		['VISA Debit',0xa0,0x00,0x00,0x00,0x03,0x10,0x10,0x02],
		['VISA Electron',0xa0,0x00,0x00,0x00,0x03,0x20,0x10],
		['VISA Interlink',0xa0,0x00,0x00,0x00,0x03,0x30,0x10],
		['VISA Plus',0xa0,0x00,0x00,0x00,0x03,0x80,0x10],
		['VISA ATM',0xa0,0x00,0x00,0x00,0x03,0x99,0x99,0x10],
		['MASTERCARD',0xa0,0x00,0x00,0x00,0x04,0x10,0x10],
		['Maestro',0xa0,0x00,0x00,0x00,0x04,0x30,0x60],
		['Maestro UK',0xa0,0x00,0x00,0x00,0x05,0x00,0x01],
		['Maestro TEST',0xb0,0x12,0x34,0x56,0x78],
		['Self Service',0xa0,0x00,0x00,0x00,0x24,0x01],
		['American Express',0xa0,0x00,0x00,0x00,0x25],
		['ExpressPay',0xa0,0x00,0x00,0x00,0x25,0x01,0x07,0x01],
		['Link',0xa0,0x00,0x00,0x00,0x29,0x10,0x10],
	     	['Alias AID',0xa0,0x00,0x00,0x00,0x29,0x10,0x10],
	    	]

# define the apdus used in this script
GET_RESPONSE = [0x00, 0xC0, 0x00, 0x00 ]
SELECT = [0x00, 0xA4, 0x04, 0x00]
DF_PSE = [0x31, 0x50, 0x41, 0x59, 0x2E, 0x53, 0x59, 0x53, 0x2E, 0x44, 0x44, 0x46, 0x30, 0x31]
READ_RECORD = [0x00, 0xb2]
GET_DATA = [0x80, 0xca]
UNBLOCK_PIN= [0x84,0x24,0x00,0x00,0x00]
#BRUTE_AID= [0xa0,0x00,0x00,0x00]
BRUTE_AID= []

# define tags for response
BINARY= 0
TEXT= 1
BER_TLV= 2
NUMERIC= 3
MIXED= 4
TEMPLATE= 0
ITEM= 1
SFI= 0x88
TAGS= 	{	
	0x4f:['Application Identifier (AID)',BINARY,ITEM],
	0x50:['Application Label',TEXT,ITEM],
	0x57:['Track 2 Equivalent Data',BINARY,ITEM],
	0x5a:['Application Primary Account Number (PAN)',NUMERIC,ITEM],
	0x6f:['File Control Information (FCI) Template',BINARY,TEMPLATE],
	0x70:['Record Template',BINARY,TEMPLATE],
	0x82:['Application Interchange Profile',BINARY,ITEM],
	0x84:['DF Name',MIXED,ITEM],
	0x87:['Application Priority Indicator',BINARY,ITEM],
	0x88:['Short File Identifier',BINARY,ITEM],
	0x8c:['Card Risk Management Data Object List 1 (CDOL1)',BINARY,ITEM],
	0x8d:['Card Risk Management Data Object List 2 (CDOL2)',BINARY,ITEM],
	0x8e:['Cardholder Verification Method (CVM) List',BINARY,ITEM],
	0x8f:['Certification Authority Public Key Index',BINARY,ITEM],
	0x94:['Application File Locator',BINARY,ITEM],
	0xa5:['Proprietary Information',BINARY,TEMPLATE],
	0x5f20:['Cardholder Name',TEXT,ITEM],
	0x5f24:['Application Expiration Date YYMMDD',NUMERIC,ITEM],
	0x5f25:['Application Effective Date YYMMDD',NUMERIC,ITEM],
	0x5f28:['Issuer Country Code',NUMERIC,ITEM],
	0x5f2d:['Language Preference',TEXT,ITEM],
	0x5f30:['Service Code',NUMERIC,ITEM],
	0x5f34:['Application Primary Account Number (PAN) Sequence Number',NUMERIC,ITEM],
	0x5f50:['Issuer URL',TEXT,ITEM],
	0x9f05:['Application Discretionary Data',BINARY,ITEM],
	0x9f07:['Application Usage Control',BINARY,ITEM],
	0x9f08:['Application Version Number',BINARY,ITEM],
	0x9f0d:['Issuer Action Code - Default',BINARY,ITEM],
	0x9f0e:['Issuer Action Code - Denial',BINARY,ITEM],
	0x9f0f:['Issuer Action Code - Online',BINARY,ITEM],
	0x9f11:['Issuer Code Table Index',BINARY,ITEM],
	0x9f12:['Application Preferred Name',TEXT,ITEM],
	0x9f1f:['Track 1 Discretionary Data',TEXT,ITEM],
	0x9f20:['Track 2 Discretionary Data',TEXT,ITEM],
	0x9f26:['Application Cryptogram',BINARY,ITEM],
	0x9f42:['Application Currency Code',NUMERIC,ITEM],
	0x9f44:['Application Currency Exponent',NUMERIC,ITEM],
	0x9f4a:['Static Data Authentication Tag List',BINARY,ITEM],
	0xbf0c:['File Control Information (FCI) Issuer Discretionary Data',BINARY,TEMPLATE],
	}

# define BER-TLV tags
TLV_CLASS_MASK= 0xc0
TLV_DATA_MASK= 0x20
TLV_TAG_MASK= 0x1f

TLV_CLASS_TAGS= {	
		0x00:'Universal class',
		0x40:'Application class',
		0x80:'Context-specific class',
		0xc0:'Private class',
		}

TLV_DATA_TAGS= 	{
		0x00:'Primitive data object',
		0x01:'Constructed data object',
		}

# define SW1 return values
SW1_RESPONSE_BYTES= 0x61
SW1_WRONG_LENGTH= 0x6c
SW12_OK= [0x90,0x00]
SW12_NOT_FOUND= [0x6a,0x82]

# define GET_DATA primitive tags
PIN_TRY_COUNTER= [0x9f,0x17]
ATC= [0x9f,0x36]
LAST_ATC= [0x9f,0x13]
LOG_FORMAT= [0x9f, 0x4f]

def printhelp():
	print '\nOptions:\n'
	print '\t-a\t\tBruteforce AIDs'
	print '\t-A\t\tPrint list of known AIDs'
	print '\t-d\t\tDebug - Show PC/SC APDU data'
	print '\t-e\t\tBruteforce EMV AIDs'
	print '\t-h\t\tPrint detailed help message'
	print '\t-p\t\tBruteforce primitives and files'
	print '\t-r\t\tRaw output - do not interpret EMV data'
	print '\t-t\t\tUse T1 protocol (default is T0)'
	print '\t-v\t\tVerbose on'
        print

def hexprint(data):
	index= 0

	while index < len(data):
		print '%02x' % data[index],
		index += 1
	print

def get_tag(data,req):
	"return a tag's data if present"

	index= 0

	# walk the tag chain to ensure no false positives
	while index < len(data):
		try:
			# try 1-byte tags
			tag= data[index]	
			TAGS[tag]
			taglen= 1
		except:
			try:
				# try 2-byte tags
				tag= data[index] * 256 + data[index+1]
				TAGS[tag]
				taglen= 2
			except:
				# tag not found
				index += 1
				continue
		if tag == req:
			itemlength= data[index + taglen]
			index += taglen + 1
			return True, itemlength, data[index:index + itemlength]
		else:
			index += taglen + 1
	return False,0,''

def isbinary(data):
	index= 0

	while index < len(data):
		if data[index] < 0x20 or data[index] > 0x7e:
			return True
		index += 1
	return False

def decode_pse(data):
	"decode the main PSE select response"

	index= 0
	indent= ''

	if RawOutput:
		hexprint(data)
		textprint(data)
		return

	while index < len(data):
		try:
			tag= data[index]
			TAGS[tag]
			taglen= 1
		except:
			try:
				tag= data[index] * 256 + data[index+1]
				TAGS[tag]
				taglen= 2
			except:
				print indent + '  Unrecognised TAG:', 
				hexprint(data[index:])
				return
		print indent + '  %0x:' % tag, TAGS[tag][0],
		itemlength= data[index + taglen]
		print '(%d bytes):' % itemlength,
		offset= 1
		out= ''
		mixedout= []
		while itemlength > 0:
			if TAGS[tag][1] == BINARY:
					if TAGS[tag][2] != TEMPLATE or Verbose:
						print '%02x' % data[index + taglen + offset],
			else: 
				if TAGS[tag][1] == NUMERIC:
					out += '%02x' % data[index + taglen + offset]
				else:
					if TAGS[tag][1] == TEXT:
						out += "%c" % data[index + taglen + offset]
					if TAGS[tag][1] == MIXED:
						mixedout.append(data[index + taglen + offset])
			itemlength -= 1
			offset += 1
		if TAGS[tag][1] == MIXED:
			if isbinary(mixedout):
				hexprint(mixedout)
			else:
				textprint(mixedout)
		if TAGS[tag][1] == BINARY:
			print
		if TAGS[tag][1] == TEXT or TAGS[tag][1] == NUMERIC:
			print out
		if TAGS[tag][2] == ITEM:
			index += data[index + taglen] + taglen + 1
		else:
			index += taglen + 1
			indent += '   ' 

def textprint(data):
	index= 0
	out= ''

	while index < len(data):
		if data[index] >= 0x20 and data[index] < 0x7f:
			out += chr(data[index])
		else:
			out += '.'
		index += 1
	print out

def bruteforce_primitives():
	for x in range(256):
		for y in range(256):
			status, length, response= get_primitive([x,y])
			if status:
				print 'Primitive %02x%02x: ' % (x,y)
				if response:
					hexprint(response)
					textprint(response)

def get_primitive(tag):
	# get primitive data object - return status, length, data
	le= 0x00
	apdu = GET_DATA + tag + [le]
	response, sw1, sw2 = send_apdu(apdu)
	if response[0:2] == tag:
		length= response[2]
		return True, length, response[3:]
	else:
		return False, 0, ''

def check_return(sw1,sw2):
	if [sw1,sw2] == SW12_OK:
		return True
	return False

def send_apdu(apdu):
	# send apdu and get additional data if required 
	response, sw1, sw2 = cardservice.connection.transmit( apdu, Protocol )
	if sw1 == SW1_WRONG_LENGTH:
		# command used wrong length. retry with correct length.
		apdu= apdu[:len(apdu) - 1] + [sw2]
		return send_apdu(apdu)
	if sw1 == SW1_RESPONSE_BYTES:
		# response bytes available.
		apdu = GET_RESPONSE + [sw2]
		response, sw1, sw2 = cardservice.connection.transmit( apdu, Protocol )
	return response, sw1, sw2

def select_aid(aid):
	# select an AID and return True/False plus additional data
	apdu = SELECT + [len(aid)] + aid + [0x00]
	response, sw1, sw2= send_apdu(apdu)
	if check_return(sw1,sw2):
		if Verbose:
			decode_pse(response)
		return True, response, sw1, sw2
	else:
		return False, [], sw1,sw2

def bruteforce_aids(aid):
	#brute force two digits of AID
	print 'Bruteforcing AIDs'
	y= z= 0
	if BruteforceEMV:
		brute_range= [0xa0]
	else:
		brute_range= range(256)
	for x in brute_range:
		for y in range(256):
			for z in range(256):
				#aidb= aid + [x]
				aidb= [x,y,0x00,0x00,z]
				if Verbose:
					print '\r  %02x %02x %02x %02x %02x' % (x,y,0x00,0x00,z),
				status, response, sw1, sw2= select_aid(aidb)
				if [sw1,sw2] != SW12_NOT_FOUND:
					print '\r  Found AID:',
					hexprint(aidb)
					if status:
						decode_pse(response)
					else:
						print 'SW1 SW2: %02x %02x' % (sw1,sw2)

def dump_aid(aid):
		# now try and brute force records
		print '  Checking for records:'
		for y in range(1,31):
			for x in range(1,256):
				p1= x
				p2= (y << 3) + 4
				le= 0x00
				apdu= READ_RECORD + [p1] + [p2,le]
				response, sw1, sw2= send_apdu(apdu)
				if check_return(sw1,sw2):
					print "  Record %02x, File %02x: length %d" % (x,y,len(response))
					if Verbose:
						hexprint(response)
						textprint(response)
					decode_pse(response)
				else:
					if not BruteforcePrimitives:
						return

# main loop
aidlist= KNOWN_AIDS

try:
	# 'args' will be set to remaining arguments (if any)
	opts, args  = getopt.getopt(sys.argv[1:],'aAdeprtv')
	for o, a in opts:
		if o == '-a':
			BruteforceAID= True
		if o == '-A':
			print
			for x in range(len(aidlist)):
				print '% 20s: ' % aidlist[x][0],
				hexprint(aidlist[x][1:])
			print
			sys.exit(False)	
		if o == '-d':
			Debug= True
		if o == '-e':
			BruteforceAID= True
			BruteforceEMV= True
		if o == '-p':
			BruteforcePrimitives= True
		if o == '-r':
			RawOutput= True
		if o == '-t':
			Protocol= CardConnection.T1_protocol
		if o == '-v':
			Verbose= True

except getopt.GetoptError:
	# -h will also cause an exception as it doesn't exist!
	printhelp()
	sys.exit(False)

try:
	# request any card type
	cardtype = AnyCardType()
	# request card insertion
	print 'insert a card within 10s'
	cardrequest = CardRequest( timeout=10, cardType=cardtype )
	cardservice = cardrequest.waitforcard()




	# attach the console tracer
	if Debug:
		observer=ConsoleCardConnectionObserver()
    		cardservice.connection.addObserver( observer )


	# connect to the card
	cardservice.connection.connect(Protocol)

	# try to select PSE
	apdu = SELECT + [len(DF_PSE)] + DF_PSE
	response, sw1, sw2 = send_apdu( apdu )

	if check_return(sw1,sw2):
		# there is a PSE
		print 'PSE found!'
		decode_pse(response)
		if BruteforcePrimitives:
			# brute force primitives
			print 'Brute forcing primitives'
			bruteforce_primitives()
		status, length, psd= get_tag(response,SFI)
		if not status:
			print 'No PSD found!'
		else:
			print '  Checking for records:',
			if BruteforcePrimitives:
				psd= range(31)
				print '(bruteforce all files)'
			else:
				print
			for x in range(256):
				for y in psd:
					p1= x
					p2= (y << 3) + 4
					le= 0x00
					apdu= READ_RECORD + [p1] + [p2,le]
					response, sw1, sw2 = cardservice.connection.transmit( apdu )
					if sw1 == 0x6c:
						print "  Record %02x, File %02x: length %d" % (x,y,sw2)
						le= sw2
						apdu= READ_RECORD + [p1] + [p2,le]
						response, sw1, sw2 = cardservice.connection.transmit( apdu )
						print "  ",
						aid= ''
						if Verbose:
							hexprint(response)
							textprint(response)
						i= 0
						while i < len(response):
							# extract the AID
							if response[i] == 0x4f and aid == '':
								aidlen= response[i + 1]
								aid= response[i + 2:i + 2 + aidlen]
							i += 1
						print '   AID found:',
						hexprint(aid)
						aidlist.append(['PSD Entry']+aid)
	if BruteforceAID:
		bruteforce_aids(BRUTE_AID)
	if aidlist:
		# now try dumping the AID records
		current= 0
		while current < len(aidlist):
			if Verbose:
				print 'Trying AID: %s -' % aidlist[current][0],
				hexprint(aidlist[current][1:])
			selected, response, sw1, sw2= select_aid(aidlist[current][1:])
			if selected:
				if Verbose:
					print '  Selected: ',
					hexprint(response)
					textprint(response)
				else:
					print '  Found AID: %s -' % aidlist[current][0],
					hexprint(aidlist[current][1:])
				decode_pse(response)
				if BruteforcePrimitives:
					# brute force primitives
					print 'Brute forcing primitives'
					bruteforce_primitives()
				ret, length, pins= get_primitive(PIN_TRY_COUNTER)
				if ret:
					print '  PIN tries left:', pins[0]
				if pins == 0:
					print 'unblocking PIN'
					ret, sw1, sw2= send_apdu(UNBLOCK_PIN)
					hexprint([sw1,sw2])
				ret, length, atc= get_primitive(ATC)
				if ret:
					atcval= (atc[0] << 8) + atc[1]
					print '  Application Transaction Counter:', atcval
				ret, length, latc= get_primitive(LAST_ATC)
				if ret:
					latcval= (latc[0] << 8) + latc[1]
					print '  Last ATC:', latcval
				ret, length, logf= get_primitive(LOG_FORMAT)
				if ret:
					print 'Log Format: ',
					hexprint(logf)
				dump_aid(aidlist[current][1:])
				current += 1
			else:
				if Verbose:
					print '  Not found: %02x %02x' % (sw1,sw2)
				current += 1
	else:
		print 'no PSE: %02x %02x' % (sw1,sw2)

except CardRequestTimeoutException:
	print 'time-out: no card inserted during last 10s'


if 'win32'==sys.platform:
	print 'press Enter to continue'
	sys.stdin.read(1)
