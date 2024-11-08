# itan.py - functions for handling Mauritian Tax Account Numbers
# coding: utf-8
#
# Copyright (C) 2018 Arthur de Jong
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

"""Tax Account Number (Mauritian tax account number for individuals).

The Mauritian tax account number is a unique 8 digit numeric identifier

The Mauritius Revenue Authority (MRA) issues a Tax Account Number
to all individuals with a tax obligation in Mauritius. The TAN is given at the time of the
registration of the individual in the databases of the MRA.

The number consists of 8 digits:
the first digit is always a 1, 5, 7, or 9

More information:
https://www.oecd.org/content/dam/oecd/en/topics/policy-issue-focus/aeoi/mauritius-tin.pdf
"""

import datetime
import re

from stdnum.exceptions import *
from stdnum.util import clean

_tan_re = re.compile('^[1578][0-9]{7}$')


def compact(number):
    """Convert the number to the minimal representation. This strips
    surrounding whitespace and separation dash."""
    return clean(number, ' ').upper().strip()


def validate(number):
    """Check if the number is a valid ID number."""
    number = compact(number)
    if len(number) != 8:
        raise InvalidLength()
    if not _tan_re.match(number):
        raise InvalidFormat()
    return number


def is_valid(number):
    """Check if the number provided is a valid RFC."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False
