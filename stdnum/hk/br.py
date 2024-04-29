from stdnum.exceptions import InvalidFormat, InvalidLength, ValidationError
from stdnum.util import isdigits


def validate(number):
    """Check if the number provided is a valid BR number."""
    if not len(number) == 8:
        raise InvalidLength()
    if not isdigits(number):
        raise InvalidFormat()
    return number


def is_valid(number):
    """Check if the number provided is a valid CAS RN."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False
