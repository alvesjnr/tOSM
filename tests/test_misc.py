
# tOSM - Tiny Object to Structure Modeller
# Copyright (C) 2012 - Antonio Ribeiro Alves Junior
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest
from tosm.properties import _BaseProperty
from tosm.properties import *
from tosm.objects import Tobj


class A(Tobj):
    
    this_arg = StringProperty(required=True)
    other_arg = IntegerProperty(default=100)


class Basic(unittest.TestCase):

    def test_a_default_value(self):
        a = A(this_arg='Banana')
        self.assertTrue(a.dump() == {'this_arg':'Banana', 'other_arg':100})

    def test_b_missed_value(self):
        self.assertRaises(MiscError, A)
        

if __name__=='__main__':
    unittest.main()
