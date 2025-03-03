"""CID (Omani Civil ID Number).

The Omani Civil ID Number is a unique identifier assigned to citizens and residents
of Oman. It is used for identification purposes on the Omani National ID Card 
(Civil Card).

The CID in Oman is a numeric sequence comprising exactly 8 digits.

More information:
* https://www.rop.gov.om/english/id_card.html

>>> validate('12345678')
'12345678'
>>> validate('1234 5678')
'12345678'
>>> is_valid('12345678')
True
>>> is_valid('')  # empty
False
>>> is_valid('1234567')  # too short
False
>>> is_valid('123456789')  # too long
False
>>> is_valid('1234567A')  # non-digits
False
>>> format('12345678')
'12345678'
"""

from stdnum.exceptions import *
from stdnum.util import clean, isdigits


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, ' -').strip()


def validate(number):
    """Check if the number is a valid Civil ID Number.
    
    This checks that the number is a numeric sequence of exactly 8 digits."""
    number = compact(number)
    if not number:
        raise InvalidFormat("Empty number provided")
    if len(number) != 8:
        raise InvalidLength("The number must be exactly 8 digits long")
    if not isdigits(number):
        raise InvalidFormat("The number must contain only digits")
    return number


def is_valid(number):
    """Check if the number provided is a valid Civil ID Number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Format the number according to the standard presentation format."""
    return compact(number) 