/*
    Billy the Kid (btk-pcap.h)
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
	On some platforms/kernels the .stats() method seems to be broken, thuz its
	not compiled in on a default install. Uncomment BTK_USE_STATS to make sure
	it gets compiled in. Please note that .stats() is always defined so it dont
	breaks portable programs, but in that case it always returns (0,0). 
*/ 

/* #define BTK_USE_STATS */ 

staticforward PyTypeObject pcap_object_type;

/* Python 'backgrounded' functions are defined here */
pcap_object * new_pcap_object(PyObject *args);
static void pcap_object_dealloc(pcap_object *);
static PyObject * pcap_object_getattr(pcap_object *, char *);
static int pcap_object_setattr(pcap_object *, char *, PyObject *);

/* misc helping functions */
void wrap_callback(u_char *, const struct pcap_pkthdr *, const u_char *);
void pcap_object_reset(pcap_object *); 

/* proto-typing from public methods in the pcap-class */ 
static PyObject * pcap_object_lookupdev(pcap_object *, PyObject *);
static PyObject * pcap_object_loop(pcap_object *, PyObject *);
static PyObject * pcap_object_open_live(pcap_object *, PyObject *);
static PyObject * pcap_object_dispatch(pcap_object *, PyObject *);
static PyObject * pcap_object_lookupnet(pcap_object *, PyObject *);
static PyObject * pcap_object_findalldevs(pcap_object *, PyObject *);
static PyObject * pcap_object_compile(pcap_object *, PyObject *);
static PyObject * pcap_object_setfilter(pcap_object *, PyObject *);
static PyObject * pcap_object_setnonblock(pcap_object *, PyObject *);
static PyObject * pcap_object_getnonblock(pcap_object *, PyObject *);
static PyObject * pcap_object_datalink(pcap_object *, PyObject *);
static PyObject * pcap_object_snapshot(pcap_object *, PyObject *);
static PyObject * pcap_object_next(pcap_object *, PyObject *);
static PyObject * pcap_object_close(pcap_object *, PyObject *);
static PyObject * pcap_object_stats(pcap_object *, PyObject *);
static PyObject * pcap_object_open_offline(pcap_object *, PyObject *);
static PyObject * pcap_object_dump_open(pcap_object *, PyObject *);
static PyObject * pcap_object_dump_close(pcap_object *, PyObject *);
static PyObject * pcap_object_dump(pcap_object *, PyObject *);
static PyObject * pcap_object_minor_version(pcap_object *, PyObject *);
static PyObject * pcap_object_major_version(pcap_object *, PyObject *);
static PyObject * pcap_object_is_swapped(pcap_object *, PyObject *);
static PyObject * pcap_object_disas_packet(pcap_object *, PyObject *);

/* methods of the pcap-class */
static PyMethodDef pcap_obj_methods[] = {
	{"loop", (PyCFunction)pcap_object_loop, METH_VARARGS},
	{"dispatch", (PyCFunction)pcap_object_dispatch, METH_VARARGS},
	{"open_live", (PyCFunction)pcap_object_open_live, METH_VARARGS},
	{"lookupdev", (PyCFunction)pcap_object_lookupdev, METH_VARARGS},
	{"lookupnet", (PyCFunction)pcap_object_lookupnet, METH_VARARGS},
	{"findalldevs", (PyCFunction)pcap_object_findalldevs, METH_VARARGS},
	{"compile", (PyCFunction)pcap_object_compile, METH_VARARGS},
	{"setfilter", (PyCFunction)pcap_object_setfilter, METH_VARARGS},
	{"setnonblock", (PyCFunction)pcap_object_setnonblock, METH_VARARGS},
	{"getnonblock", (PyCFunction)pcap_object_getnonblock, METH_VARARGS},
	{"setfilter", (PyCFunction)pcap_object_setfilter, METH_VARARGS},
	{"datalink", (PyCFunction)pcap_object_datalink, METH_VARARGS},
	{"snapshot", (PyCFunction)pcap_object_snapshot, METH_VARARGS},
	{"next", (PyCFunction)pcap_object_next, METH_VARARGS},
	{"close", (PyCFunction)pcap_object_close, METH_VARARGS},
	{"stats", (PyCFunction)pcap_object_stats, METH_VARARGS},
	{"open_offline", (PyCFunction)pcap_object_open_offline, METH_VARARGS},
	{"dump_open", (PyCFunction)pcap_object_dump_open, METH_VARARGS},	
	{"dump", (PyCFunction)pcap_object_dump, METH_VARARGS},
	{"dump_close", (PyCFunction)pcap_object_dump_close, METH_VARARGS},
	{"is_swapped", (PyCFunction)pcap_object_is_swapped, METH_VARARGS},
	{"major_version", (PyCFunction)pcap_object_major_version, METH_VARARGS},
	{"minor_version", (PyCFunction)pcap_object_minor_version, METH_VARARGS},
	{"disas_packet", (PyCFunction)pcap_object_disas_packet, METH_VARARGS},
	{NULL, NULL}
};

/* define some error strings */
#define ERR_OPEN_LIVE 		"No valid open_*() called!"
#define ERR_0_OR_1 			"Specify 0 or 1!"
#define ERR_CALLABLE 		"Specified object not callable!"
#define ERR_NO_COMPILE		"No valid compile() called!" 
#define ERR_NO_DUMP			"No dump-file opened!"
#define ERR_ALREADY_DUMP	"A dump-file is already opened!"

/* thanks to /usr/include/net/bpf.h */
char * DL[15] = {
	"No link-layer encapsulation",
	"Ethernet (10MB)",
	"Experimental Ethernet (3Mb)",
	"Amateur Radio AX.25",
	"Proteon ProNET Token Ring", 
	"Chaos",
	"IEEE 802 Networks", 
	"ARCNET",
	"Serial Line IP", 
	"Point-to-point Protocol",
	"FDDI",
	"LLC/SNAP encapsulated atm", 
	"Raw IP",
	"BSD/OS Serial Line IP",
	"BSD/OS Point-to-point Protocol"
};

#define __DATA_LINK(x) DL[x]
#define DATA_LINK(x) __DATA_LINK(((x) < 16 && (x) >= 0))

