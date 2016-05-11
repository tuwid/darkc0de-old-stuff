/*
    Billy the Kid (pcap.c)
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
	Based on some example codes around the net *and* the pylibpcap package
	which is an SWIG-generated wrapper to libpcap for Python. I want to make
	this package as independant as possible and didn't want to relie much on
	other obsolete, old and unmaintained packages.  

	It's based on libpcap 0.7.1 and it seems to work nicely. Please note that
	there are some pcap-functions not callable from within Python. This is 
	because they are only for internal use (like pcap_error() eg.) and btk takes
	care of all those things for you.

	-- Gorny 4/May/2002 
*/

#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <string.h>

#include "wrap.h"
#include "btk-pcap.h"

pcap_object *
new_pcap_object(PyObject *args) {
	pcap_object *self;
	self = PyObject_New(pcap_object, &pcap_object_type);
	if (self == NULL)
		return NULL;

	/* make sure everything is clean */
	pcap_object_reset(self);
	
	return self;
}

/*	
	Every time a new class is defined these lines of codes need to be
	rewritten. Isn't it possible to make a general class-handler which
	is capable of handling all objects? No special needs for it in btk, but
	certainly worth a try in the near future :) 
*/

static void
pcap_object_dealloc(pcap_object *self)
{
	Py_XDECREF(self->pcap_obj_attr);
	PyObject_Del(self);
}

static PyObject *
pcap_object_getattr(pcap_object *self, char *name)
{
	if (self->pcap_obj_attr != NULL) {
		PyObject *v = PyDict_GetItemString(self->pcap_obj_attr, name);
		if (v != NULL) {
			Py_INCREF(v);
			return v;
		}
	}
	return Py_FindMethod(pcap_obj_methods, (PyObject *)self, name);
}

static int
pcap_object_setattr(pcap_object *self, char *name, PyObject *v)
{
	if (self->pcap_obj_attr == NULL) {
		self->pcap_obj_attr = PyDict_New();
		if (self->pcap_obj_attr == NULL)
			return -1;
	}
	if (v == NULL) {
		int rv = PyDict_DelItemString(self->pcap_obj_attr, name);
		if (rv < 0)
			PyErr_SetString(PyExc_AttributeError,
				"delete non-existing pcap_obj attribute");
		return rv;
	}
	else
		return PyDict_SetItemString(self->pcap_obj_attr, name, v);
}

/* all references to the background methods are defined here */
statichere PyTypeObject pcap_object_type = {
	PyObject_HEAD_INIT(NULL)
	0,                      /*ob_size*/
	"pcap_object",
	sizeof(pcap_object),
	0,                      /*tp_itemsize*/
	(destructor)pcap_object_dealloc,
	0,                      /*tp_print*/
	(getattrfunc)pcap_object_getattr,
	(setattrfunc)pcap_object_setattr,
	0,                      /*tp_compare*/
	0,                      /*tp_repr*/
	0,                      /*tp_as_number*/
	0,                      /*tp_as_sequence*/
	0,                      /*tp_as_mapping*/
	0,                      /*tp_hash*/
};

/* 
*	The real work starts from here... owh boy, owh boy.. :) 
*/

static PyObject *
pcap_object_lookupdev(pcap_object *self, PyObject *args)
{
	self->dev = pcap_lookupdev(self->errbuf);
	
	if(self->dev == NULL) {
		PyErr_SetString(PyExc_StandardError,self->errbuf);	
		return NULL;
	}
	
	return PyString_FromString(self->dev);
}

void
pcap_object_reset(pcap_object *self)
{
	self->pcap_obj_attr = NULL;
	self->descr = NULL;
	self->dev = NULL;
	self->no_packets = 0;
	self->callback = NULL;
	self->promisc = 0;
	self->timeout = -1;
	self->nonblock = 0;		/* default */
	self->snaplen = BUFSIZ;  /* standard snaplen... usually 96 bytes */
	self->netp = 0;
	self->maskp = 0;
	self->filter = NULL;
	self->file = NULL;
	self->pkt_data = NULL;
	self->dump = NULL;	
	/* pcap_freecode(self->fp); Segmentation fault... aargh.. why???!? */

	/* dont cleanup timeval... this should be enough */
	self->hdr.caplen = 0;
	self->hdr.len = 0;
}

