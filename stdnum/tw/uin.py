# uin.py - functions for handling Taiwanese uin (TIN) numbers
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

"""UI Number (Unified Identification number)

The UI Number is a 10-digit number used to identify foreigners.
The number consists of two alphabetic letter followed by 8 numeric digits.
>>> validate('GB12233445')
'GB12233445'
>>> validate('GB12233446')  # invalid check digit
Traceback (most recent call last):
    ...
InvalidChecksum: ...
>>> validate('GB1223344')  # digit missing
Traceback (most recent call last):
    ...
InvalidLength: ...
"""

import math

from stdnum.exceptions import *
from stdnum.util import clean, isdigits


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""

    return clean(number, ' -').upper().strip()


def calc_check_digit(number):
    """Calculate the check digit. The number passed should not have the
    check digit included.
    Source: https://identity.tw/"""
    id_letters = 'ABCDEFGHJKLMNPQRSTUVXYWZIO'
    letter_index = id_letters.index(number[0])
    checksum = math.floor(letter_index / 10 + 1) + (letter_index * 9)
    checksum += (id_letters.index(number[1]) % 10) * 8
    checksum += sum((9 - position) * int(number[position]) for position in range(2, 9))
    checksum += int(number[9])
    return checksum % 10


def validate(number):
    """Check if the number provided is a valid UI Number. This checks the
        length, formatting and check digit."""
    number = compact(number)
    if not isdigits(number[2:]):
        raise InvalidFormat()
    if len(number) != 10:
        raise InvalidLength()
    if number[1] not in ('A', 'B', 'C', 'D'):
        raise InvalidComponent()
    if calc_check_digit(number) != 0:
        raise InvalidChecksum()
    return number


def is_valid(number):
    """Check if the number provided is a valid UI Number. This checks the
    length, formatting and check digit."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False
