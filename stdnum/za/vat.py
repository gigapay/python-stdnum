# vat.py - functions for handling South African VAT numbers

"""VAT (South African Value Added Tax number).

The South African VAT number is a unique identifier issued to businesses 
registered for Value Added Tax (VAT) in South Africa by the South African 
Revenue Service (SARS).

VAT numbers in South Africa start with digit 4 and consist of 10 digits.

More information:
* https://www.sars.gov.za/

>>> validate('4123456789')
'4123456789'
>>> validate('412345678')
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidLength: The number has an invalid length.
>>> validate('41')
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidLength: The number has an invalid length.
>>> validate('5123456789')
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidFormat: The number has an invalid format.
"""

from stdnum.exceptions import *
from stdnum.util import clean, isdigits
from stdnum import luhn


__all__ = ['compact', 'validate', 'is_valid', 'format']


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, '').strip()


def validate(number):
    """Check if the number is a valid South African VAT number.
    This checks the format, length, and components."""
    number = compact(number)
    
    if len(number) != 10:
        raise InvalidLength()
    
    if not isdigits(number):
        raise InvalidFormat()
    
    if not number.startswith('4'):
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
    return number
