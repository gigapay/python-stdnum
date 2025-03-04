# personal_tin.py - functions for handling Maltese Personal Tax Identification Numbers

"""MT Personal TIN (Maltese Personal Tax Identification Number).

The Maltese Personal Tax Identification Number is used for tax purposes in Malta.
It can be in one of two formats:
- National format: 7 digits followed by a letter (M, G, A, P, L, H, B, or Z)
- Non-national format: 9 digits

More information:
* https://www.oecd.org/content/dam/oecd/en/topics/policy-issue-focus/aeoi/malta-tin.pdf

>>> validate('1234567M')
'1234567M'
>>> validate('123 456 7M')
'1234567M'
>>> validate('123456789')
'123456789'
>>> validate('123-456-789')
'123456789'
>>> validate('1234567X')  # invalid letter
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidFormat: National format must be 7 digits followed by M, G, A, P, L, H, B, or Z
>>> validate('1234567')  # invalid length
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidLength: Number must be 8 characters (national format) or 9 digits (non-national format)
>>> validate('12345678A')  # invalid format (8 digits + letter)
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidFormat: Non-national format must be 9 digits
>>> is_valid('1234567M')
True
>>> is_valid('1234567X')
False
"""

import re
from stdnum.exceptions import *
from stdnum.util import clean, isdigits


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    number = clean(number, ' -,/').upper().strip()
    return number


def validate(number):
    """Check if the number is valid. This checks the format against
    the official specifications."""
    number = compact(number)

    # Check Maltese national format: 7 digits + 1 valid letter
    if len(number) == 8:
        if not re.fullmatch(r'^[0-9]{7}[MGAPLHBZ]$', number, flags=re.IGNORECASE):
            raise InvalidFormat('National format must be 7 digits followed by M, G, A, P, L, H, B, or Z')
    # Check non-national format: 9 digits
    elif len(number) == 9:
        if not isdigits(number):
            raise InvalidFormat('Non-national format must be 9 digits')
    else:
        raise InvalidLength('Number must be 8 characters (national format) or 9 digits (non-national format)')
    
    return number


def is_valid(number):
    """Check if the number is valid."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False