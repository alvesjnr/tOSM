
from t_exceptions import *


class NumberedProperty(object):
    
    counter = 0

    @classmethod
    def get_counter_and_increment(cls):
        cls.counter += 1
        return cls.counter


class _BaseProperty(object):
    
    _allowed_args = ['doc','validator']

    def __init__(self, default=None, *args, **kwargs):

        self._property_index = NumberedProperty.get_counter_and_increment()
        
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
        elif hasattr(instance, _default_value):
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
