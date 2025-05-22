# personal_tin.py - functions for handling Nigerian Personal Tax Identification Number

"""Personal TIN (Nigerian Personal Tax Identification Number).

The Personal Tax Identification Number (TIN) is a unique identifier issued
by  States Board of Internal Revenue/Federal (JTB) to individuals in Nigeria.

The number consists of 10 digits.

More information:

* https://www.oecd.org/content/dam/oecd/en/topics/policy-issue-focus/aeoi/nigeria-tin.pdf

>>> compact('1234567890')
'1234567890'
>>> validate('1234567890')
'1234567890'
>>> validate('123456789A')
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidFormat: The number has an invalid format.
>>> validate('12345678901')
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidLength: The number has an invalid length.
>>> format('1234567890')
'1234-5678-90'
"""

from stdnum.exceptions import *
from stdnum.util import clean, isdigits


__all__ = ['compact', 'validate', 'is_valid', 'format']


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, '').strip()  # separators are not allowed


def validate(number):
    """Check if the number is a valid Nigerian personal TIN. This checks the length,
    formatting and digits."""
    number = compact(number)
    if len(number) != 10:
        raise InvalidLength()
    if not isdigits(number):
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
    return '-'.join((number[0:4], number[4:8], number[8:10]))