/* thanks to pylibpcap sources */
void
wrap_callback (u_char *PyObj, const struct pcap_pkthdr *header,
				const u_char *packetdata)
{
	PyObject *func, *arglist;
	pcap_object *self;
	unsigned int *len;
	self = (pcap_object *)PyObj;

	if (PyCallable_Check(self->callback)) {
		len    = (unsigned int *)&header->len;
		func = self->callback;
		arglist = Py_BuildValue("is#",*len,packetdata,*len);

		/* jump 2 callback with packetlength and headers as args */
		PyObject_CallObject(func, arglist);
		Py_DECREF(arglist);
	}
}

static PyObject *
pcap_object_loop(pcap_object *self, PyObject *args)
{
	if (!PyArg_ParseTuple(args, "iO:loop", &self->no_packets,
						&self->callback))
		return NULL;

	if (self->descr == NULL) {
		PyErr_SetString(PyExc_StandardError, ERR_OPEN_LIVE);
		return NULL;
	}

	if (!PyCallable_Check(self->callback)) {
		PyErr_SetString(PyExc_StandardError, ERR_CALLABLE);
		return NULL;
	}

	/* wrap_callback is used to parse the C stuff to Pythonic thingies */
	pcap_loop(self->descr, self->no_packets, wrap_callback, (char *)self);

	Py_INCREF(Py_None);
	return Py_None;
}

/* identical to pcap_object_loop() except for libpcap behaviour */
static PyObject *
pcap_object_dispatch(pcap_object *self, PyObject *args)
{
	if (!PyArg_ParseTuple(args, "iO:dispatch", &self->no_packets,
						&self->callback))
		return NULL;

	if (self->descr == NULL) {
		PyErr_SetString(PyExc_StandardError, ERR_OPEN_LIVE);
		return NULL;
	}

	if (!PyCallable_Check(self->callback)) {
		PyErr_SetString(PyExc_StandardError, ERR_CALLABLE);
		return NULL;
	}

	pcap_dispatch(self->descr, self->no_packets, wrap_callback, (char *)self);
	
	Py_INCREF(Py_None);
	return Py_None;
}


