# business_tin.py - functions for handling Kuwait Business Tax Identification Number

"""Business TIN (Kuwait Business Tax Identification Number).

The Business Tax Identification Number (TIN) is a unique identifier issued
by the Kuwait tax authorities to businesses operating in Kuwait.

The number consists of 6 digits and cannot be all zeros.

More information:

* https://www.oecd.org/content/dam/oecd/en/topics/policy-issue-focus/aeoi/kuwait-tin.pdf

>>> validate('123456')
'123456'
>>> validate('1234567')
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidLength: The number has an invalid length.
>>> validate('000000')
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidComponent: Business TIN cannot be all zeros
>>> format('123456')
'123456'
"""

from stdnum.exceptions import *
from stdnum.util import clean, isdigits


__all__ = ['compact', 'validate', 'is_valid', 'format']


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, '').strip()


def validate(number):
    """Check if the number is a valid Kuwait business TIN. This checks the length,
    formatting and digits."""
    number = compact(number)
    if len(number) != 6:
        raise InvalidLength()
    if not isdigits(number):
        raise InvalidFormat()
    if number == '000000':
        raise InvalidComponent('Business TIN cannot be all zeros')
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
