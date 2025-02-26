# trn.py - functions for handling UAE TRN numbers
# ref:
#   https://www.cleartax.com/ae/trn-verification-uae
#   https://tax.gov.ae/en/services/vat.registration.aspx

"""TRN (Tax Registration Number)

The TRN is a 15 digit number.

>>> validate('123456789012345')
'123456789012345'
>>> validate('1234-5678901-2345')
'123456789012345'
>>> validate('1234567890123456')
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidLength: The number has an invalid length.
"""

import re

from stdnum.exceptions import *
from stdnum.util import clean


_trn_re = re.compile(r'^\d{15}$')


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, ' -').strip()


def validate(number):
    """Check if the number is a valid TRN. This checks the length and format."""
    number = compact(number)
    if len(number) != 15:
        raise InvalidLength()
    if not _trn_re.match(number):
        raise InvalidFormat()
    return number


def is_valid(number):
    """Check if the number is a valid TRN."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False
