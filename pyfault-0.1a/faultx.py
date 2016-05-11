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

import pyfault_defines
import ctypes

'''
A very simple exception class for pyfault. If you really want to have the WIN32API errors here
then let me know and I will add them.

Raise an exception like this: raise faultx("Holy poop batman, I think the batcar just broke down.")
'''

class faultx(Exception):
    
    def __init__(self,error_message):
        
        self.error_message = error_message
        
    
    def __str__(self):
        
        return self.error_message
        