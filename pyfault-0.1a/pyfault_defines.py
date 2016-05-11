#
# PyFault
# Copyright (C) 2007 Justin Seitz <jms@bughunter.ca>
#
#
# This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program; if not, write to the Free
# Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#


'''
This provides the constants the main pyfault class uses for process access, memory writes, etc.
Some of these were gleaned from MSDN (http://msdn.microsoft.com) and the module structure is 
referring to a code snippet in the PaiMei framework (http://paimei.openrce.org) by Pedram Amini, although I 
changed the ctypes type of hModule to be slightly different.
'''

import ctypes

INFINITE               =     0xFFFFFFFF
INVALID_HANDLE_VALUE   =     0xFFFFFFFF
PAGE_READWRITE         =     0x04
PROCESS_ALL_ACCESS     =     ( 0x000F0000 | 0x00100000 | 0xFFF )
TH32CS_SNAPMODULE      =     0x00000008
VIRTUAL_MEM            =     ( 0x1000 | 0x2000 )



class MODULEENTRY32(ctypes.Structure):
    _fields_ = [
        ("dwSize",        ctypes.c_ulong),
        ("th32ModuleID",  ctypes.c_ulong),
        ("th32ProcessID", ctypes.c_ulong),
        ("GlblcntUsage",  ctypes.c_ulong),
        ("ProccntUsage",  ctypes.c_ulong),
        ("modBaseAddr",   ctypes.c_ulong),
        ("modBaseSize",   ctypes.c_ulong),
        ("hModule",       ctypes.c_void_p),
        ("szModule",      ctypes.c_char * 256),
        ("szExePath",     ctypes.c_char * 260),
	]