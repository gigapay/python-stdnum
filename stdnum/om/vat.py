"""VAT (Omani Value Added Tax number) or VATIN.

The VAT number (VATIN) is issued by the Oman Tax Authority for VAT registered entities.
The VATIN consists of an 'OM' prefix followed by 10 digits where:
- First digit after the prefix is typically '1'
- The following digits form a sequential number
- The last digit is a check digit

VAT was introduced in Oman in April 2021.

More information:
* https://tms.taxoman.gov.om/portal/web/taxportal/vat-tax
* https://tms.taxoman.gov.om/portal/web/taxportal/tax-data-validation
* https://lookuptax.com/docs/tax-identification-number/oman-tax-id-guide
* https://www.oecd.org/content/dam/oecd/en/topics/policy-issue-focus/aeoi/oman-tin.pdf

>>> validate('1234567890')
'1234567890'
>>> validate('OM1234567890')
'1234567890'
>>> validate('OM1 2345678 90')
'1234567890'
>>> is_valid('1234567890')
True
>>> is_valid('123456789')  # too short
False
>>> is_valid('12345678901')  # too long
False
>>> is_valid('123456789A')  # non-digits
False
>>> format('1234567890')
'OM1 2345678 90'
"""

from stdnum.exceptions import *
from stdnum.util import clean, isdigits


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    number = clean(number, ' -').upper().strip()
    if number.startswith('OM'):
        number = number[2:]
    return number


def validate(number):
    """Check if the number is a valid VAT number.
    
    This checks the length and formatting."""
    number = compact(number)
    if len(number) != 10:
        raise InvalidLength()
    if not isdigits(number):
        raise InvalidFormat()
    return number


def is_valid(number):
    """Check if the number provided is a valid VAT number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Format the number according to the standard presentation format."""
    number = compact(number)
    return 'OM{} {} {}'.format(number[0], number[1:8], number[8:]) 