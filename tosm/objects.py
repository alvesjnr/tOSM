
class TosmError(BaseException):
    pass

class NotImplementedMethodError(TosmError):
    pass


class Obj(object):

    def __new__(cls,*args,**kwargs):
        o = super(Obj, cls).__new__(cls,args,*kwargs)
        return o

    def __init__(self,*args,**kwargs):
        # blah
        try:
            self._validate()
        except NotImplementedMethodError:
            pass

    def _validate(self):
        """
            The validation function must be implemented by the API user
        """
        raise NotImplementedMethodError()

    def dump(self):
        return {}

    @classmethod
    def load(cls, dct):
        o = cls()
        return o

    @staticmethod
    def load2(dct):
        o = Obj()
        return o

if __name__ == '__main__':
    Obj()
