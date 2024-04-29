import re

from stdnum.exceptions import InvalidChecksum, InvalidFormat, InvalidLength, ValidationError


_brn_re = re.compile('^([A-Z])?([A-Z])([0-9]{6})([0-9A])$')


def is_valid_checksum(number):
    """Calculate the check digit for the number."""
    weight = [9, 8, 7, 6, 5, 4, 3, 2, 1]
    values = list('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') + [None]
    match = _brn_re.match(number)
    if not match: return False
    hkidArr = []
    for g in match.groups():
      hkidArr += list(g) if g else [g]
    r = sum([values.index(i) * w for i, w in zip(hkidArr, weight)]) % 11
    return r == 0


def validate(number):
    """Check if the number provided is a valid HKID."""
    if not len(number) in [8, 9]:
        raise InvalidLength()
    if not _brn_re.match(number):
        raise InvalidFormat()
    if not is_valid_checksum(number):
        raise InvalidChecksum()
    return number


def is_valid(number):
    """Check if the number provided is a valid HKID."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False

