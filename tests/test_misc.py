
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


class B(Tobj):
    """Here the property with default value comes firts"""
    other_arg = IntegerProperty(default=100)
    this_arg = StringProperty(required=True)


class Basic(unittest.TestCase):

    def test_a_default_value(self):
        a = A(this_arg='Banana')
        self.assertTrue(a.dump() == {'this_arg':'Banana', 'other_arg':100})

    def test_b_missed_value(self):
        self.assertRaises(MiscError, A)

    def test_c_rewrinting_default(self):
        a = A(this_arg="Banana", other_arg=99)    
        self.assertTrue(a.dump() == {'this_arg':'Banana', 'other_arg':99})

    def test_d_sequential(self):
        a = A("sapato", 51)
        self.assertTrue(a.dump() == {'this_arg':'sapato', 'other_arg':51})

    def test_e_partial_qequentil(self):
        a = A("sapato")
        self.assertTrue(a.dump() == {'this_arg':'sapato', 'other_arg':100})

    def test_f_default_value(self):
        b = B(this_arg="Pedra")
        self.assertTrue(b.dump() == {'this_arg':'Pedra', 'other_arg':100})

    def test_g_missed_value(self):
        self.assertRaises(MiscError,B)

    def test_h_rewriting_default(self):
        b = B(this_arg="Pedra", other_arg=99)    
        self.assertTrue(b.dump() == {'this_arg':'Pedra', 'other_arg':99})

    def test_i_positional_plus_named(self):
        b = B(33,this_arg="Trinta e tres")
        self.assertTrue(b.dump() == {'this_arg':'Trinta e tres', 'other_arg':33})
        a = A("Trinta e tres", other_arg=33)
        self.assertTrue(a.dump() == {'this_arg':'Trinta e tres', 'other_arg':33})



if __name__=='__main__':
    unittest.main()
