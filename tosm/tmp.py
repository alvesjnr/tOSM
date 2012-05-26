
from objects import Tobj
from properties import ObjectProperty, IntegerProperty


class A(Tobj):
	a = ObjectProperty()


class B(Tobj):
	b = IntegerProperty()

b = B()
a = A(b)
