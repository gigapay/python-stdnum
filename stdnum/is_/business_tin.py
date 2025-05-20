# business_tin.py - functions for handling Icelandic business identity codes

"""
Business Kennitala
Module for handling Icelandic business identity codes

>>> validate('450401-3150')
'4504013150'
>>> validate('120174-3399')
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidComponent: Invalid first digit for business TIN
>>> validate('530575-0299')
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidChecksum: The number's checksum or check digit is invalid.
>>> validate('320174-3399')
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidComponent: One of the parts of the number are invalid or unknown.
>>> format('1201743399')
'120174-3399'
"""

from stdnum.exceptions import *
from stdnum.is_ import kennitala


__all__ = ['compact', 'validate', 'is_valid', 'format']


def compact(number):
    return kennitala.compact(number)

def validate(number):
    number = kennitala.validate(number)
    if int(number[0]) < 4:
        raise InvalidComponent('Invalid first digit for business TIN')
    return number

def is_valid(number):
    """Check whether the number is valid."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False

def format(number):
    return kennitala.format(number)

    