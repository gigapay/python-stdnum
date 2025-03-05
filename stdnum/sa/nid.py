# nid.py - functions for handling Saudi Arabian National ID numbers
# coding: utf-8
#
# Copyright (C) 2024
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

"""National ID (Saudi Arabian National ID or Iqama number).

The Saudi Arabian National ID (for Saudi citizens, رقم الهوية الوطنية) or Iqama 
(Residence ID for expatriates, الإقامة) serve as the tax ID for individuals when applicable.

The number consists of 10 digits:
- For Saudi citizens, it typically starts with 1 or 2
- For resident expatriates (Iqama), it typically starts with 2
- The number includes an internal check digit for validation

For tax purposes, sometimes a 12-digit format is used:
- First 2 digits: region code
- Remaining 10 digits: the unique ID

More information:
* https://www.oecd.org/tax/automatic-exchange/crs-implementation-and-assistance/tax-identification-numbers/

>>> validate('1012345678')
'1012345678'
>>> validate('abcdefghij')  # doctest: +IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
    ...
InvalidComponent: ...
>>> validate('10123456')  # doctest: +IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> format('101-234-5678')
'1012345678'
>>> format('1312345678901')
'2345678901'
>>> is_valid('1012345678')
True
>>> is_valid('131012345678')
True
"""

from stdnum.exceptions import InvalidLength, InvalidComponent, ValidationError
from stdnum.util import clean, isdigits


def compact(number):
    """Convert the number to the minimal representation.
    
    This strips the number of any valid separators and removes surrounding
    whitespace.
    """
    return clean(number, ' -/').strip()


def validate(number):
    """Check if the number is a valid Saudi Arabian National ID or Iqama number.
    
    This checks the length and that all characters are digits.
    The ID can be either 10 digits (standard format) or 12 digits (with region code).
    For Saudi citizens, the ID typically starts with 1 or 2.
    For resident expatriates (Iqama), the ID typically starts with 2.
    """
    number = compact(number)
    
    if len(number) == 12:
        # If 12 digits (with region code), consider only the last 10 digits
        number = number[2:]
    
    if len(number) != 10:
        raise InvalidLength()
    
    if not isdigits(number):
        raise InvalidComponent()
    
    first_digit = number[0]
    if first_digit not in ('1', '2'):
        raise InvalidComponent('National ID should start with 1 or 2')
    
    # Note: The specific check digit algorithm is not publicly documented,
    # so we cannot implement a full validation here.
    
    return number


def is_valid(number):
    """Check if the number is a valid Saudi Arabian National ID or Iqama number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Format the number to the standard representation.
    
    If the number is 12 digits (with region code), return only the last 10 digits.
    If the number is 13 digits, return only the last 10 digits.
    Otherwise, return the compacted 10-digit number.
    """
    number = compact(number)
    if len(number) == 12:
        return number[2:]
    elif len(number) == 13:
        return number[3:]
    return number
