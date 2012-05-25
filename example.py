"""
    tOSM - tinny object to structure modeller 
    generic example of use
"""

from tosm.objects import Tobj
from tosm.properties import IntegerProperty, StringProperty

class A(Tobj):

    this_arg = StringProperty()
    other_arg = IntegerProperty()

a = A(this_arg="12", other_arg=99)

b = A("Cavaco", 1999)

try:
    A(99,99)
except:
    print "You got an exception here!"

