# eid.py - functions for handling UAE Emirates ID numbers
# ref:
#   https://www.icp.gov.ae/en/

"""Emirates ID (Emirates Identity Card Number)

The Emirates ID is a 15 digit number.

>>> validate('123456789012345')
'123456789012345'
>>> validate('1234-5678901-2345')
'123456789012345'
>>> validate('1234567890123456')
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidLength: The number has an invalid length.
>>> validate(None)
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidFormat: The number has an invalid format.
"""

import re

from stdnum.exceptions import *
from stdnum.util import clean


_eid_re = re.compile(r'^\d{15}$')


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, ' -').strip()


def validate(number):
    """Check if the number is a valid Emirates ID. This checks the length and format."""
    number = compact(number)
    if len(number) != 15:
        raise InvalidLength()
    if not _eid_re.match(number):
        raise InvalidFormat()
    return number


def is_valid(number):
    """Check if the number is a valid Emirates ID."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False
