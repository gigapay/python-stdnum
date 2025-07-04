# jmbg.py - functions for handling Serbian JMBG numbers
# coding: utf-8
#
# Copyright (C) 2025 Arthur de Jong
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

"""JMBG (Jedinstveni Matični Broj Građana, Serbian Unique Master Citizen Number).

The Serbian Unique Master Citizen Number consists of 13 digits where the last
digit is a check digit. The number encodes the birth date and region of birth.

>>> validate('0101006500006')
'0101006500006'
>>> validate('0101006500007')
Traceback (most recent call last):
    ...
InvalidChecksum: ...
>>> validate('123456789012')  # Wrong length
Traceback (most recent call last):
    ...
InvalidLength: ...
"""

from stdnum.exceptions import *
from stdnum.iso7064 import mod_11_10
from stdnum.util import clean, isdigits


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, ' -.').strip()


def validate(number):
    """Check if the number is a valid JMBG number. This checks the length,
    formatting and check digit."""
    number = compact(number)
    if not isdigits(number):
        raise InvalidFormat()
    if len(number) != 13:
        raise InvalidLength()
    mod_11_10.validate(number)
    return number


def is_valid(number):
    """Check if the number is a valid JMBG number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False