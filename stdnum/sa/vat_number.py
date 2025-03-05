# vat_number.py - functions for handling Saudi Arabian VAT numbers
# coding: utf-8
#
# Copyright (C) 2016 Luciano Rossi
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

"""VAT (Kingdom of Saudi Arabia Value Added Tax number).

The Saudi Arabian VAT number is a 15-digit number used for Value Added Tax
purposes in Saudi Arabia. It incorporates the 10-digit Tax Identification
Number (TIN) and adds 5 more digits with specific meanings.

The structure is as follows:
- First digit: GCC member state code (3 for Saudi Arabia)
- Next 8 digits: Base serial number
- Next 1 digit: Check digit (completes the 10-digit TIN)
- Next 3 digits: Branch/establishment identifier (000 for headquarters, 
  001, 002, etc. for branches)
- Last 2 digits: Tax type identifier (01 for VAT)

More information:
* https://zatca.gov.sa/en/eServices/Pages/TaxpayerLookup.aspx

>>> validate('300270769210001')
'300270769210001'
>>> validate('3002707692100')  # too short
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidLength: The number has an invalid length.
>>> validate('300270769X10001')  # invalid character
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidFormat: The number has an invalid format.
>>> is_valid('300270769210001')
True
>>> is_valid('400270769210001')  # should start with 3 for Saudi Arabia
False
>>> format('300270769210001')
'3 00270769 2 100 01'
"""

from stdnum.exceptions import InvalidLength, InvalidFormat, ValidationError
from stdnum.util import clean, isdigits


def compact(number):
    """Convert the number to the minimal representation.
    
    This strips the number of any valid separators and removes
    surrounding whitespace.
    """
    return clean(number, ' -').strip()


def validate(number):
    """Check if the number is a valid Saudi Arabian VAT number.
    
    This checks the length, format, and basic country code.
    """
    number = compact(number)
    if len(number) != 15:
        raise InvalidLength()
    if not isdigits(number):
        raise InvalidFormat()
    # First digit should be 3 for Saudi Arabia
    if number[0] != '3':
        raise InvalidFormat('First digit should be 3 for Saudi Arabia')
    # Last two digits should be 01 for VAT
    if number[-2:] != '01':
        raise InvalidFormat('Last two digits should be 01 for VAT')
    return number


def is_valid(number):
    """Check if the number is a valid Saudi Arabian VAT number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Format the number in the standard format.
    
    For a VAT number this would be: 3 00270769 2 100 01
    (Country code, serial, check digit, branch, tax type)
    """
    number = compact(number)
    if len(number) != 15:
        raise InvalidLength()
    return ' '.join([
        number[0],       # Country code (3)
        number[1:9],     # Base serial
        number[9:10],    # Check digit
        number[10:13],   # Branch identifier
        number[13:15],   # Tax type
    ])
