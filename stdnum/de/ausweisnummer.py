# ausweisnummer.py - functions for handling German ID card numbers
# coding: utf-8
#
# Copyright (C) 2025
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

"""Ausweisnummer (German ID card number).

The Ausweisnummer is the identifier on German ID cards and passports.
For ID cards valid since November 2010, it consists of 9 characters
(alphanumeric) followed by a check digit. For older ID cards and passports
the formats differ.

The check digit is calculated using a weighted sum (7,3,1 pattern) of the
first 9 characters, with letters converted to numbers (A→10, B→11, ..., Z→35).

More information:

* https://de.wikipedia.org/wiki/Ausweisnummer

>>> validate('T22000129')
'T22000129'
>>> validate('T220001293')
'T220001293'
>>> validate('T220001294')
Traceback (most recent call last):
    ...
InvalidChecksum: ...
>>> validate('1220001297')
'1220001297'
>>> validate('1220001298')
Traceback (most recent call last):
    ...
InvalidChecksum: ...
>>> format('T220001293')
'T22000129-3'
"""

from stdnum.exceptions import InvalidChecksum, InvalidFormat, InvalidLength, ValidationError
from stdnum.util import clean


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, ' -').strip().upper()


def calc_check_digit(number):
    """Calculate the check digit for the number.
    
    The algorithm multiplies each character with weight 7, 3, or 1 in succession.
    For letters: A=10, B=11, ..., Z=35.
    Then the last digits of the products are summed, and the check digit is the last
    digit of that sum.
    """
    # Convert letters to numbers according to the scheme A→10, B→11, …, Z→35
    values = []
    weights = [7, 3, 1]  # Weights for the algorithm
    
    for i, char in enumerate(number):
        if char.isdigit():
            value = int(char)
        else:
            value = ord(char) - ord('A') + 10
        
        # Apply the weight (7,3,1) to each digit
        weight = weights[i % 3]
        # We only take the last digit of each product
        values.append((value * weight) % 10)
    
    # Sum the last digits of the products
    return str(sum(values) % 10)


def validate(number):
    """Check if the number provided is a valid ID card number.
    This checks the length, formatting and check digit."""
    number = compact(number)
    
    # Check if it's the new format (10 characters, including check digit)
    if len(number) == 10:
        # The new format has 9 alphanumeric characters + 1 check digit
        if not number[:9].isalnum():
            raise InvalidFormat()
        
        if not number[9].isdigit():
            raise InvalidFormat()
            
        # Verify the check digit
        if calc_check_digit(number[:9]) != number[9]:
            raise InvalidChecksum()
        
        return number
    
    # If it's 9 characters, assume it's without check digit
    elif len(number) == 9:
        if not number.isalnum():
            raise InvalidFormat()
        
        # Just validate the format without verifying check digit
        return number
    
    else:
        raise InvalidLength()


def is_valid(number):
    """Check if the number provided is a valid ID card number.
    This checks the length, formatting and check digit."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Reformat the number to the standard presentation format."""
    number = compact(number)
    
    if len(number) == 10:
        # Format with a hyphen before the check digit
        return '%s-%s' % (number[:9], number[9])
    else:
        # Return as is if no check digit
        return number
