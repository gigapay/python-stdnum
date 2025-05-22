# pin_business.py - functions for handling Kenya Business PIN numbers
# coding: utf-8

"""Business PIN (Personal Identification Number, Kenya tax number).

Same as the pin.py module, but only validates business PINs. 
Business PINs start with 'P' and individual PINs start with 'A'.

More information:

* https://www.oecd.org/content/dam/oecd/en/topics/policy-issue-focus/aeoi/kenya-tin.pdf

>>> validate('P051365947M')
'P051365947M'
>>> validate('A004416331M')
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidFormat: Business PINs start with "P"
>>> validate('V1234567890')
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidFormat: The number has an invalid format.
>>> format('p051365947m')
'P051365947M'
"""

from stdnum.exceptions import *
from stdnum.ke import pin


def compact(number):
    return pin.compact(number)


def validate(number):
    number = pin.validate(number)
    if number[0] != 'P':
        raise InvalidFormat('Business PINs start with "P"')
    return number


def is_valid(number):
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    return pin.format(number)
