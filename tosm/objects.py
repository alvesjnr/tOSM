
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

from properties import _BaseProperty, ObjectProperty, ListProperty
from t_exceptions import UnexpectedArgumentError, MiscError


class _TobjMetaclass(type):

    def __new__(cls, name, bases, dct):

        for base in bases:
            for key, value in base.__dict__.items():
                if isinstance(value,_BaseProperty):
                    dct[key] = base.__dict__[key]
                    delattr(base, key)

        prop = {}
        for key,value in dct.items():
            if isinstance(value, _BaseProperty):
                prop[key] = (value.__class__, value._property_index)

        consecutive_arguments = [(key,value[1]) for key,value in prop.items()]
        consecutive_arguments.sort(key=lambda a : a[1])
        consecutive_arguments = [arg for arg,i in consecutive_arguments]

        dct.update({'_tosm_properties': prop,
                    '_consecutive_arguments': consecutive_arguments,
                    })
        
        return super(_TobjMetaclass, cls).__new__(cls, name, bases, dct)
    

class Tobj(object):

    __metaclass__ = _TobjMetaclass

    def __init__(self, *args, **kwargs):
        
        self._set_consecutive_arguments(args)

        for prop_name in self._consecutive_arguments[len(args):]:
            prop = self.__class__.__getattribute__(self.__class__,prop_name)
            if prop.required_property:
                if not prop_name in kwargs.keys():
                    raise MiscError("Missing required value: '%s'" % prop_name)

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
                    if issubclass(obj_class, Tobj):
                        obj = [obj_class.load(v) for v in value]
                    else:
                        obj = [obj_class(v) for v in value]
                    setattr(tobj, key, obj)

                else:
                    setattr(tobj, key, value)
            
            else:
                raise UnexpectedArgumentError()

        return tobj
