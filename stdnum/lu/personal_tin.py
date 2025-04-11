from stdnum.exceptions import InvalidFormat, InvalidLength, ValidationError, InvalidChecksum
from stdnum.util import clean, isdigits
from stdnum import luhn, verhoeff


"""Luxembourg personal TIN (Tax Identification Number).

The Luxembourg personal TIN is a 13-digit code that follows this format:
- First 8 digits represent birth date (YYYYMMDD)
- Next 3 digits ensure uniqueness for people born on the same date (XXX)
- The 12th digit is a check digit using Luhn algorithm on the first 11 digits
- The 13th digit is a check digit using Verhoeff algorithm on the first 12 digits

>>> validate('2000060500127')
'2000060500127'
>>> is_valid('2000060500127')
True
>>> is_valid('2000060500128')  # invalid check digit
False
>>> compact(' 2000-060-500127 ')
'2000060500127'
>>> validate('200006050012X')  # non-digit
Traceback (most recent call last):
    ...
InvalidFormat: ...
>>> validate('20000605001')  # too short
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> validate('2000060500128')  # invalid check digits
Traceback (most recent call last):
    ...
InvalidChecksum: ...
>>> calc_check_digits('20000605001')
('2', '7')
>>> calc_check_digits('20000605001')[0]  # Luhn digit
'2'
>>> calc_check_digits('20000605001')[1]  # Verhoeff digit
'7'
>>> calc_check_digits('2000060500')  # too short
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> base = '20000605001'  # Base number (YYYYMMDDXXX)
>>> luhn_digit, verhoeff_digit = calc_check_digits(base)
>>> validate(base + luhn_digit + verhoeff_digit)  # Valid TIN
'2000060500127'
"""


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    number = clean(number, ' -/').upper().strip()
    return number


def validate(number):
    """Check if the number provided is a valid Luxembourg personal TIN.

    The number is a 13-digit code:
    - First 8 digits represent birth date (YYYYMMDD)
    - Next 3 digits ensure uniqueness for people born on the same date (XXX)
    - The 12th digit is a check digit using Luhn algorithm on the first 11 digits
    - The 13th digit is a check digit using Verhoeff algorithm on the first 12 digits"""
    number = compact(number)
    if not isdigits(number):
        raise InvalidFormat()
    if len(number) != 13:
        raise InvalidLength()

    # Check birthdate format (basic validation)
    year = int(number[0:4])
    month = int(number[4:6])
    day = int(number[6:8])
    if year < 1800 or year > 2100 or month < 1 or month > 12 or day < 1 or day > 31:
        raise InvalidFormat()

    # Calculate expected check digits using our calc_check_digits function
    luhn_digit, verhoeff_digit = calc_check_digits(number[:11])
    
    # Validate the check digits
    if luhn_digit != number[11]:
        raise InvalidChecksum('First check digit (Luhn) is invalid')
    if verhoeff_digit != number[12]:
        raise InvalidChecksum('Second check digit (Verhoeff) is invalid')

    return number


def is_valid(number):
    """Check if the number provided is a valid Luxembourg personal TIN."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def calc_check_digits(number):
    """Calculate the two check digits for the number provided.
    The first check digit uses the Luhn algorithm on the first 11 digits.
    The second check digit uses the Verhoeff algorithm on the first 12 digits.
    
    Returns a tuple with both check digits as strings.
    
    The input must be exactly 11 digits (YYYYMMDDXXX)."""
    number = compact(number)
    
    # For the Luxembourg TIN, we need exactly 11 digits to calculate the check digits
    if len(number) != 11:
        raise InvalidLength('Need exactly 11 digits (YYYYMMDDXXX) to calculate check digits')
    
    # Calculate the Luhn check digit for the 11 digits
    luhn_digit = luhn.calc_check_digit(number)
    
    # Calculate the Verhoeff check digit for the first 12 digits (including the Luhn check digit)
    verhoeff_digit = verhoeff.calc_check_digit(number + luhn_digit)
    
    return (luhn_digit, verhoeff_digit)

