
from properties import _BaseProperty
from t_exceptions import *


class TobjMetaclass(type):

    def __new__(cls, name, bases, dct):

        prop = {}
        consecutive = []
        for key,value in dct.items():
            if isinstance(value, _BaseProperty):
                prop[key] = (value.__class__, value._property_index)
                consecutive.append((value._property_index,key))
        # blah = dct.items()[0][1]
        # import pdb; pdb.set_trace()
        # isinstance(blah,_BaseProperty)
        consecutive.sort(key=lambda a : a[0])
        dct.update({'_tosm_properties': prop,
                    '_consecutive_arguments': [name for i,name in consecutive],
                    })

        return super(TobjMetaclass, cls).__new__(cls, name, bases, dct)
