
import unittest
from properties import _BaseProperty


class TestBaseProperty(unittest.TestCase):

    def test_a_base_property_basic_consistence(self):
        A = self.get_class_a()
        a = A()
        a.a = 10
        self.assertTrue(isinstance(a.a, _BaseProperty))

    def test_b_default_value(self):
        B = get_class_with_default()
        b = B()
        self.assertTrue(b.b == 10)

    def test_c1_validator(self):
        pass

    def test_d_doc(self):
        D = get_class_with_doc()
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

    pass

if __name__ == '__main__':
    unittest.main()
