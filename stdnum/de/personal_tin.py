from collections import defaultdict

from stdnum.exceptions import *
from stdnum.util import clean, isdigits

from .idnr import validate as idnr_validate
from .stnr import validate as stnr_validate


def compact(number):
    return clean(number, ' -./,').strip()


def validate(number):
    """
    TODO
    Not perfect, bad code!
    """
    number = compact(number)
    if stnr_is_valid(number) or idnr_validate(number):
        return number
    raise InvalidFormat()


def is_valid(number):
    """Check if the number provided is a valid tax identification number.
    This checks the length, formatting and check digit."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False

