
from stdnum.exceptions import *
from stdnum.util import clean, isdigits


def compact(number):
    number = clean(number, ' -/').upper().strip()
    return number


def validate(number):
    """
    TODO
    simple regex check
    """
    number = compact(number)
    if not isdigits(number):
        raise InvalidFormat()
    if len(number) != 13:
        raise InvalidLength()

    return number


def is_valid(number):
    try:
        return bool(validate(number))
    except ValidationError:
        return False