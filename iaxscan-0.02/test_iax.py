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

import unittest
from iax import IAXProto

class TestIAXProto(unittest.TestCase):
    
    def setUp(self):
        self.iaxProto = IAXProto()
        
    def testExtractAuthUser(self):
        f = open('regauth_data', 'r')
        data = f.read()
        f.close()
        res = self.iaxProto.extractAuthUser(data)
        self.assertEqual(res, '999')
        
    def testExtractAuthUserNoUser(self):
        f = open('regrej_data', 'r')
        data = f.read()
        f.close()
        res = self.iaxProto.extractAuthUser(data)
        self.assertEqual(res, None)