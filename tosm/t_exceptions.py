
class _BaseTosmException(BaseException):
    """
        Just a plcaeholder
    """

class KeylessArgError(_BaseTosmException):
    """ Property accepts only key arguments """


class NotAllowedArgument(_BaseTosmException): 
    """ This value is not allowed to this property """

class InvalidKeyValueError(_BaseTosmException):
    """ The key is not valid """

class UnexpectedArgumentError(_BaseTosmException):
    """ Unexpected argument """

class ArgumentsArithmError(_BaseTosmException):
    """ Tobj got more arguments than expected """

class InvalidArgument(_BaseTosmException):
    """ Your argument is invalid """
