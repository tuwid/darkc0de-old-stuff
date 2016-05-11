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
from scanner import HostScanner
from optparse import OptionParser

optParser = OptionParser()
optParser.add_option('-i', '--ip-range', dest='ipRange', help='The range of IP addresses to scan in the form of \
a single IP or a list like 192.168.3-5.100-150')
optParser.add_option('-p', '--port', dest='port', default=4569, help='(Optional, default=4569) The port to send requests to')
optParser.add_option('-v', '--verbosity', dest='verbosity', default=5, help='(Optional, default=5) \
Can be 0, 5 or 10. Increase for more verbose logging')

(options, args) = optParser.parse_args()

if options.ipRange == None:
    optParser.print_help()
    print '[!] A target host (-i) must be specified'
    sys.exit(-1)

targetString = options.ipRange 
targetList = []

octets = targetString.split('.')
octetGenList = [[], [], [], []]
for idx, octet in enumerate(octets):
    if octet.find('-') != -1:
        start, end = octet.split('-')
        octetGenList[idx] = range(int(start), int(end)+1)
    else:
        octetGenList[idx] = [octet]
        
for oct0 in octetGenList[0]:
    for oct1 in octetGenList[1]:
        for oct2 in octetGenList[2]:
            for oct3 in octetGenList[3]:
                targetList.append('.'.join([str(oct0), str(oct1), str(oct2), str(oct3)]))
    

hScanner = HostScanner(int(options.verbosity))
hScanner.scan(targetList, int(options.port))

print '=+='*20
print 'The following %d live hosts were found' % len(hScanner.liveHosts)
for host in hScanner.liveHosts:
    print host
