"""
    tOSM - tinny object to structure modeller 
    generic example of use
"""

from tosm.objects import Tobj
from tosm.properties import IntegerProperty, StringProperty, PositiveIntegerProperty, ObjectProperty

class A(Tobj):

    this_arg = StringProperty()
    other_arg = IntegerProperty()

a = A(this_arg="12", other_arg=99)

print a.this_arg, a.other_arg

b = A("Cavaco", 1999)

print b.this_arg, b.other_arg

try:
    A(99,99)
except:
    print "You got an exception here because 99 is not string!"

try:
    A(12,"34") #similar to 'b = A("Cavaco", 1999)' above, but in a wrong order
except:
    print "Order matters!"


"""
    A more complex example
"""

class Person(Tobj):
    name = StringProperty()
    tel = PositiveIntegerProperty()
    address = ObjectProperty()


class Address(Tobj):
    street = StringProperty()
    number = PositiveIntegerProperty()

carlos = Person("Carlos", 99887766, Address(number=99, street="Koningstraat"))

dumped = carlos.dump()
print dumped

recreated_carlos = Person.load(dumped)

print recreated_carlos.dump()

