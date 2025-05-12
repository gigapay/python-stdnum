# tin.py - functions for handling Sri Lankan Personal Tax Identification Number
#
# Copyright (C) 2023 The python-stdnum contributors
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

"""TIN (Sri Lanka Personal Tax Identification Number).

The Tax Identification Number (TIN) is a 9-digit unique identifier 
issued by the Inland Revenue Department to individuals in Sri Lanka.

The number consists of 9 digits with no special formatting.


>>> compact('123456789')
'123456789'
>>> validate('123456789')
'123456789'
>>> format('123456789')
'123456789'
>>> validate('000000000')
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidComponent: All-zero TIN is not valid
"""

from stdnum.exceptions import *
from stdnum.util import clean, isdigits


__all__ = ['compact', 'validate', 'is_valid', 'format']


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, '').strip()


def validate(number):
    """Check if the number is a valid Sri Lankan personal TIN. This checks the length
    and ensures it contains only digits."""
    number = compact(number)
    if len(number) != 9:
        raise InvalidLength()
    if not isdigits(number):
        raise InvalidFormat()
    if number == '000000000':
        raise InvalidComponent('All-zero TIN is not valid')
    return number


def is_valid(number):
    """Check whether the number is valid."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Reformat the number to the standard presentation format."""
    number = compact(number)
    return number
