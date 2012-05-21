
class _BaseProperty:

    def __init__(self):
        pass

    def _implicid_validation(self):
        """
            The implicid validation uses general keys to valid the property
            Examples of keys are: max, min, validation_function, etc.
            Available keys may change from one property to another, check the 
            API reference for valid keys for each property
        """

    def _validate(self):
        raise NotImplementedMethodError()


class StringProperty(_BaseProperty):

    def __init__(self,**kwargs):
        pass


class IntegerProperty(_BaseProperty):

    def __init__(self,**kwargs):
        pass


class PositiveIntegerProperty(IntegerProperty):

    def __init__(self,**kwargs):
        pass
