# nidcn.py - functions for handling Taiwanese nidcn (TIN) numbers
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

"""National ID Card Number

The National ID Card Number is a 10-digit number used to identify Tiwanese citizens.
The number consists of an alphabetic letter followed by 9 numeric digits.

Foreign national, since 2021 are issued a UIN (Unified Identification number) instead.
>>> validate('G112233445')
'G112233445'
>>> validate('G112233446')  # invalid check digit
Traceback (most recent call last):
    ...
InvalidChecksum: ...
>>> validate('G11223344')  # digit missing
Traceback (most recent call last):
    ...
InvalidLength: ...
"""
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
    checksum += sum((9 - position) * int(number[position]) for position in range(1, 9))
    checksum += int(number[9])
    return checksum % 10


def validate(number):
    """Check if the number provided is a valid National ID Card Number. This checks the
        length, formatting and check digit."""
    number = compact(number)
    if not isdigits(number[1:]):
        raise InvalidFormat()
    if len(number) != 10:
        raise InvalidLength()
    if number[1] not in ('1', '2', '8', '9'):
        raise InvalidComponent()
    if calc_check_digit(number) != 0:
        raise InvalidChecksum()
    return number


def is_valid(number):
    """Check if the number provided is a valid NIDCN. This checks the
    length, formatting and check digit."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False
