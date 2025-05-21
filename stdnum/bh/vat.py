# vat.py - functions for handling Bahrain VAT numbers

"""VAT (Bahrain Value Added Tax number).

The Bahrain VAT number is a unique identifier issued to businesses 
registered for Value Added Tax (VAT) in Bahrain by the National Bureau for Revenue.

Bahrain VAT numbers consist of 15 digits.

More information:
* https://www.nbr.gov.bh/

>>> validate('123456789012345')
'123456789012345'
>>> format('123456789012345')
'123456789012345'
>>> validate('12345')
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidLength: The number has an invalid length.
>>> validate('12345678901234A')
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
    """Check if the number is a valid Bahrain VAT number.
    This checks the format and length."""
    number = compact(number)
    
    if not isdigits(number):
        raise InvalidFormat()
    
    if len(number) != 15:
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
    return number