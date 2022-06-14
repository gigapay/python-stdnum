from stdnum.exceptions import *
from stdnum.util import clean, isdigits


def compact(number):
    number = clean(number, ' -/,').upper().strip()
    return number


def validate(number):
    """Check if the number is a valid VAT number. This checks the length,
    formatting and check digit."""
    number = compact(number)
    if not isdigits(number):
        raise InvalidFormat()
    if len(number) != 10:
        raise InvalidLength()
    return number


def is_valid(number):
    """Check if the number provided is a valid VAT number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False