from stdnum.exceptions import *
from stdnum.util import clean, isdigits


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    number = clean(number, ' -').upper().strip()
    if number.startswith('CY'):
        number = number[2:]
    return number


def validate(number):
    '''
    TODO
    Basic format check
    '''
    number = compact(number)
    if not isdigits(number[:-1]) or isdigits(number[-1]):
        raise InvalidFormat()
    if len(number) != 9:
        raise InvalidLength()
    return number


def is_valid(number):
    """Check if the number is a valid VAT number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False