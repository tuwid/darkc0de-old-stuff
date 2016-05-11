/*
    Billy the Kid (wrap.h)
    "..a python module to do all kinds of raw network shit..."

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

    by Gorny (gorny0@zonnet.nl)
    http://gorny.cjb.net
*/

/*
	Defining the btk_object and the pcap_object structs. Please note that 
	btk_object is, in fact, a stupid name and it could better be renamed to
	something like packet_object or something like that... 
*/

#include <Python.h>
#include <pcap.h>

/* very large struct.. needs work */
typedef struct {
        PyObject_HEAD
        PyObject        * btk_obj_attr; /* holds all Python attributes */
	int flags; /* holds flags which can be (un)set by user */
	int protocol; /* holds protocol number (eg. TCP=6) */
	int packet_length; /* length incl. all headers and data */
	int data_length; /* erh? */

	/* tcp options */
	u_int32_t seq; /* sequence number */
	u_int32_t ack; /* acknowledgement number */
	u_int16_t win;           /* window */
	u_int16_t urp;           /* urgent pointer */

	/* ip options */
	u_short off;   /* fragment offset field */
	u_short id; /* identification */
	u_int8_t ttl;  /* time to live */
	u_int8_t tos;  /* type of service */

	/* holding source and destination port and ip */
	int srcport; 
	int dstport;
	char * srcip;
	char * dstip;

	/* icmp options */
	u_int8_t type;
	u_int8_t code;
	char * gateway;
	char * address_mask;
	u_int32_t time_originate;
	u_int32_t time_receive;
	u_int32_t time_transmit;
	u_int8_t pointer;
	u_int8_t no_addresses;
	u_int8_t entry_size;
	u_int16_t lifetime;
	u_int16_t icmpid;
	u_int16_t icmpseq;

	/* (possible) packet contents */
	char * data;
	struct pseudo * pseudo;
	struct tcphdr * tcph;
	struct udphdr * udph;
	struct icmphdr * icmph;
	struct ip * iph;
	struct ether_header * etherh;
       
#define MAX_PACKET_LEN 65535
	u_char packet[MAX_PACKET_LEN];
	char tmpdata[MAX_PACKET_LEN]; /* preventing messing up of packet */
        
} btk_object;


typedef struct {
	PyObject_HEAD
	PyObject        * pcap_obj_attr;
	
	char *dev;  /* device to sniff on */
	char errbuf[PCAP_ERRBUF_SIZE];
	
	int no_packets;	 /* No. of packets to catch */
	PyObject * callback;	 /* pointer to the callback function */
	pcap_t * descr;  /* resembles the pcap-session */
	
	int promisc; /* set to non-zero if device in promiscuous mode */
	int timeout; /* timed in milli-seconds */
	int nonblock; 
	int snaplen; /* how many bytes should be snarfed ?? */
	
	bpf_u_int32 netp;
	bpf_u_int32 maskp;
	
	struct bpf_program fp; /* used by pcap_compile */
	struct pcap_pkthdr hdr;
	struct pcap_stat stats;
	pcap_dumper_t * dump;

	const char * pkt_data; /* pointer to packet data */	
	char * filter; /* filter string in tcpdump-style */
	char * file; /* holds the filename for offline pcapusage */
} pcap_object;
