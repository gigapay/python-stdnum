# nid.py - functions for handling Bahrain National ID numbers

"""BH NID (Bahrain National ID number).

The Bahrain National ID number (also known as CPR - Central Population 
Registration number or Personal Number) is a unique identifier issued by the 
Information & eGovernment Authority (iGA) to all citizens and residents of Bahrain.

The number consists of 9 digits and is used for identification, government 
services, banking, healthcare, and can be used as a travel document within 
GCC countries.

The general format is YYMMNNNNC where:
- YY = year of birth (last 2 digits)
- MM = month of birth
- NNNN = sequential number
- C = check digit

However, some citizens have numbers that don't follow this exact format,
particularly older registrations or special cases.

More information:
* https://www.iga.gov.bh/en/category/id-card-and-civil-record-services
* https://www.bahrain.bh/wps/portal/IDInfo_en

>>> validate('520202236')
'520202236'
>>> validate('52020223')  # invalid length
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidLength: The number has an invalid length.
>>> validate('52020223A')  # invalid format
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidFormat: The number has an invalid format.
>>> is_valid('520202236')
True
>>> is_valid('52020223A')
False
>>> format('520202236')
'520-202-236'
"""

from stdnum.exceptions import *
from stdnum.util import clean, isdigits


__all__ = ['compact', 'validate', 'is_valid', 'format']


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, '').strip()


def validate(number):
    """Check if the number is a valid Bahrain National ID. This checks the 
    length and formatting."""
    number = compact(number)
    if len(number) != 9:
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
    return '-'.join((number[0:3], number[3:6], number[6:9]))
