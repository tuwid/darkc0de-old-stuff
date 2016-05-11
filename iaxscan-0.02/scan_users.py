'''
The contents of this file are subject to the Mozilla Public License
Version 1.1 (the "License"); you may not use this file except in
compliance with the License. You may obtain a copy of the License at
http://www.mozilla.org/MPL/

Software distributed under the License is distributed on an "AS IS"
basis, WITHOUT WARRANTY OF ANY KIND, either express or implied. See the
License for the specific language governing rights and limitations
under the License.

The Original Code is iaxscan, v0.02, 9th October 2008.

The Initial Developer of the Original Code is nnp, http://www.unprotectedhex.com
'''

import sys
from scanner import UserScanner
from optparse import OptionParser

optParser = OptionParser()
optParser.add_option('-i', '--host', dest='host', help='The host to target with the scan')
optParser.add_option('-p', '--port', dest='port', default='4569', help='(Optional, \
default=4569) The port to target with the scan')
optParser.add_option('-s', '--start-user', dest='startUser', help='The first username in the sequence \
to include in the scan')
optParser.add_option('-e', '--end-user', dest='endUser', help='The last username in the sequence \
to include in the scan')
optParser.add_option('-v', '--verbosity', dest='verbosity', default=5, help='(Optional, default=5) \
Can be 0, 5 or 10. Increase for more verbose logging')

(options, args) = optParser.parse_args()

if options.host == None:
    optParser.print_help()
    print '[!] A target host (-i) must be specified'
    sys.exit(-1)
    
if options.startUser == None:
    optParser.print_help()
    print '[!] A start user (-s) must be specified'
    sys.exit(-1)
    
startUser = int(options.startUser)

if options.endUser == None:
    optParser.print_help()
    print '[!] An end user (-e) must be specified'
    sys.exit(-1)

endUser = int(options.endUser)
    
u = UserScanner(int(options.verbosity))
targetTuple = (options.host, int(options.port))
u.scan(targetTuple, userRange=(startUser, endUser))
print '=+='*20
print 'The following %d users were found at %s' % (len(u.liveUsers), str(targetTuple))
for uname in u.liveUsers:
    print uname
    
