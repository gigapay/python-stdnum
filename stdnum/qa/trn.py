# trn.py - functions for handling Qatar Tax Registration Numbers

"""TRN (Qatar Tax Registration Number).

The Qatar Tax Registration Number (TRN) is a unique identifier issued by the
General Tax Authority (GTA) to businesses and individuals for tax purposes
in Qatar.

There are two types of TRNs:

1. Mainland (GTA) TRN: A 10-digit number that starts with '5' (the GCC-state
   prefix for Qatar) and includes a check digit.

2. Qatar Financial Centre (QFC) TRN: Always begins with the letter 'T',
   followed by the QFC license number. The length varies.

More information:
* https://www.oecd.org/content/dam/oecd/en/topics/policy-issue-focus/aeoi/qatar-tin.pdf

>>> validate('5000000109')
'5000000109'
>>> validate('5000535401')
'5000535401'
>>> validate('T12345')
'T12345'
>>> format('5123456789')
'5123456789'
>>> format('T12345')
'T12345'
>>> validate('512345678')
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidLength: The number has an invalid length.
>>> validate('6123456789')
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidFormat: The number has an invalid format.
>>> validate('5123456780')
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidChecksum: The number's checksum or check digit is invalid.
>>> validate('512345678X')
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidFormat: The number has an invalid format.
>>> validate('A12345')
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidLength: The number has an invalid length.
>>> validate('T')
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidLength: The number has an invalid length.
>>> validate('T123A5')  
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidFormat: The number has an invalid format.
"""

from stdnum.exceptions import *
from stdnum.util import clean, isdigits
from stdnum import luhn


__all__ = ['compact', 'validate', 'is_valid', 'format', 'is_mainland', 'is_qfc']


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, '').upper().strip()


def validate(number):
    """Check if the number is a valid Qatar TRN.
    
    This validates either a Mainland (GTA) TRN or a QFC TRN based on format.
    For Mainland TRNs, this checks the length, prefix, and check digit.
    For QFC TRNs, this checks the format (T followed by digits).
    """
    number = compact(number)
    
    if number[0] == 'T':
        if len(number) < 2:
            raise InvalidLength()
        if not isdigits(number[1:]):
            raise InvalidFormat()
    else:
        if len(number) != 10:
            raise InvalidLength()
        if number[0] != '5':
            raise InvalidFormat()
        luhn.validate(number[1:])

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
