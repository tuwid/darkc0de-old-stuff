'''
The contents of this file are subject to the Mozilla Public License
Version 1.1 (the "License"); you may not use this file except in
compliance with the License. You may obtain a copy of the License at
http://www.mozilla.org/MPL/

Software distributed under the License is distributed on an "AS IS"
basis, WITHOUT WARRANTY OF ANY KIND, either express or implied. See the
License for the specific language governing rights and limitations
under the License.

The Original Code is iaxscan, v0.02, 9th October 2008.

The Initial Developer of the Original Code is nnp, http://www.unprotectedhex.com
'''

import sys

class Logger:
    
    def __init__(self, level=5):
        '''
        The higher the level the more debug info that will be printed
        '''
        self.level = level
        
    def log(self, msg, level=5):
        if level <= self.level:
            if level > 5:
                caller = sys._getframe(1)
                fileName = caller.f_code.co_filename.split('/')[-1]
                print '[%s/%s] %s' % (fileName, caller.f_code.co_name, msg)
            else:
                print msg
