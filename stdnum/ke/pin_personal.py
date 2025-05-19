# pin_personal.py - functions for handling Kenya Personal PIN numbers
# coding: utf-8

"""Individual PIN (Personal Identification Number, Kenya tax number).

Same as the pin.py module, but only validates individual PINs. 
Individual PINs start with 'A' and non-individual PINs start with 'P'.

More information:

* https://www.oecd.org/content/dam/oecd/en/topics/policy-issue-focus/aeoi/kenya-tin.pdf

>>> validate('P051365947M')
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidFormat: Individual PINs start with "A"
>>> validate('A004416331M')
'A004416331M'
>>> validate('12345')
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidLength: The number has an invalid length.
>>> validate('V1234567890')
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidFormat: The number has an invalid format.
>>> format('a004416331m')
'A004416331M'
"""

from stdnum.exceptions import *
from stdnum.ke import pin


def compact(number):
    return pin.compact(number)


def validate(number):
    number = pin.validate(number)
    if number[0] != 'A':
        raise InvalidFormat('Individual PINs start with "A"')
    return number


def is_valid(number):
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    return pin.format(number)
