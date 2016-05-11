/*
    Billy the Kid (btk.c)
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
#include "btk.h"
#include "packet.h"

/* those wrapper functions make it easier to call 
   functions or classes in btk_obj.c and pcap.c */
 
static btk_object *
btk_obj_wrap(PyObject *self, PyObject *args)
{
	btk_object * return_object;
	return_object = new_btk_object(args);
	return return_object;
}

static pcap_object *
pcap_wrap(PyObject *self, PyObject *args)
{
	pcap_object * return_object;
	return_object = new_pcap_object(args);
	return return_object;
}

static PyObject *
btk_version(void)
{
	return PyString_FromString(__NAME__" "VERSION);
}

DL_EXPORT(void)
initbtk(void)
{
	PyObject *module, *dict;

	module = Py_InitModule("btk", btk_methods);
	dict = PyModule_GetDict(module);

	/* setting environment vars */
	PyDict_SetItemString(dict, "__name__", PyString_FromString(__NAME__));
	PyDict_SetItemString(dict, "__doc__", PyString_FromString(__DOC__));
	PyDict_SetItemString(dict, "SYN", PyInt_FromLong(SYN));
	PyDict_SetItemString(dict, "RST", PyInt_FromLong(RST));
	PyDict_SetItemString(dict, "ACK", PyInt_FromLong(ACK));
	PyDict_SetItemString(dict, "FIN", PyInt_FromLong(FIN));
	PyDict_SetItemString(dict, "PUSH", PyInt_FromLong(PUSH));
	PyDict_SetItemString(dict, "URG", PyInt_FromLong(URG));
	PyDict_SetItemString(dict, "CWR", PyInt_FromLong(CWR));
	PyDict_SetItemString(dict, "ECN", PyInt_FromLong(ECN));
	PyDict_SetItemString(dict, "TCP", PyInt_FromLong(TCP));
	PyDict_SetItemString(dict, "ICMP", PyInt_FromLong(ICMP));
	PyDict_SetItemString(dict, "UDP", PyInt_FromLong(UDP));
}
