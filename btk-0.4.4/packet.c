/*
    Billy the Kid (packet.c)
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

#include "wrap.h"
#include "packet.h"

/* never seen this routine before? get a life! >;) */
unsigned short
in_cksum (unsigned short *ptr, int nbytes)
{
  register long sum;
  u_short oddbyte;
  register u_short answer;
  sum = 0;
  while (nbytes > 1)
    {
      sum += *ptr++;
      nbytes -= 2;
    }
  if (nbytes == 1)
    {
      oddbyte = 0;
      *((u_char *) & oddbyte) = *(u_char *) ptr;
      sum += oddbyte;
    }
  sum = (sum >> 16) + (sum & 0xffff);
  sum += (sum >> 16);
  answer = ~sum;
  return (answer);
}

void
fill_ip_headers(btk_object *self) 
{
	struct in_addr srcip, dstip;
        srcip.s_addr = inet_addr(self->srcip);
        dstip.s_addr = inet_addr(self->dstip);	

	if (self->protocol == TCP || self->protocol==UDP) {
		self->pseudo->saddr = srcip.s_addr;
 		self->pseudo->daddr = dstip.s_addr;
		self->pseudo->protocol=self->protocol;
	}
        
       	self->iph->ip_src = srcip;
       	self->iph->ip_dst = dstip;
        self->iph->ip_hl = 5;        /* header length */
        self->iph->ip_v = 4;         /* version */
	self->iph->ip_len = htons(self->packet_length);
	self->iph->ip_p = (u_int8_t)self->protocol;

	if(self->id) self->iph->ip_id = htons(self->id);
        else self->iph->ip_id = htons(_IP_ID);      /* identification */

	if(self->off) self->iph->ip_off = htons(self->off);
	else self->iph->ip_off = htons(_IP_OFF);
	
	if(self->tos) self->iph->ip_tos = htons(self->tos);
	else self->iph->ip_tos = htons(_IP_TOS);

	if(self->ttl) self->iph->ip_ttl = self->ttl;
	else self->iph->ip_ttl = _IP_TTL;

        self->iph->ip_p = (u_int8_t)self->protocol;
}

void
fill_tcp_headers(btk_object *self)
{
	u_long length = (u_long)self->data_length;
	int i;
	self->packet_length = sizeof(struct ip) + sizeof(struct tcphdr) + length;
	fill_ip_headers(self); /* don't forget the ip-headers */

	self->pseudo->length = htons(sizeof (struct tcphdr)+ length);
	
	self->tcph->th_x2 = 0;
        self->tcph->th_off = 5;
        self->tcph->th_flags = self->flags;
        self->tcph->th_sport = htons(self->srcport);
        self->tcph->th_dport = htons(self->dstport);

	if(self->win) self->tcph->th_win = htons(self->win);
	else self->tcph->th_win = _TCP_WIN;

	if(self->urp) self->tcph->th_urp = htons(self->urp);
	else self->tcph->th_urp = _TCP_URP;

	if(self->ack) self->tcph->th_ack = htonl(self->ack);
	else self->tcph->th_ack = _TCP_ACK;

	if(self->seq) self->tcph->th_seq=htonl(self->seq);
	else self->tcph->th_seq = random();
	
	/* copy data to packet.. */
	for (i=0;i<self->data_length;i++) {
		memcpy(self->data+i, *(&self->tmpdata)+i, 1);
	
	}
	for (i=0;i<self->data_length;i++) {
		memcpy(self->packet + sizeof(struct ip) + sizeof(struct tcphdr)+
			sizeof(struct pseudo)+i, (self->data)+i, 1);
	}                 

	/* let's checksumm the packet */
        self->tcph->th_sum = in_cksum((unsigned short *) self->pseudo, length +
                                sizeof(struct pseudo)+sizeof(struct tcphdr));
	memcpy(self->pseudo, self->tcph,sizeof(struct tcphdr)+length);
}

void
fill_udp_headers(btk_object *self)
{
	u_long length = (u_long)self->data_length;
	int i;
	self->packet_length = sizeof(struct ip) + sizeof(struct udphdr) + length;
	fill_ip_headers(self); /* don't forget the ip-headers */

	self->pseudo->length = htons(sizeof(struct udphdr)+ length);

	self->udph->uh_sport = htons(self->srcport);
	self->udph->uh_dport = htons(self->dstport);
	self->udph->uh_ulen = htons(sizeof(struct udphdr)+ length);
	
	/* copy data to packet.. */
	for (i=0;i<self->data_length;i++) {
		memcpy(self->data+i, *(&self->tmpdata)+i, 1);
	
	}
	for (i=0;i<self->data_length;i++) {
		memcpy(self->packet + sizeof(struct ip) + sizeof(struct udphdr)+
			sizeof(struct pseudo)+i, (self->data)+i, 1);
	}                 

	/* let's checksum this packet */
	self->udph->uh_sum = in_cksum((unsigned short*) self->pseudo, length +
				sizeof(struct pseudo)+sizeof(struct udphdr));

	memcpy(self->pseudo, self->udph, sizeof(struct udphdr)+length);
}

