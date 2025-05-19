# business_tin.py - functions for handling Nigerian Business Tax Identification Number

"""Business TIN (Nigerian Business Tax Identification Number).

The Business Tax Identification Number (TIN) is a unique identifier issued
by the Federal Inland Revenue Service (FIRS) to businesses in Nigeria.

The number consists of 12 digits, sometimes with a hyphen separating the first 8
digits from the last 4 digits.

More information:

* https://www.oecd.org/content/dam/oecd/en/topics/policy-issue-focus/aeoi/nigeria-tin.pdf

>>> validate('123456789012')
'123456789012'
>>> validate('12345678-9012')
'123456789012'
>>> validate('123-456789012')
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidFormat: The hyphen must separate 8 digits and 4 digits.
>>> validate('1234567890123')
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidLength: The number has an invalid length.
>>> validate('1234567890AB')
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidFormat: The number contains non-numeric characters.
>>> format('123456789012')
'12345678-9012'
"""

from stdnum.exceptions import *
from stdnum.util import clean, isdigits


__all__ = ['compact', 'validate', 'is_valid', 'format']


def compact(number):
    """Convert the number to the minimal representation. This strips
    surrounding whitespace and removes the hyphen if present."""
    return clean(number, '').strip()


def validate(number):
    """Check if the number is a valid Nigerian business TIN. This checks the length,
    formatting and digits."""
    number = compact(number)
    
    if '-' in number:
        parts = number.split('-')
        if len(parts) != 2:
            raise InvalidFormat("The number must contain exactly one hyphen.")
        if len(parts[0]) != 8 or len(parts[1]) != 4:
            raise InvalidFormat("The hyphen must separate 8 digits and 4 digits.")
        if not isdigits(parts[0]) or not isdigits(parts[1]):
            raise InvalidFormat("The number contains non-numeric characters.")
        number = parts[0] + parts[1]
    else:
        if len(number) != 12:
            raise InvalidLength()
        if not isdigits(number):
            raise InvalidFormat("The number contains non-numeric characters.")
    
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
    return number[0:8] + '-' + number[8:12]