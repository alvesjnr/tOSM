"""
    tOSM - tinny object to structure modeller 
    generic example of use
"""

import tosm as t


class Contacts(t.Obj):
    persons = t.ObjListProperty(obj=Person)

    def insert_new_contac(self, contact):
        self.persons.append(contact)


class Person(t.Obj):
    name = t.StringProperty()
    phonenumber = t.IntegerProperty()
    birthdate = t.ObjProperty(obj=BirthDate)


class Birthdate(t.Obj):
    day = t.PositiveIntegerProperty(max=31)
    month = t.PositiveIntegerProperty(max=12)
    year = t.PositiveIntegerProperty(min=1850, max=2020)

    def _validate(self):
        
        if self.month in [4,6,9,11] and self.day == 31:
            raise t.BaseError("The month %s hasn't 31 days!" % self.month)

        if is_bissext(self.year):
            if self.day >= 29:
                raise t.BaseError("The month %s hasn't %s days" % (self.month, self.day))
        else:
            if self.day >= 28:
                raise t.BaseError("The month %s hasn't %s days" % (self.month, self.day))


if __name__ == '__main__':

    contacts = Contacts()

    p1 = Person(name="Miguel Angelo", phonenumber=21238, birthdate=Birthdate(19,8,1977))
    p2 = Person(name="Donald Otello", phonenumber=999887766, birthdate=Birthdate(10,11,1955))

    contacts.insert_new_contac(p1)
    contacts.insert_new_contac(p2)

    dictionary = contacts.dump()
    """
        should return something like:
        
        {"persons":[{"name":"Miguel Angelo", 
                     "phonenumber":21238, 
                     "birthdate":{"day":19, 
                                  "year":1977, 
                                  "month":8}},
                    {"name":"Donald Otello", 
                     "phonenumber":999887766, 
                     "birthdate":{"day":10, 
                                  "year":1955, 
                                  "month":11}}
                    ]
        }

    """

    recreated_contacts = Contacts.load(dictionary)
