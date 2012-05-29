
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


if __name__ == '__main__':
    unittest.main()
