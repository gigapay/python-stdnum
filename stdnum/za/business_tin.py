# business_tin.py - functions for handling South African Business Registration Numbers

"""Business TIN (South African Business Registration Number).

The South African Business Registration Number is a unique identifier 
issued to businesses in South Africa by the Companies and Intellectual 
Property Commission (CIPC), formerly known as CIPRO.

The number consists of 14 characters in the format YYYY/NNNNNN/NN:
- YYYY: The year of incorporation (4 digits)
- NNNNNN: A unique sequential 6-digit number assigned in that year
- NN: A numeric code indicating the type of business, 07 for private and 06 for public

More information:
* https://images.investgo.cn/law/7fe0790e-1773-4736-8d6a-5a59fbc97270.pdf

>>> compact('2000/000001/07')
'200000000107'
>>> validate('2000/000001/07')
'200000000107'
>>> format('200000000107')
'2000/000001/07'
>>> validate('2000/000001/08')
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidComponent: Entity type must be 07 or 06
>>> validate('2000/00001/07')
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidLength: The number has an invalid length.
>>> validate('199/000001/07')
Traceback (most recent call last):
    ...
stdnum.exceptions.InvalidLength: The number has an invalid length.
"""

from stdnum.exceptions import *
from stdnum.util import clean, isdigits
import datetime


__all__ = ['compact', 'validate', 'is_valid', 'format']


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, '/').strip()


def validate(number):
    """Check if the number is a valid South African business registration number.
    This checks the format, length, and components."""
    number = compact(number)
    
    if len(number) != 12:
        raise InvalidLength()
    if not isdigits(number):
        raise InvalidFormat()
    
    year = number[:4]
    entity_type = number[-2:]

    current_year = datetime.datetime.now().year
    if int(year) < 1900 or int(year) > current_year:
        raise InvalidComponent(f"Year must be between 1900 and {current_year}")

    if entity_type != '07' and entity_type != '06':
        raise InvalidComponent("Entity type must be 07 or 06")

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
    
    year = number[:4]
    seq = number[4:-2]
    entity_type = number[-2:]

    return f"{year}/{seq}/{entity_type}"
