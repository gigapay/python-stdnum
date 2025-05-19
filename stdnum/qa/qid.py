# qid.py - functions for handling Qatar ID numbers

"""QID (Qatar ID number).

The Qatar ID (QID) is a unique identification number assigned to Qatari
citizens and residents.

A valid QID must:
- Be exactly 11 digits
- Start with '2' (for birth years 1900–1999) or '3' (for birth years 2000+)
- Next two digits: year of birth (00–99)
- Next three digits: ISO 3166-1 numeric country code (000–999)
- Last five digits: sequence number (00000–99999)

More information:
* https://www.dohaguides.com/qatar-id-number/

>>> validate('29012345678')
'29012345678'
>>> validate('30123456789')
'30123456789'
>>> format('29012345678')
'2 90 123 45678'
>>> validate('12345678901')
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidFormat: The number has an invalid format.
>>> validate('2901234567')
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidLength: The number has an invalid length.
>>> validate('290A2345678')
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidFormat: The number has an invalid format.
"""

from stdnum.exceptions import *
from stdnum.util import clean, isdigits


__all__ = ['compact', 'validate', 'is_valid', 'format']


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, '').strip()


def validate(number):
    """Check if the number is a valid Qatar ID (QID).
    
    This checks the length, starting digit, and format.
    """
    number = compact(number)
    
    if len(number) != 11:
        raise InvalidLength()
    if not isdigits(number):
        raise InvalidFormat()
    if number[0] not in ('2', '3'):
        raise InvalidFormat()
    
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
    return f"{number[0]} {number[1:3]} {number[3:6]} {number[6:]}"
