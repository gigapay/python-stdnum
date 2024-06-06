# itn.py - functions for handling Malaysian ITN numbers
# coding: utf-8
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

"""ITN (Income Tax Number, Malaysian TIN number).

The Malaysian ITN is defined for both individuals and non-individuals.

The Inland Revenue Board of Malaysia (IRBM) assigns a unique number to persons registered
with the Board. This unique number is known as “Nombor Cukai Pendapatan” or Income Tax
Number (ITN). This number is issued to persons who are required to report their income for
assessment to the Director General of Inland Revenue.

The ITN is unique to a person and is not assigned to another person. Individuals are not
automatically issued with TIN. TIN is only issued either on request, on registration exercise by
the tax authority or on employment when their employer request for their registration.
The ITN consist of maximum twelve or thirteen alphanumeric characters with a combination of
the Type of File Number and the Income Tax Number.

Read more: https://phl.hasil.gov.my/pdf/pdfam/MALAYSIA_TIN_NUMBER_AND_TIN_REGISTRATION_02122020.pdf

>>> validate('SG 10234567090')
'SG10234567090'
>>> validate('C 2584563202')
'C2584563202'
>>> validate('SG 1234')
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidLength: The number has an invalid length.
>>> validate('XX 1234567890')
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidFormat: The number has an invalid format.
"""

import re
from stdnum.exceptions import InvalidLength, InvalidFormat, ValidationError
from stdnum.util import clean

# Regular expressions for matching individual and non-individual ITN formats
_individual_itn_re = re.compile(r'^(SG|OG)\s?\d{10,11}[01]$')
_non_individual_itn_re = re.compile(r'^(C|CS|D|E|F|FA|PT|TA|TC|TN|TR|TP|TJ|LE)\s?\d{9,10}$')


def compact(number):
    """Convert the ITN number to the minimal representation. This strips the number of any
    valid separators and removes surrounding whitespace."""
    number = clean(number, ' ').upper().strip()
    return number


def validate(number):
    """Check if the number is a valid Malaysian ITN number. This checks the length
    and formatting."""
    number = compact(number)

    if _individual_itn_re.match(number) or _non_individual_itn_re.match(number):
        return number
    else:
        if not (10 <= len(number) <= 13):
            raise InvalidLength()
        raise InvalidFormat()


def is_valid(number):
    """Check if the number is a valid Malaysian ITN number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False
