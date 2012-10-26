
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


class TestBaseProperty(unittest.TestCase):

    def test_a_base_property_basic_consistence(self):
        A = self.get_class_a()
        a = A()
        a.a = 10
        self.assertTrue(isinstance(a.__class__.__dict__['a'], _BaseProperty))

    def test_b_default_value(self):
        B = self.get_class_with_default()
        b = B()
        self.assertTrue(b.b == 10)

    def test_c1_validator(self):
        pass

    def test_d_doc(self):
        D = self.get_class_with_doc()
        d = D()
        self.assertTrue(d.d.doc == "Yes, this is doc!") #FIXME!!!
    
    @staticmethod
    def get_class_a():
        class A(object):
            a = _BaseProperty()

        return A

    @staticmethod
    def get_class_with_default():
        class B(object):
            b = _BaseProperty(default=10)

        return B

    @staticmethod
    def get_class_with_validator(validator):
            class C(object):
                c = _BaseProperty(validator=validator)

            return C

    @staticmethod
    def get_class_with_doc():
        class D(object):
            d = _BaseProperty(doc="Yes, this is doc!")

        return D


class TestIntegerProperty(unittest.TestCase):

    @staticmethod
    def get_class():
        class A(Tobj):
            value = IntegerProperty()

        return A

    def test_a_integer_property(self):
        a = self.get_class()(10)
        self.assertTrue(a.value == 10)

    def test_b_dump(self):
        a = self.get_class()(10)
        self.assertTrue(a.dump() == {'value': 10})

    def test_b_load(self):
        A = self.get_class()
        a = A.load({'value':88})
        self.assertTrue(a.value == 88)



class TestListProperty(unittest.TestCase):

    @staticmethod
    def get_class_a():
        class A(Tobj):
            values = ListProperty()

        return A()

    @staticmethod
    def get_class_b():
        class B(Tobj):
            values = ListProperty(content_type=str)

        return B()

    def test_a_default_value(self):
        a = self.get_class_a()
        self.assertTrue(a.values == [])

    def test_b_add_things_to_list(self):
        a = self.get_class_a()
        for i in range(10):
            a.values.append(i)
        self.assertTrue(a.values == range(10))

    def test_c_add_correct_type_value(self):
        b = self.get_class_b()
        for i in range(10):
            b.values.append(str(i))
        self.assertTrue(b.values == [str(i) for i in range(10)])

    def test_d_add_incorrect_type_value(self):
        b = self.get_class_b()
        self.assertRaises(InvalidArgument,b.values.append,10)

    def test_e_check_content_type(self):
        class E(Tobj):
            l = ListProperty(content_type=str)

        self.assertTrue(E(l=['1']).dump() == {'l':['1']})
        self.assertRaises(InvalidArgument,E,['1',2])
        self.assertRaises(InvalidArgument, E, 12)
        self.assertRaises(InvalidArgument, E, [12])


if __name__ == '__main__':
    unittest.main()
