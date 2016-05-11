#!/usr/bin/python
#
# Sample code for using Pcap module
#
# written by Aaron Rhodes, 11 Nov 98
#
#
import time
import Pcap
import sys
import string
from threading import *

def c2h(character):
    return(string.upper("%02x" % ord(character)))

def decode_ether(packet):
    eth_dst = packet[:6]
    eth_src = packet[6:12]
    print "ETH_SRC: " + string.join(map(c2h,eth_src),':'),
    print "ETH_DST: " + string.join(map(c2h,eth_dst),':')
    rest_of_packet = packet[12:]
    a = string.join(map(c2h,rest_of_packet),' ')
    print a

#
# This function is the callback every packet gets passed to
#
def packet_printer(p_len,packet):
    # Increment the packet count
    global packetcount
    packetcount = packetcount + 1
    print "%06d" % packetcount,
    decode_ether(packet)


#
# Check usage
#
if len(sys.argv) < 2:
    print "Usage: " + sys.argv[0] + " <device>" + " [ filter ] "
    sys.exit(1)

packetcount = 0

##
## Set the device to capture packets from
##

pcap_dev = sys.argv[1]

filter_string = string.join (sys.argv[2:])
print "Filter string: ",filter_string

errbuf = ''

NON_PROMISCUOUS =  0
PROMISCUOUS     =  1
FOREVER         = -1

p          = Pcap.open_live(pcap_dev,100,NON_PROMISCUOUS,1500,errbuf)
bpf_prog   = Pcap.bpfprog_new()
bpf_filter = Pcap.compile(p,bpf_prog,filter_string,0,0)
Pcap.setfilter(p,bpf_prog)
Pcap.loop (p,FOREVER,packet_printer)

