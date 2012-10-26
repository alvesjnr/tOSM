
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
    tel = ListProperty(content_type=Telephone)


class Contacts(Tobj):
    people = ListProperty(content_type=Person)


class TestDumpLoad(unittest.TestCase):

    def test_a_dump_object(self):
        t = Telephone('cel', 99980)
        self.assertTrue(t.dump() == {'tpe':'cel', 'number':99980})

    def test_b_load_from_struct(self):
        t = Telephone.load({'tpe':'cel', 'number':99980})
        self.assertTrue(t.tpe == 'cel')
        self.assertTrue(t.number == 99980)

    def test_c_load_list(self):
        class A(Tobj):
            s = ListProperty(content_type=str)

        struct = {'s':['1','a','9.9']}
        a = A.load(struct)
        self.assertTrue(a.dump() == {'s':['1','a','9.9']})

    def test_d_load_list_of_objects(self):
        class B(Tobj):
            p = IntegerProperty()
        class A(Tobj):
            l = ListProperty(content_type=B)

        struct = {'l':[{'p':9},{'p':-8},{'p':0}]}
        a = A.load(struct)
        self.assertTrue(a.dump() == struct)


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

    def test_c_inheritance_with_ordered_args(self):
        a = Address('Koningstraat', 18)
        t1 = Telephone('cel', 123)
        t2 = Telephone('house', 777)
        p = Person("Donald Otello", a, [t1, t2])

        expected_struct = {'name':'Donald Otello',
                           'address':{'street':'Koningstraat',
                                      'number':18},
                           'tel':[{'tpe':'cel', 'number':123},
                                  {'tpe':'house', 'number':777}],
                           }

        self.assertTrue(p.dump() == expected_struct)

    def test_d1_load(self):
        struct = {'name':'Donald Otello',
                  'address':{'street':'Koningstraat',
                             'number':18},
                  'tel':[{'tpe':'cel', 'number':123},
                         {'tpe':'house', 'number':777}],
                  }
        p = Person.load(struct)
        self.assertTrue(p.dump() == struct)

    def testd_d2_load(self):
        struct = {'people':[{'name':'Donald Otello',
                               'address':{'street':'Koningstraat',
                                          'number':18},
                               'tel':[{'tpe':'cel', 'number':12},
                                      {'tpe':'house', 'number':777}],
                               },
                               {'name':'Michel Angelo',
                               'address':{'street':'Danport',
                                          'number':1998},
                               'tel':[{'tpe':'cel', 'number':222},
                                      {'tpe':'house', 'number':978}],
                               },
                               {'name':'Poc a Hontas',
                               'address':{'street':'Sint Pieters',
                                          'number':33},
                               'tel':[{'tpe':'cel', 'number':654},
                                      {'tpe':'house', 'number':123}],
                               },
                               ]
                    }
        p = Contacts.load(struct)
        self.assertTrue(p.dump() == struct)


class OtherPerson(Tobj):
    name = StringProperty()
    age = PositiveIntegerProperty()


class Student(OtherPerson):
    course = StringProperty()


class Professor(OtherPerson):
    salary = PositiveNumberProperty()


class Director(Professor):
    institute = StringProperty()


class TestMultipleInheritance(unittest.TestCase):

    def test_a_people(self):
        p = OtherPerson(name="Carlos", age=22)
        self.assertTrue(p.dump() == {'name':'Carlos', 'age':22})

    def test_b_student(self):
        s = Student(name="Carlos", age=22, course="fotonica")
        self.assertTrue(s.dump() == {'name':'Carlos', 'age':22, 'course':'fotonica'})

    def test_c_professor(self):
        p = Professor(name="Fernando", age=77, salary=1000)
        self.assertTrue(p.dump() == {'name':'Fernando', 'age':77, 'salary':1000})

    def test_d_director(self):
        p = Director(name="Fernando", age=77, salary=1000, institute="Math")
        self.assertTrue(p.dump() == {'name':'Fernando', 'age':77, 'salary':1000, 'institute':'Math'})

        
if __name__=='__main__':
    unittest.main()