static PyObject *
pcap_object_open_live(pcap_object *self, PyObject *args)
{
	if (!PyArg_ParseTuple(args, "s|iii:open_live", &self->dev, &self->snaplen, 
			&self->promisc, &self->timeout))
		return NULL;

	if (self->promisc != 0 && self->promisc != 1) {
		PyErr_SetString(PyExc_StandardError, ERR_0_OR_1);
		return NULL;
	}

	if (self->snaplen < 0 || self->snaplen > 65536) /* just in case */
		self->snaplen = BUFSIZ;

	self->descr = pcap_open_live(self->dev, self->snaplen, self->promisc, 
									self->timeout, self->errbuf);
		
	if (self->descr == NULL) {
		PyErr_SetString(PyExc_StandardError, self->errbuf);
		return NULL;
	}

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
pcap_object_lookupnet(pcap_object *self, PyObject *args) 
{
	char * dev;
	char tmp1[16], tmp2[16];
	struct in_addr in;

	if (!PyArg_ParseTuple(args, "s:lookupnet", &dev))
		return NULL;

	if (pcap_lookupnet(dev, &self->netp, &self->maskp, self->errbuf)==-1) {
		PyErr_SetString(PyExc_StandardError, self->errbuf);
		return NULL;
	}

	in.s_addr = self->netp;
	strcpy(tmp1, inet_ntoa(in));
	in.s_addr = self->maskp;
	strcpy(tmp2, inet_ntoa(in));

	return Py_BuildValue("(ss)", tmp1, tmp2);
}

static PyObject *
pcap_object_findalldevs(pcap_object *self, PyObject *args)
{
	pcap_if_t * alldevs, * check;
	int i = 0;
	PyObject * list, *help;

	if (pcap_findalldevs(&alldevs, self->errbuf) == -1) {
		PyErr_SetString(PyExc_StandardError, self->errbuf);
		return NULL;
	}	

	list = PyList_New(0);

	while (1) {
		if (alldevs == NULL) break;  /* otherwise segfault when not root */
		/* for some unknown reason .next is not always correctly set to NULL */
		if (alldevs[i].name == NULL || alldevs[i].next == NULL) break;
		help = PyString_FromString(alldevs[i].name);
		PyList_Append(list, help);
		Py_DECREF(help);
		i++;
	}

	pcap_freealldevs(alldevs); /* free it up */
	return list;
}

static PyObject *
pcap_object_compile(pcap_object *self, PyObject *args)
{
	if (!PyArg_ParseTuple(args, "s", &self->filter))
		return NULL;

	if (self->descr == NULL) {
		PyErr_SetString(PyExc_StandardError, ERR_OPEN_LIVE);
		return NULL;
	}	

	if (&self->maskp == NULL) {
		if (pcap_lookupnet(self->dev, &self->netp, &self->maskp, 
			self->errbuf)==-1) {
			PyErr_SetString(PyExc_StandardError, self->errbuf);
			return NULL;
    	}
	}

	/* dont use optimize and thus set arg4 to 0 */
	if (pcap_compile(self->descr,&self->fp, self->filter, 0, self->maskp)==-1){ 
		PyErr_SetString(PyExc_StandardError, pcap_geterr(self->descr));
		return NULL;
	}
 
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
pcap_object_setfilter(pcap_object *self, PyObject *args)
{
	if (self->descr == NULL) {
		PyErr_SetString(PyExc_StandardError, ERR_OPEN_LIVE);
		return NULL;
	}

	if (pcap_setfilter(self->descr, &self->fp) == -1) {
		PyErr_SetString(PyExc_StandardError, pcap_geterr(self->descr));
		return NULL;
	}

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
pcap_object_datalink(pcap_object *self, PyObject *args)
{
	int no;
	if (self->descr == NULL) {
		PyErr_SetString(PyExc_StandardError, ERR_OPEN_LIVE);
		return NULL;
	}

	/* quick look at libpcap sources shows this call *cant* fail :-P */	
	no = pcap_datalink(self->descr);

	/* lets translate it to some nice strings */
	return PyString_FromString(DATA_LINK(no));
}

static PyObject *
pcap_object_setnonblock(pcap_object *self, PyObject *args)
{
	if (!PyArg_ParseTuple(args, "i:setnonblock", &self->nonblock))
		return NULL;

	if (self->nonblock != 0 && self->nonblock != 1) {
		PyErr_SetString(PyExc_StandardError, ERR_0_OR_1);
		return NULL;
	}

	if (self->descr == NULL) {
		PyErr_SetString(PyExc_StandardError, ERR_OPEN_LIVE);
		return NULL;
	}

	if (pcap_setnonblock(self->descr, self->nonblock, self->errbuf) == -1) {
		PyErr_SetString(PyExc_StandardError, self->errbuf);
		return NULL;
	} 

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
pcap_object_getnonblock(pcap_object *self, PyObject *args)
{
	int ret;

	if (self->descr == NULL) {
		PyErr_SetString(PyExc_StandardError, ERR_OPEN_LIVE);
		return NULL;
	}

	if ((ret = pcap_getnonblock(self->descr, self->errbuf)) == -1) {
		PyErr_SetString(PyExc_StandardError, self->errbuf);
		return NULL;
	}
	return PyInt_FromLong(ret);
}

static PyObject *
pcap_object_next(pcap_object *self, PyObject *args)
{
	PyObject *arglist;

	if (self->descr == NULL) {
		PyErr_SetString(PyExc_StandardError, ERR_OPEN_LIVE);
		return NULL;
	}

	self->pkt_data = pcap_next(self->descr, &self->hdr);

	arglist = Py_BuildValue("s#", self->pkt_data, self->hdr.len);

	if (arglist == NULL)
		return NULL;

	return arglist;
}

static PyObject *
pcap_object_snapshot(pcap_object *self, PyObject *args)
{
	if (self->descr == NULL) {
		PyErr_SetString(PyExc_StandardError, ERR_OPEN_LIVE);
		return NULL;
	}

	/* snapshot call doesn't fail :P */
	return PyInt_FromLong(pcap_snapshot(self->descr));
}

static PyObject *
pcap_object_close(pcap_object *self, PyObject *args)
{
	if (self->descr == NULL) {
		PyErr_SetString(PyExc_StandardError, ERR_OPEN_LIVE);
		return NULL;
	}

	pcap_close(self->descr);
	pcap_object_reset(self); /* clean up struct pcap_object */

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
pcap_object_stats(pcap_object *self, PyObject *args)
{
#if defined(BTK_USE_STATS)
	PyObject * stats;

	if (self->descr == NULL) {
		PyErr_SetString(PyExc_StandardError, ERR_OPEN_LIVE);	
		return NULL;
	}

	if (pcap_stats(self->descr, &self->stats) == -1) {
		PyErr_SetString(PyExc_StandardError, pcap_geterr(self->descr));
		return NULL;
	}
	
	stats = Py_BuildValue("(ii)",self->stats.ps_recv, self->stats.ps_drop);

	if (stats == NULL)
		return NULL;

	return stats;

#else
	return Py_BuildValue("(ii)", 0, 0);
#endif;
}

static PyObject *
pcap_object_open_offline(pcap_object *self, PyObject *args)
{
	if (!PyArg_ParseTuple(args, "s:open_offline", &self->file))
		return NULL;	

	if ((self->descr = pcap_open_offline(self->file, self->errbuf)) == NULL) {
		PyErr_SetString(PyExc_StandardError, self->errbuf);
		return NULL;
	}
		
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
pcap_object_dump_open(pcap_object *self, PyObject *args)
{
	if (!PyArg_ParseTuple(args, "s:dump_open", &self->file))
		return NULL;

	if (self->descr == NULL) {
		PyErr_SetString(PyExc_StandardError, ERR_OPEN_LIVE);
		return NULL;
	}

	if (self->dump != NULL) {
		PyErr_SetString(PyExc_StandardError, ERR_ALREADY_DUMP);
		return NULL;
	}

	(pcap_dumper_t *)self->dump = pcap_dump_open(self->descr, self->file);

	if (self->dump == NULL) {
		PyErr_SetString(PyExc_StandardError, pcap_geterr(self->descr));
		return NULL;
	}

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
pcap_object_dump_close(pcap_object *self, PyObject *args)
{
	if (self->dump == NULL) {
		PyErr_SetString(PyExc_StandardError, ERR_NO_DUMP);
		return NULL;
	}

	pcap_dump_close(self->dump);
	self->dump = NULL;
	
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
pcap_object_dump(pcap_object *self, PyObject *args)
{
	pcap_dump((u_char *)self->dump, &self->hdr, (u_char *)self->pkt_data);

	self->pkt_data = NULL;
	self->hdr.caplen = 0;
	self->hdr.len = 0;

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
pcap_object_is_swapped(pcap_object *self, PyObject *args)
{
	if (self->descr == NULL) {
		PyErr_SetString(PyExc_StandardError, ERR_OPEN_LIVE);
		return NULL;
	}

	return Py_BuildValue("i", pcap_is_swapped(self->descr));
}

static PyObject *
pcap_object_major_version(pcap_object *self, PyObject *args)
{
	if (self->descr == NULL) {
		PyErr_SetString(PyExc_StandardError, ERR_OPEN_LIVE);
		return NULL;
	}

	return Py_BuildValue("i", pcap_major_version(self->descr));
}

static PyObject *
pcap_object_minor_version(pcap_object *self, PyObject *args)
{
	if (self->descr == NULL) {
		PyErr_SetString(PyExc_StandardError, ERR_OPEN_LIVE);
		return NULL;
	}
	
	return Py_BuildValue("i", pcap_minor_version(self->descr));
}

static PyObject *
pcap_object_disas_packet(pcap_object *self, PyObject *args)
{
	disas_packet((u_char *)self->pkt_data);
	Py_INCREF(Py_None);
	return Py_None;
}

