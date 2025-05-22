# crn.py - functions for handling Bahrain Commercial Registration numbers

"""CRN (Bahrain Commercial Registration Number).

The Commercial Registration Number (CRN) is a unique identifier issued to 
businesses registered in Bahrain by the Ministry of Industry and Commerce.

Bahrain CRNs are typically numeric and may include certain patterns and validations
specific to Bahrain's business registration system.

More information:
* https://www.sijilat.bh/public-search-cr/search-cr-2.aspx

>>> validate('1234567')
'1234567'
>>> validate('123456')
'123456'
>>> validate('12345-6')
'123456'
>>> format('1234567')
'12345-67'
>>> validate('abc123')
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidFormat: The number has an invalid format.
>>> validate('12345')
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidLength: The number has an invalid length.
>>> validate('12345678')
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidLength: The number has an invalid length.
"""

from stdnum.exceptions import *
from stdnum.util import clean, isdigits


__all__ = ['compact', 'validate', 'is_valid', 'format']


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, '-').strip()


def validate(number):
    """Check if the number is a valid Bahrain Commercial Registration Number.
    This checks the format and length."""
    number = compact(number)
    
    if not isdigits(number):
        raise InvalidFormat()
    
    if len(number) != 6 and len(number) != 7:
        raise InvalidLength()
    
    return number


def is_valid(number):
    """Check whether the number is valid."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Reformat the number to the standard presentation format."""
    number = compact(number)
    return f"{number[:5]}-{number[5:]}"
