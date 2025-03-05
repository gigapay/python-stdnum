# tin_number.py - functions for handling Saudi Arabian TIN numbers
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

"""TIN (Saudi Arabian Tax Identification Number).

The Saudi Arabian Tax Identification Number (TIN), often referred to as the "Unique Number" 
(الرقم المميز) is issued by ZATCA (Zakat, Tax and Customs Authority) to 
taxpayer entities for tax and zakat purposes.

The number consists of 10 digits:
- First digit is 3 (indicating KSA's GCC country code)
- Next 8 digits are a serial identifier
- Last digit is a check digit

More information:
* https://web-archive.oecd.org/tax/automatic-exchange/crs-implementation-and-assistance/tax-identification-numbers/Saudi-Arabia-TIN.pdf
* https://zatca.gov.sa/

>>> validate('3002707692')
'3002707692'
>>> validate('1234567890')  # doctest: +IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
    ...
InvalidComponent: ...
>>> validate('300270769')  # doctest: +IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> format('300-270-7692')
'3002707692'
>>> is_valid('3002707692') 
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
    """Check if the number is a valid Saudi Arabian TIN number.
    
    This checks the length, first digit (must be 3 for KSA), and that
    all characters are digits.
    """
    number = compact(number)
    if len(number) != 10:
        raise InvalidLength()
    if not isdigits(number):
        raise InvalidComponent()
    if number[0] != '3':
        raise InvalidComponent()
    # Note: We would implement a check digit validation here if the specific
    # algorithm was known. Currently, it's known that the last digit is a check
    # digit, but the exact calculation method is not documented publicly.
    return number


def is_valid(number):
    """Check if the number is a valid Saudi Arabian TIN number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Format the number to the standard representation."""
    return compact(number)
