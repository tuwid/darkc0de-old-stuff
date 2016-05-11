PyFault - 0.1a
--------------
Author: Justin Seitz <jms@bughunter.ca> - VDA Labs LLC.

PyFault is a python library aimed at fault injection scenarios in Win32 based applications. Currently it 
only implements a DLL injection and ejection mechanism, but we aim to add more functionality to it,and 
of course all requests are welcome.


Usage
-----

from pyfault import *

fault = pyfault()

pid = 1234

injected = fault.inject_dll("C:\injecteddll.dll",pid)

if injected == True:
    print "We succesfully injected our DLL, gonna eject that business now."
    ejected = fault.eject_dll("injecteddll.dll",pid)
    print "Result of ejection: %s" % ejected




Included
---------

injecteddll.dll - this is a simple test DLL, it merely calls MessageBoxA() and outputs a message.


Requirements
------------

Python 2.4.x
ctypes (http://superb-east.dl.sourceforge.net/sourceforge/ctypes/ctypes-0.9.9.6.win32-py2.4.exe)


Contact
-------
Justin Seitz <jms@bughunter.ca>
Jared DeMott <jdemott@vdalabs.com>