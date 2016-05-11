/*
    Billy the Kid (btk_obj.c)
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
#include "btk_obj.h"

btk_object *
new_btk_object(PyObject *args)
{
        btk_object *self;
        self = PyObject_New(btk_object, &btk_object_type);
        if (self == NULL)
                return NULL;
        self->btk_obj_attr = NULL;
        return self;
}

static void
btk_object_dealloc(btk_object *self)
{
        Py_XDECREF(self->btk_obj_attr);
        PyObject_Del(self);
}

static PyObject *
btk_object_getattr(btk_object *self, char *name)
{
        if (self->btk_obj_attr != NULL) {
                PyObject *v = PyDict_GetItemString(self->btk_obj_attr, name);
                if (v != NULL) {
                        Py_INCREF(v);
                        return v;
                }
        }
        return Py_FindMethod(btk_obj_methods, (PyObject *)self, name);
}

static int
btk_object_setattr(btk_object *self, char *name, PyObject *v)
{
        if (self->btk_obj_attr == NULL) {
                self->btk_obj_attr = PyDict_New();
                if (self->btk_obj_attr == NULL)
                        return -1;
        }
        if (v == NULL) {
                int rv = PyDict_DelItemString(self->btk_obj_attr, name);
                if (rv < 0)
                        PyErr_SetString(PyExc_AttributeError,
                                "delete non-existing btk_obj attribute");
                return rv;
        }
        else
                return PyDict_SetItemString(self->btk_obj_attr, name, v);
}

/* setting references to automatic methods */
statichere PyTypeObject btk_object_type = {
        PyObject_HEAD_INIT(NULL)
        0,                      /*ob_size*/
        "btk_object",
        sizeof(btk_object),
        0,                      /*tp_itemsize*/
        (destructor)btk_object_dealloc,
        0,                      /*tp_print*/
        (getattrfunc)btk_object_getattr,
        (setattrfunc)btk_object_setattr,
        0,                      /*tp_compare*/
        0,                      /*tp_repr*/
        0,                      /*tp_as_number*/
        0,                      /*tp_as_sequence*/
        0,                      /*tp_as_mapping*/
        0,                      /*tp_hash*/
};

/*  
*  from here all btk_object methods are defined
*/

static PyObject * 
btk_object_protocol(btk_object *self, PyObject *args)
{
        int protocol;
        if (!PyArg_ParseTuple(args, "i:protocol", &protocol))
                return NULL;
printf("%i\n", sizeof(struct icmphdr));	
	if (protocol == TCP) {
		self->protocol = TCP;
	        self->iph=(struct ip *) self->packet;
       	 	self->pseudo=(struct pseudo *)(self->packet + 
			   	sizeof(struct ip));
        	self->tcph=(struct tcphdr *) (self->packet + sizeof(struct ip)
                                + sizeof(struct pseudo));
        	self->data=(char *) (self->packet + sizeof(struct ip) +
                     		sizeof(struct pseudo) + sizeof(struct tcphdr));
	}
	else if (protocol == UDP) {
		self->protocol = UDP;
		self->iph=(struct ip *) self->packet;
		self->pseudo=(struct pseudo *)(self->packet +
				sizeof(struct ip));
		self->udph=(struct udphdr *) (self->packet + sizeof(struct ip)
				+ sizeof(struct pseudo));
		self->data=(char *) (self->packet + sizeof(struct ip) +
				sizeof(struct pseudo) + sizeof(struct udphdr)); 
	}
	else if (protocol == ICMP) {
		self->protocol = ICMP;
		self->iph=(struct ip *) self->packet;
		self->icmph=(struct icmphdr *) (self->packet + sizeof(struct ip));
		self->data=(char *) (self->packet + sizeof(struct ip) +\
				sizeof(struct icmphdr));
	}
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
btk_object_data(btk_object *self, PyObject *args)
{
	char * data;
	int i;
	self->data_length = 0;
	if (!PyArg_ParseTuple(args, "s#:data", &data,
			&self->data_length))
		return NULL;
	
/* seems to do the trick, altough it fucks up the
   unicode based encodings !! */
	for (i=0;i<self->data_length;i++) {
		memcpy(*(&self->tmpdata)+i, *(&data)+i, 1);
	}

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
btk_object_flags(btk_object *self, PyObject *args)
{
	int flags;
	if (!PyArg_ParseTuple(args, "i:flags", &flags))
		return NULL;
	self->flags = flags;
	if (self->flags != flags || self->flags < 0)
		return PyInt_FromLong(-1);
	Py_INCREF(Py_None);
	return Py_None;	
}

static PyObject *
btk_object_send(btk_object *self, PyObject *args)
{
	struct sockaddr_in foo;
        int rawfd, one;

        if (!PyArg_ParseTuple(args, "sisi:send", &self->dstip, &self->dstport,
					&self->srcip, &self->srcport))
                return NULL;

	switch(self->protocol) {
	case TCP:
		fill_tcp_headers(self);
		break;
	case UDP:
		fill_udp_headers(self);
		break;
	case ICMP:
		fill_icmp_headers(self);
		break;
	};

	memset(&foo,'\0',sizeof(foo));
	foo.sin_family=AF_INET;
        foo.sin_addr.s_addr=inet_addr(self->dstip);
        one = 1;

        if ((rawfd=socket(PF_INET,SOCK_RAW,IPPROTO_ICMP))<0) {
                perror("RawSocket");
        }
        if (setsockopt(rawfd,IPPROTO_IP,IP_HDRINCL,&one,sizeof(one))<0) {
                perror("SetSockOpt");
        }

        if (sendto(rawfd,self->packet,self->packet_length, 0,
                        (struct sockaddr *) &foo,sizeof(foo))<0)
		perror("SendingSock");
		
	memset(self->packet, '\0', MAX_PACKET_LEN);

        Py_INCREF(Py_None);
        return Py_None;
}

static PyObject *
btk_object_options(btk_object *self, PyObject *args, PyObject *keywords)
{
/* making options not directly go to self->x 'cause of some problems
* which can arise if btk_object_protocol() hasn't been run yet. */

	static char *kwlist[] = {"seq", "ack", "urp", "win", "off", "tos",
				 "ttl", "id", "type", "code", "gateway", "address_mask",
				 "time_orig", "time_recv", "time_tsmt", "pointer",
				 "no_addr", "entry_size", "lifetime", "icmp_id",
				 "icmp_seq" , NULL};

	if (!PyArg_ParseTupleAndKeywords(args, keywords, "|iiiiiiiiiissiiiiiiiii",
		kwlist,
			&self->seq, &self->ack, &self->urp, &self->win,
			&self->off, &self->tos, &self->ttl, &self->id,
			&self->type, &self->code, &self->gateway, &self->address_mask,
			&self->time_originate, &self->time_receive,
			&self->time_transmit, &self->pointer, &self->no_addresses,
			&self->entry_size, &self->lifetime, &self->icmpid,
			&self->icmpseq))
        	return NULL;
	
	Py_INCREF(Py_None);
	return Py_None;
}
