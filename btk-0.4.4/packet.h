/*
    Billy the Kid (packet.h)
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

#define __FAVOR_BSD
#include <arpa/inet.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <netinet/tcp.h>
#include <netinet/udp.h>
#include <netinet/ip_icmp.h>
#include <net/ethernet.h>
#include <sys/socket.h>

/* all default values filled in by packet.c
 if not user-defined! */
#define _IP_ID	0
#define _IP_TOS  0
#define _IP_OFF	0
#define _IP_TTL  40
#define _TCP_WIN 65535
#define _TCP_ACK 0
#define _TCP_URP 0

/* TCP flags */
#define FIN        0x01
#define SYN        0x02
#define RST        0x04
#define PUSH       0x08
#define ACK        0x10
#define URG        0x20
#define CWR	   0x40
#define ECN	   0x80

/* Supported protocols */
#define TCP 6
#define UDP 17
#define ICMP 1

/* pseudo header struct */
struct pseudo {
        u_long saddr;
        u_long daddr;
        u_char zero;
        u_char protocol;
        u_short length;
};

/* all packet.c function prototypes */
unsigned short in_cksum (unsigned short *, int);
void fill_ip_headers(btk_object *self);
void fill_tcp_headers(btk_object *self);
void fill_udp_headers(btk_object *self);
void fill_icmp_headers(btk_object *self);
