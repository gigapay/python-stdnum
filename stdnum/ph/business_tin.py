# business_tin.py - functions for handling Philippine Business Nombor ChukaiPendapatan (Business Tax ID Number)
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

"""Business NCP (Philippines Business Tax Identification Number).

The Business Tax Identification Number (TIN), also known as Nombor ChukaiPendapatan,
is a unique identifier issued by the Bureau of Internal Revenue (BIR) to
businesses in the Philippines.

The number consists of 12 digits in the format XXX-XXX-XXX-XXX where the first
9 digits are the base number and the last 3 digits are branch codes. For businesses,
the last three digits cannot be 000 (which is reserved for individuals).

More information:

* https://www.bir.gov.ph/primary-registration

>>> compact('123456789001')
'123456789001'
>>> validate('123456789001')
'123456789001'
>>> validate('123456789000')
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidComponent: Business TIN should not end with 000
>>> format('123456789001')
'123-456-789-001'
"""

from stdnum.exceptions import *
from stdnum.util import clean, isdigits


__all__ = ['compact', 'validate', 'is_valid', 'format']


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, '').strip()  # separators are not allowed


def validate(number):
    """Check if the number is a valid Philippines business TIN. This checks the length,
    formatting and digits."""
    number = compact(number)
    if len(number) != 12:
        raise InvalidLength()
    if not isdigits(number):
        raise InvalidFormat()
    if number[9:12] == '000':
        raise InvalidComponent('Business TIN should not end with 000')
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
    return '-'.join((number[0:3], number[3:6], number[6:9], number[9:12]))
