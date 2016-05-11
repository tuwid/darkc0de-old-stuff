/*
###############################################################################
## fingerprints.py  -- see http://www.zeppoo.net                             ##
##									     ##	
## The project zeppoo is (C) 2006 : contact@zeppoo.net			     ##
## This program is free software;            				     ##
## you can redistribute it and/or modify it under the terms of the GNU       ##
## General Public License as published by the Free Software Foundation;      ##
## Version 2. This guarantees your right to use, modify, and                 ##
## redistribute this software under certain conditions.                      ##
##      								     ##
## Source is provided to this software because we believe users have a       ##
## right to know exactly what a program is going to do before they run       ##
## it.                                                                       ##
##									     ##
## This program is distributed in the hope that it will be                   ##
## useful, but WITHOUT ANY WARRANTY; without even the implied                ##
## warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR                   ##
## PURPOSE. See the GNU General Public License for more details (            ##
## http://www.gnu.org/copyleft/gpl.html ).                                   ##
##                                                                           ##
###############################################################################
*/

#include <Python.h>
struct {
	unsigned short limit;
	unsigned int base;
} __attribute__((packed)) idtr;

static PyObject * ulibzeppoo_idtr(PyObject *self){
	char base[11];
	asm("sidt %0" : "=m" (idtr));
    
	sprintf(base,"0x%x", idtr.base);
	base[sizeof(base) - 1] = '\0';
	return Py_BuildValue("s", base);
}

static PyMethodDef SpamMethods[] = {
	{"idtr",  ulibzeppoo_idtr, METH_VARARGS,"Retourne l'adresse de base de idtr"},
	{NULL, NULL, 0, NULL}        /* Sentinel */
}; 

void initulibzeppoo(void){
   (void) Py_InitModule("ulibzeppoo", SpamMethods);
}


