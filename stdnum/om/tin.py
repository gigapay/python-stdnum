"""TIN (Omani Tax Identification Number).

The Omani Tax Identification Number is a unique identifier assigned by the
Oman Tax Authority to taxpayers (companies only, not individuals).

The TIN in Oman is a numeric sequence comprising up to seven digits, represented as {xxxxxxx}.

More information:
* https://tms.taxoman.gov.om/
* https://lookuptax.com/docs/tax-identification-number/oman-tax-id-guide
* https://www.oecd.org/content/dam/oecd/en/topics/policy-issue-focus/aeoi/oman-tin.pdf

>>> validate('123456')
'123456'
>>> validate('1 234 567')
'1234567'
>>> is_valid('1234567')
True
>>> is_valid('')  # empty
False
>>> is_valid('12345678')  # too long
False
>>> is_valid('123456A')  # non-digits
False
>>> format('1234567')
'1234567'
"""

from stdnum.exceptions import *
from stdnum.util import clean, isdigits


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, ' -').strip()


def validate(number):
    """Check if the number is a valid TIN.
    
    This checks that the number is a numeric sequence of up to seven digits."""
    number = compact(number)
    if not number:
        raise InvalidFormat("Empty number provided")
    if len(number) > 7:
        raise InvalidLength("The number must be at most 7 digits long")
    if not isdigits(number):
        raise InvalidFormat("The number must contain only digits")
    return number


def is_valid(number):
    """Check if the number provided is a valid TIN."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Format the number according to the standard presentation format."""
    return compact(number) 