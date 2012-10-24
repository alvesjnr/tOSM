
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


class _BaseTosmException(BaseException):
    """
        Just a plcaeholder
    """

class MiscError(_BaseTosmException):
    """An error hapened!"""

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

class UnexpectedArgumentError(_BaseTosmException):
	""" Some argument was not expected """