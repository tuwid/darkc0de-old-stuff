/*
    Billy the Kid (btk.h)
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

#define __DOC__      "..a python module to do all kinds of raw network shit..."
#define __NAME__     "Billy the Kid"

static btk_object * btk_obj_wrap(PyObject *, PyObject *);
static pcap_object * pcap_wrap(PyObject *, PyObject *);
static PyObject * btk_version(void);
DL_EXPORT(void) initbtk(void);

/* only defined here to make the wrapper functions work :-S */
btk_object * new_btk_object(PyObject *args);
pcap_object * new_pcap_object(PyObject *args);

/* list of functions/classes defined in this module */
static PyMethodDef btk_methods[] = {
	{"btk", (PyCFunction)btk_obj_wrap, METH_VARARGS},
	{"pcap", (PyCFunction)pcap_wrap, METH_VARARGS},
	{"version", (PyCFunction)btk_version, METH_VARARGS},
	{NULL, NULL}
};

