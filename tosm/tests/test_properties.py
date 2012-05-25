
import unittest
from properties import *


class TestBaseProperty(unittest.Test):

    def test_a_base_property_basic_consistence(self):
        A = self.get_class_a()
        a = A()
        a.a = 10
        self.AssertTrue(isisntace(a.a, _BaseProperty))
    
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
