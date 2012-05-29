

import types
from t_exceptions import *
from base_property import _BaseProperty
from objects import Tobj


class StringProperty(_BaseProperty):

    def _implicid_validation(self, value):

        if not isinstance(value, basestring):
            raise InvalidArgument()


class IntegerProperty(_BaseProperty):

    _allowed_args = _BaseProperty._allowed_args + ['min', 'max']

    def _implicid_validation(self, value):
        
        if not isinstance(value, types.IntType):
            raise InvalidArgument()

        if hasattr(self, '_key_max') and value > self._key_max:
            raise InvalidArgument()

        if hasattr(self, '_key_min') and value < self._key_min:
            raise InvalidArgument()

    def _key_meta_validation(self):

        if hasattr(self, '_key_max') and hasattr(self, '_key_min'):
            if self._key_max <= self._key_min:
                raise InvalidKeyValueError()


class PositiveIntegerProperty(IntegerProperty):

    def _implicid_validation(self, value):

        super(PositiveIntegerProperty,self)._implicid_validation(value)
        
        if value < 0:
            raise InvalidArgument()

    def _key_meta_validation(self):

        super(PositiveIntegerProperty, self)._key_meta_validation()

        if hasattr(self,_key_min) and self._key_min < 0:
            raise InvalidKeyValueError()
        
        if hasattr(self, _key_max) and self._key_max < 0:
            raise InvalidKeyValueError()


class ObjectProperty(_BaseProperty):

    def _implicid_validation(self, value):
        # pass
        if not isinstance(value, Tobj):
          raise InvalidArgument()
