
import types

from t_exceptions import KeylessArgError, NotAllowedArgument, InvalidKeyValueError, InvalidArgument


class _OrderedProperty(object):
    
    counter = 0

    @classmethod
    def get_counter_and_increment(cls):
        cls.counter += 1
        return cls.counter


class _BaseProperty(object):
    
    _allowed_args = ['doc','validator']

    def __init__(self, default=None, *args, **kwargs):

        self._property_index = _OrderedProperty.get_counter_and_increment()
        
        if args:
            raise KeylessArgError()

        for key,value in kwargs.items():
            if key in self._allowed_args:
                setattr(self, "_key_"+key, value)
            else:
                raise NotAllowedArgument()
        
        self._key_meta_validation()

        if default:
            self._validate(default)
            self._implicid_validation(default)
            self._default_value = default

    def _implicid_validation(self, value):
        """
            The implicid validation uses general keys to valid the property
            Examples of keys are: max, min, validation_function, etc.
            Available keys may change from one property to another, check the 
            API reference for valid keys for each property
        """

    def _validate(self, value):
        """
            The validate function is a wrapper to the externally provided
            validation function
        """
        if hasattr(self,"_key_validator"):
            self._key_validator(value)

    def __get__(self, instance, cls):
        
        if hasattr(instance, self.attr_name):
            return getattr(instance, self.attr_name)
        elif hasattr(instance, '_default_value'):
            return instance._default_value


    def __set__(self, instance, value):
        self._implicid_validation(value)
        self._validate(value)
        for attr_name, attr_value in instance.__class__.__dict__.items():
            if attr_value == self:
                self.attr_name = '_attributename_'+attr_name
                setattr(instance, self.attr_name, value)
                break
    
    def _key_meta_validation(self):
        """
            This method valid if the key arguments are valid as keys
            For instance, if checks if key max isn't less or equal than key min
        """

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

        if hasattr(self,'_key_min') and self._key_min < 0:
            raise InvalidKeyValueError()
        
        if hasattr(self, '_key_max') and self._key_max < 0:
            raise InvalidKeyValueError()


class ObjectProperty(_BaseProperty):

    def __set__(self, instance, value):
        
        super(ObjectProperty, self).__set__(instance, value)

        self._object_definition = type(value)

    def _implicid_validation(self, value):
        
        from objects import Tobj    #FIXME: inside-objects imports are not a good idea!
        
        if not isinstance(value, Tobj):
            raise InvalidArgument()


class ObjectListProperty(_BaseProperty):
    pass
