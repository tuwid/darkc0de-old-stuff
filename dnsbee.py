#!/usr/bin/python
#
# Malformation's dnsbee.py
#
# Queries all record types in the DNS protocol.
# When a new one comes out, just add it to the list.
# Please note this script is really noisy, it can be easily seen
# via a rogue router or on a DNS server itself.
#
# Kisses go to .aware, OTW, STS, darkc0de, str0ke, some Aussies and anyone keeping the scene alive
# Please don't strip the credits out if you modify or redistribute.

import os, subprocess, sys

records = ["A","AAAA","AFSDB","CERT","CNAME","DHCID","DLV","DNAME",
        "DNSKEY","DS","IPSECKEY","KEY","LOC","MX","NAPTR","NS","NSEC",
        "NSEC3","PTR","RRSIG","SIG","SOA","SPF","SRV","SSHFP",
        "TXT","AXFR","OPT","TKEY","TSIG"] #"IXFR", "HIP" and "NSEC3PARAM", "TA" records are not included.

def usage():
	print sys.argv[0] + " host nameserver"

def main():
	file_name = "dnsbee.txt"
	dot = "."
	if (os.path.exists(file_name)):
		file = open(file_name,"a")
	else:
		file = open(file_name,"w")
	host = sys.argv[1]
	nameserver = sys.argv[2]
	print "Trying to query",
	for i in range(0,len(records)):
		string = "dig " + records[i] + " " + host + " @" + nameserver
		command = os.popen(string,"r")
		while(1):
			line = command.readline()
			#line = line.strip()
			if line:
				print ".",
				file.write("Query> " + string + ":\n")
				file.write(line)
			else:
				break

if __name__ == '__main__': #Thanks b14ck
	if (len(sys.argv) < 3):
			usage()
			sys.exit(1)
	main()

