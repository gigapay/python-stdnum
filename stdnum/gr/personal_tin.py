'''
TODO
Comment
'''

from stdnum.exceptions import *
from stdnum.util import clean, isdigits


def compact(number):
    number = clean(number, ' :-/,')
    return number


def validate(number):
    """Check if the number is a valid identity number."""
    number = compact(number)
    if len(number) != 9:
        raise InvalidLength()
    if not isdigits(number):
        raise InvalidFormat()
    return number


def is_valid(number):
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    return compact(number)
