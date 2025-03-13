# nin.py - functions for handling United Kingdom National Insurance Numbers

"""NIN (United Kingdom National Insurance Number).

The National Insurance Number (NIN or NINO) is used in the United Kingdom to
identify individuals for the social security system. It consists of two letters,
six digits, and a final letter (suffix).

The format has several restrictions:
- First letter cannot be D, F, I, Q, U, or V
- Second letter cannot be D, F, I, Q, U, V, or O
- Certain prefix combinations are invalid: BG, GB, NK, KN, NT, TN, ZZ
- The suffix must be A, B, C, or D

More information:

* https://en.wikipedia.org/wiki/National_Insurance_number
* https://www.gov.uk/hmrc-internal-manuals/national-insurance-manual/nim39110

>>> validate('AB123456C')
'AB123456C'
>>> validate('ab 12 34 56 c')
'AB123456C'
>>> validate('DQ123456C')
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidFormat: First letter cannot be D, F, I, Q, U, or V
>>> validate('BG123456A')  # invalid prefix
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidFormat: Invalid prefix combination
>>> validate('DF123456A')  # invalid first two letters
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidFormat: First letter cannot be D, F, I, Q, U, or V
>>> format('AB123456C')
'AB 12 34 56 C'
"""

from stdnum.exceptions import *
from stdnum.util import clean, isdigits


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, ' -').strip().upper()


def validate(number):
    """Check if the number is valid. This checks the format against
    the official specifications."""
    number = compact(number)
    
    # Basic length check
    if len(number) != 9:
        raise InvalidLength()
    
    # Check first letter restrictions
    if number[0] in 'DFIQUV':
        raise InvalidFormat('First letter cannot be D, F, I, Q, U, or V')
    
    # Check second letter restrictions
    if number[1] in 'DFIQUVO':
        raise InvalidFormat('Second letter cannot be D, F, I, Q, U, V, or O')
    
    # Check for invalid prefix combinations
    invalid_prefixes = {'BG', 'GB', 'NK', 'KN', 'NT', 'TN', 'ZZ'}
    if number[:2] in invalid_prefixes:
        raise InvalidFormat('Invalid prefix combination')
    
    # Check if middle 6 characters are digits
    if not isdigits(number[2:8]):
        raise InvalidFormat('Middle 6 characters must be digits')
    
    # Check if suffix is valid
    if number[8] not in 'ABCD':
        raise InvalidFormat('Suffix must be A, B, C, or D')
    
    return number


def is_valid(number):
    """Check if the number is valid."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number, separator=' '):
    """Reformat the number to the standard presentation format."""
    number = compact(number)
    return separator.join([number[0:2], number[2:4], number[4:6], number[6:8], number[8:]])
