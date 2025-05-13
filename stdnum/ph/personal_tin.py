# personal_tin.py - functions for handling Philippine Personal Nombor ChukaiPendapatan (Personal Tax ID Number)
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

"""Personal NCP (Philippines Personal Tax Identification Number).

The Personal Tax Identification Number (TIN), also known as Nombor ChukaiPendapatan, 
is a unique identifier issued by the Bureau of Internal Revenue (BIR) to 
individuals in the Philippines.

The number consists of 12 digits in the format XXX-XXX-XXX-XXX where the first
9 digits are the base number and the last 3 digits are branch codes (000 for individuals).

More information:

* https://www.bir.gov.ph/primary-registration

>>> compact('123456789000')
'123456789000'
>>> validate('123456789000')
'123456789000'
>>> format('123456789000')
'123-456-789-000'
"""

from stdnum.exceptions import *
from stdnum.util import clean, isdigits


__all__ = ['compact', 'validate', 'is_valid', 'format']


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, '').strip() # separators are not allowed


def validate(number):
    """Check if the number is a valid Philippines personal TIN. This checks the length,
    formatting and digits."""
    number = compact(number)
    if len(number) != 12:
        raise InvalidLength()
    if not isdigits(number):
        raise InvalidFormat()
    if number[9:12] != '000':
        raise InvalidComponent('Personal TIN should end with 000')
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