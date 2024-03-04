# personal_tin.py - functions for handling Taiwanese TIN numbers
# coding: utf-8
#
# Copyright (C) 2012, 2013 Arthur de Jong
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301 USA

""" Personal TIN

The Taiwanese personal TIN is a 10-digit number where either the first,
or the first two digits are alphabetic letters and the rest are numbers.

The number is either a National ID Card Number (for native Taiwanese), or
a UI Number (Unified Identification number, for foreigners)
>>> validate('G112233445')
'G112233445'
>>> validate('G112233446')  # invalid check digit
Traceback (most recent call last):
    ...
InvalidChecksum: ...
>>> validate('GB12233445')  # foreign person
'GB12233445'
"""

from stdnum.tw import nidcn, uin
from stdnum.exceptions import *
from stdnum.util import clean, isdigits


def compact(number):
    """Convert the number to the minimal representation.

    This strips the number of any valid separators and removes surrounding
    whitespace.
    """
    return clean(number, ' -').strip()


def validate(number):
    """Check if the number provided is a valid personal TIN number. This checks the
        length, formatting and check digit."""
    number = compact(number)
    if not isdigits(number[2:]):
        raise InvalidFormat()
    if len(number) != 10:
        raise InvalidLength()
    if isdigits(number[1]):
        # if the second digit is a number we now that it is no a UI Number
        # there for it must be a National ID Card Number
        nidcn.validate(number)
    elif not isdigits(number[1]):
        # UI Number
        uin.validate(number)
    return number


def is_valid(number):
    """Check if the number provided is a valid personal TIN number. This checks the
        length, formatting and check digit."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False
