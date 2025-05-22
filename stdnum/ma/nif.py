# nif.py - functions for handling Morocco personal TIN (Numéro d'Identification Fiscale, NIF)
# coding: utf-8

"""NIF (Numéro d'Identification Fiscale, Morocco personal tax identification number).

The Numéro d'Identification Fiscale (NIF) is the Moroccan taxpayer identification 
number used for personal tax purposes.

The NIF consists of 8 digits without any check digits or internal structure.

More information:
* https://www.fonoa.com/resources/blog/tax-number-formats-around-the-world#morocco

>>> validate('12345678')
'12345678'
>>> validate('1234567')
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidLength: NIF must be 8 digits long
>>> validate('1234567a')
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidFormat: NIF must contain only digits
>>> is_valid('12345678')
True
>>> is_valid('1234567')
False
>>> format('1234567')
'01234567'
"""


from stdnum.exceptions import ValidationError, InvalidFormat, InvalidLength
from stdnum.util import clean, isdigits

__all__ = ['validate', 'is_valid', 'format', 'compact']


def compact(number):
    """Convert the number to the minimal representation (remove spaces)."""
    return clean(number, '').strip()


def validate(number):
    """Check if the number is a valid Morocco personal TIN (NIF)."""
    num = compact(number)
    # Must be exactly 8 digits
    if len(num) != 8:
        raise InvalidLength('NIF must be 8 digits long')
    if not isdigits(num):
        raise InvalidFormat('NIF must contain only digits')
    return num


def is_valid(number):
    """Check if the number is a valid Morocco personal TIN (NIF)."""
    try:
        validate(number)
        return True
    except ValidationError:
        return False


def format(number):
    """Reformat the number to the standard presentation format (8 digits)."""
    num = compact(number)
    # Pad to 8 digits
    return num.zfill(8)
