
from properties import _BaseProperty, ObjectProperty


class _TobjMetaclass(type):

    def __new__(cls, name, bases, dct):

        prop = {}
        consecutive = []
        for key,value in dct.items():
            if isinstance(value, _BaseProperty):
                prop[key] = (value.__class__, value._property_index)
                consecutive.append((value._property_index,key))

        consecutive.sort(key=lambda a : a[0])
        dct.update({'_tosm_properties': prop,
                    '_consecutive_arguments': [name for i,name in consecutive],
                    })

        return super(_TobjMetaclass, cls).__new__(cls, name, bases, dct)


class Tobj(object):

    __metaclass__ = _TobjMetaclass

    def __init__(self, *args, **kwargs):
        
        self._set_consecutive_arguments(args)

        for key,value in kwargs.items():
            if key in self._tosm_properties:
                setattr(self, key, value)
            else:
                raise UnexpectedArgumentError()

    def _set_consecutive_arguments(self, args):
        
        if len(args) > len(self._consecutive_arguments):
            raise ArgumentsArithmError()

        for arg,attr in zip(args, self._consecutive_arguments):
            setattr(self, attr, arg)


    def dump(self):
        """
            Convert it from object to structure
        """

        d = {}

        for arg in self._consecutive_arguments:
            if hasattr(self, arg):
                obj = getattr(self, arg)

                if isinstance(obj, Tobj):
                    d[arg] = obj.dump()
                else:
                    d[arg] = getattr(self, arg)

        return d

    @classmethod
    def load(cls, raw):
        """ 
            Recreate a tOSM object based on a structure
        """
        
