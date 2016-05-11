from pydbg import *

dbg = pydbg()

test = dbg.dll_inject("C:\injecteddll.dll",5316)

print "Returned Thread ID: %08x" % test