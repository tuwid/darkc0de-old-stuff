#!/usr/bin/python
import dns.resolver
import dns.query
import dns.zone
import sys
import re

if len(sys.argv)!=2:
        print "Quick n Dirty DNS Zone Trasnfer tool"
        print "mati@see-security.com"
        print "Usage: ./dns-enum.py <domain name>"
        sys.exit(0)

print '\n##################################################'
print "# MX records found for",sys.argv[1]
print '##################################################\n'
try:
    mxanswers = dns.resolver.query(sys.argv[1], 'MX')
except dns.resolver.NoAnswer:
    print "Can't get MX records for", sys.argv[1]
    mxanswers=""
except:
	print "No such domain!"    
	sys.exit(0)
if mxanswers:    
    for mxdata in mxanswers:
        print 'MX', mxdata.exchange, 'has preference', mxdata.preference

    
print '\n##################################################'
print "# NS records found for",sys.argv[1]
print '##################################################\n'
try:
    nsanswers=dns.resolver.query(sys.argv[1], 'NS')
except dns.resolver.NoAnswer:
    print "Can't get NS records for", sys.argv[1]
    sys.exit(0)
    
for nsdata in nsanswers:
    print 'NS', nsdata

for nameserver in nsanswers:
    print '\n##################################################'
    print "# Trying Zone Transfer on",nameserver
    print '##################################################\n'
    
    try:
            z = dns.zone.from_xfr(dns.query.xfr(str(nameserver), sys.argv[1]))
    except:
        print "No Zone Transfer on",str(nameserver)
        continue
    names = z.nodes.keys()
    names.sort()
    for n in names:
        if not re.match('@',str(n)):
            print z[n].to_text(n)
print "\nDone!\n"
