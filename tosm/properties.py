
# from exceptions import AbstractClassError, NotImplementedMethodError, KeylessArgError, NotAllowedArgument


class _BaseProperty(object):
    
    _allowed_args = ["doc","validation"]

    def __init__(self, default=None, *args, **kwargs):
        
        if args:
            raise KeylessArgError()
        
        for key,value in kwargs:
            if key in _allowed_args:
                setattr(self, "_key_"+key, value)
            else:
                raise NotAllowedArgument()

        if default:
            self._set_value(default)

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
        if hasattr(self,"validation"):
            self.validation(value)

    def __get__(self, instance, cls):
        return getattr(instance, self.attr_name)

    def __set__(self, instance, value):
        for attr_name, attr_value in instance.__class__.__dict__.items():
            if attr_value == self:
                self.attr_name = '_attributename_'+attr_name
                setattr(instance, self.attr_name, value)
                break

    def _set_value(self, value):
        """
            Set the value inside the property.
            This function is internally called by the __set__ method after
            a validation.
        """
        self._implicid_validation(value)
        self._validate(value)
        setattr(self, self.attr_name, value)

class StringProperty(_BaseProperty):

    def __init__(self,**kwargs):
        pass


class IntegerProperty(_BaseProperty):

    def __init__(self,**kwargs):
        pass    


class PositiveIntegerProperty(IntegerProperty):

    def __init__(self,**kwargs):
        pass

if __name__=='__main__':
    class A(object):
        a = _BaseProperty()

    a = A()
    a.a = 10
    import pdb; pdb.set_trace()
    print a.a