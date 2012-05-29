
from properties import _BaseProperty, ObjectProperty, ListProperty
from t_exceptions import UnexpectedArgumentError


class _TobjMetaclass(type):

    def __new__(cls, name, bases, dct):

        prop = {}
        consecutive = []
        for key,value in dct.items():
            if isinstance(value, _BaseProperty):
                prop[key] = (value.__class__, value._property_index)
                consecutive.append((value._property_index,key))

        consecutive.sort(key=lambda a : a[0])

        #FIXME: The idea works, but PLEASE: refactory it!
        parent_classes_properties = {}
        parent_classes_arguments = []
        for base in bases:
            if hasattr(base, '_consecutive_arguments'):
                parent_classes_arguments += base._consecutive_arguments
            if hasattr(base, '_tosm_properties'):
                parent_classes_properties.update(base._tosm_properties)

        prop.update(parent_classes_properties)
        dct.update({'_tosm_properties': prop,
                    '_consecutive_arguments': parent_classes_arguments + [name for i,name in consecutive],
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
                raise UnexpectedArgumentError(key)

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
                elif isinstance(obj,list):
                    if obj:
                        if isinstance(obj[0], Tobj):
                            d[arg] = [v.dump() for v in obj]
                        else:
                            d[arg] = [v for v in obj]
                    else:
                        d[arg] = []
                else:
                    d[arg] = getattr(self, arg)

        return d

    @classmethod
    def load(cls, raw):
        """ 
            Recreate a tOSM object based on a structure
        """
        tobj = cls()

        for key,value in raw.items():
            if key in tobj._tosm_properties:

                meta_obj = cls.__getattribute__(cls,key)
                
                if isinstance(meta_obj, ObjectProperty):
                    obj_class = meta_obj._object_definition
                    obj = obj_class.load(value)
                    setattr(tobj, key, obj)

                elif isinstance(meta_obj, ListProperty):
                    obj_class = meta_obj._key_content_type
                    if isinstance(obj_class, _BaseProperty):
                        obj = [obj_class.load(v) for v in value]
                    else:
                        obj = [obj_class(v) for v in value]
                    setattr(tobj, key, obj)

                else:
                    setattr(tobj, key, value)
            
            else:
                raise UnexpectedArgumentError()

        return tobj