void
set_icmp_id_and_seq(btk_object *self, char * help)
{
	long help2;
	help2 = htons(self->icmpid);
	if (self->icmpid)
		memcpy(*(&help)-sizeof(u_int32_t), &help2, sizeof(u_int16_t));
	help2 = htons(self->icmpseq);
	if (self->icmpseq);
		memcpy(*(&help)-sizeof(u_int16_t), &help2, sizeof(u_int16_t));
}

void
fill_icmp_headers(btk_object *self)
{
	u_long length = (u_long)self->data_length;
	int i, extra_size;
	char * help;
	long long help2;
	self->packet_length = sizeof(struct ip) + sizeof(struct icmphdr) + length;
	fill_ip_headers(self); /* don't forget the ip-headers */

	if (self->type) self->icmph->type = self->type;
	else self->icmph->type = 0;
	if (self->code) self->icmph->code = self->code;
	else self->icmph->code = 0;

	switch(self->type) {
	
	/* Redirect */
	case(5):
		help = (char *)self->data;
		if (self->gateway) {
			help2 = inet_addr(self->gateway);
			memcpy(*(&help)-sizeof(u_int32_t), &help2, sizeof(u_int32_t));
		}
		extra_size = 0;
		break;
	case(3):
	case(4):
	case(10):
	case(11):
		self->data = (char *) (self->packet + sizeof(struct ip) +
				sizeof(struct icmphdr) - sizeof(u_int32_t));
		extra_size = 0 - sizeof(u_int32_t);
		self->packet_length += extra_size;	
		break;
		
	/* Router advertisement */
	case(9):
		help = (char *)self->data;
		if (self->no_addresses)
			memcpy(*(&help)-sizeof(u_int32_t), &self->no_addresses, 
				sizeof(u_int8_t));
		if (self->entry_size)
			memcpy(*(&help)-sizeof(u_int16_t)-sizeof(u_int8_t), 
				&self->entry_size,
				sizeof(u_int8_t));
		if (self->lifetime) {
			self->lifetime = htons(self->lifetime);
			memcpy(*(&help)-sizeof(u_int16_t), &self->lifetime, 
				sizeof(u_int16_t));
			}
		extra_size = 0;
		break;
		
	/* Parameter problem */
	case(12):
		help = (char *)self->data;
		if (self->pointer)
			memcpy(*(&help)-sizeof(u_int32_t), &self->pointer, 
				sizeof(u_int8_t));
		extra_size = 0 - sizeof(u_int16_t) - sizeof(u_int8_t);
		self->packet_length += extra_size;
		break;
		
	/* Timestamp request & reply */
	case(13):
	case(14):
		help = (char *)self->data;
		self->data = (char *) (self->packet + sizeof(struct ip) +
				sizeof(struct icmphdr) + 3*sizeof(u_int32_t));
		if (self->time_originate)
			memcpy(help, &self->time_originate, sizeof(u_int32_t));	
		if (self->time_receive)
			memcpy(*(&help)+sizeof(u_int32_t), &self->time_receive, 
				sizeof(u_int32_t));
		if (self->time_transmit)
			memcpy(*(&help)+2*sizeof(u_int32_t), &self->time_transmit, 
				sizeof(u_int32_t));
		set_icmp_id_and_seq(self, help);
		extra_size = 3*sizeof(u_int32_t);
		self->packet_length += extra_size;
		break;
	
	/* Address mask request & reply */
	case(17):
	case(18):
		help = (char *)self->data;
		self->data = (char *) (self->packet + sizeof(struct ip) +
				sizeof(struct icmphdr) + sizeof(u_int32_t));
		if (self->address_mask) {
			help2 = inet_addr(self->address_mask);
			memcpy(help, &help2, 4);
		}
		set_icmp_id_and_seq(self, help);
		extra_size = sizeof(u_int32_t);
		self->packet_length += extra_size;
		break;
		
	/* Ping request and reply */
	case(0):
	case(8):
	case(15):
	case(16):
		help = (char *)self->data;
		set_icmp_id_and_seq(self, help);
		extra_size = 0;
		break;
	default:
		extra_size = 0;
		break;
	}

	/* copy data to packet */
	for (i=0;i<self->data_length;i++) {
		memcpy(self->data+i, *(&self->tmpdata)+i, 1);
	
	}
	for (i=0;i<self->data_length;i++) {
		memcpy(self->packet + sizeof(struct ip) + sizeof(struct icmphdr)+
			i+extra_size, (self->data)+i, 1);
	}
	
	/* let's checksum this packet */
	self->icmph->checksum = in_cksum((unsigned short*) self->icmph, length +
				sizeof(struct icmphdr)+extra_size);

	if (help)
		self->data = (char *) (self->packet + sizeof(struct ip) +
				sizeof(struct icmphdr));
}

int
disas_packet(char *pkt)
{
	const struct ether_header * eth;
	const struct ip * iph;
	const struct tcphdr * tcph;
	const char * payload;

	eth = (struct ether_header *)pkt;
	iph = (struct ip *)(pkt + sizeof(struct ether_header));
	tcph = (struct tcphdr *)(pkt + sizeof(struct ether_header) + \
							sizeof(struct ip));
	payload = (char *)(pkt + sizeof(struct ether_header) + \
							sizeof(struct ip) + sizeof(tcph));	

	printf("%s\n", payload);
return 0; /* -1 on error */
} 
