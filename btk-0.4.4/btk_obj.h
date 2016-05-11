/*
    Billy the Kid (btk_obj.h)
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

staticforward PyTypeObject btk_object_type;

/* defining automatic Python methods for btk_object */
btk_object * new_btk_object(PyObject *args);
static void btk_object_dealloc(btk_object *);
static PyObject * btk_object_getattr(btk_object *self, char *name);
static int btk_object_setattr(btk_object *self, char *name, PyObject *v);

/* defining 'normal', user-callable methods for btk_object */
static PyObject * btk_object_data(btk_object *, PyObject *);
static PyObject * btk_object_flags(btk_object *, PyObject *);
static PyObject * btk_object_options(btk_object *, PyObject *, PyObject *);
static PyObject * btk_object_protocol(btk_object *, PyObject *);
static PyObject * btk_object_send(btk_object *, PyObject *);

/* all methods of btk_object must also be declared here */
static PyMethodDef btk_obj_methods[] = {
	{"data", (PyCFunction)btk_object_data, METH_VARARGS},
	{"flags", (PyCFunction)btk_object_flags, METH_VARARGS},
{"options", (PyCFunction)btk_object_options, METH_VARARGS|METH_KEYWORDS},
	{"protocol", (PyCFunction)btk_object_protocol, METH_VARARGS},
	{"send", (PyCFunction)btk_object_send, METH_VARARGS},
        {NULL,          NULL}
};

