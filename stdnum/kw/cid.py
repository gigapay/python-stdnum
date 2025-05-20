# cid.py - functions for handling Kuwait Civil ID (CID) numbers

"""CID (Kuwait Civil ID).

The Civil ID (CID) is a unique identifier issued to citizens and residents
of Kuwait by the Public Authority for Civil Information (PACI).

The number consists of 12 digits where the first 6 digits encode the birth date
in the format YYMMDD, and the last digit is a check digit.

More information:

* https://www.oecd.org/content/dam/oecd/en/topics/policy-issue-focus/aeoi/kuwait-tin.pdf
* https://prakhar.me/articles/kuwait-civil-id-checksum/
* https://patientsknowbest.github.io/nhsnum/

>>> validate('288020122596')
'288020122596'
>>> validate('227081660516')
'227081660516'
>>> validate('292091998298')
'292091998298'
>>> validate('292091998297')
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidChecksum: The number's checksum or check digit is invalid.
>>> validate('29209199829')
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidLength: The number has an invalid length.
>>> validate('288200122596')
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidComponent: Invalid birth date encoded in the Civil ID
"""

from datetime import date
from stdnum.exceptions import *
from stdnum.util import clean, isdigits


__all__ = ['compact', 'validate', 'is_valid', 'format']


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, '').strip()


def validate(number):
    """Check if the number is a valid Kuwait Civil ID. This checks the length,
    formatting, birth date and check digit."""
    number = compact(number)
    if len(number) != 12:
        raise InvalidLength()
    if not isdigits(number):
        raise InvalidFormat()
    
    # Validate birth date (YYMMDD) - starts from 2nd digit (index 1)
    yy, mm, dd = int(number[1:3]), int(number[3:5]), int(number[5:7])
    current_two_digit = date.today().year % 100
    century = 2000 if yy <= current_two_digit else 1900
    
    try:
        birth_date = date(century + yy, mm, dd)
    except ValueError:
        raise InvalidComponent('Invalid birth date encoded in the Civil ID')
    
    # Calculate and validate check digit
    weights = [2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    total = sum(int(d) * w for d, w in zip(number[:11], weights))
    
    check_digit = (11 - (total % 11)) % 11
    if check_digit == 10:
        raise InvalidChecksum('Invalid check digit configuration')
    
    if check_digit != int(number[11]):
        raise InvalidChecksum()
    
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
    return f"{number[0:1]} {number[1:5]} {number[5:9]} {number[9:12]}"
