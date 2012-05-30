
import unittest
from tosm.properties import _BaseProperty
from tosm.properties import *
from tosm.objects import Tobj


class Address(Tobj):
    street = StringProperty()
    number = PositiveIntegerProperty()


class Telephone(Tobj):
    tpe = StringProperty() #TODO: implement choices
    number = PositiveIntegerProperty()


class SimplePerson(Tobj):
    name = StringProperty()
    address = ObjectProperty()
    

class Person(SimplePerson):
    tel = ListProperty()


class Contacts(Tobj):
    people = ListProperty()


class TestDumpLoad(unittest.TestCase):

    def test_a_dump_object(self):
        t = Telephone('cel', 99980)
        self.assertTrue(t.dump() == {'tpe':'cel', 'number':99980})

    def test_b_load_from_struct(self):
        t = Telephone.load({'tpe':'cel', 'number':99980})
        self.assertTrue(t.tpe == 'cel')
        self.assertTrue(t.number == 99980)


class TestRelationship(unittest.TestCase):

    def test_a_dump_simple_person(self):
        a = Address('Koningstraat', 18)
        p = SimplePerson("Donald Otello", a)
        self.assertTrue(p.dump() == {'address':{'street':'Koningstraat', 
                                                'number':18},
                                     'name':'Donald Otello'})

    def test_b_dump_person(self):
        a = Address('Koningstraat', 18)
        t1 = Telephone('cel', 123)
        t2 = Telephone('house', 777)
        p = Person(name="Donald Otello", tel=[t1, t2], address=a)

        expected_struct = {'name':'Donald Otello',
                           'address':{'street':'Koningstraat',
                                      'number':18},
                           'tel':[{'tpe':'cel', 'number':123},
                                  {'tpe':'house', 'number':777}],
                           }
        self.assertTrue(p.dump() == expected_struct)
        
if __name__=='__main__':
    unittest.main()
