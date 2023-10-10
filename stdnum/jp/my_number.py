# my_number.py - functions for handling Japanese identity Number
# coding: utf-8
#
# Copyright (C) 2019 Alan Hettinger
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


from stdnum.exceptions import *
from stdnum.util import clean


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, "- ").strip()


def validate(number):
    """Check if the number is valid. This checks the length."""
    number = compact(number)
    if len(number) != 12:
        raise InvalidLength()
    return number


def is_valid(number):
    """Check if the number is a valid."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False
