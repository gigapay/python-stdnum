# business.py - functions for handling Hungarian business tin numbers
# coding: utf-8


"""TODO
"""

from stdnum.exceptions import *
from stdnum.util import clean, isdigits
from .anum import is_valid as anum_is_valid


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    number = clean(number, ' -').upper().strip()
    if number.startswith('HU'):
        number = number[2:]
    return number


def validate(number):
    """Check if the number is a valid VAT number. This checks the length,
    formatting and check digit."""
    number = compact(number)
    if not isdigits(number):
        raise InvalidFormat()
    if len(number) not in [8,11]:
        raise InvalidLength()
    if len(number) == 11:
        anum_valid = anum_is_valid(number[:8])
        vat_diget_valid = number[8] in ['1', '2']
        rest_valid = 0 <= int(number[9:]) < 100
        if not (anum_valid and vat_diget_valid and rest_valid):
            raise InvalidChecksum()
    if len(number) == 8:
        if not anum_is_valid(number):
            raise InvalidChecksum()

    return number


def is_valid(number):
    """Check if the number provided is a valid VAT number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False
