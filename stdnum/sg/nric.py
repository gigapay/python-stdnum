import re

from stdnum.exceptions import (
    InvalidChecksum,
    InvalidFormat,
    InvalidLength,
    ValidationError,
)

# Define the checksum tables for the first character of the NRIC
CHECKSUM_TABLES = {
    "ST": ["J", "Z", "I", "H", "G", "F", "E", "D", "C", "B", "A"],
    "FG": ["X", "W", "U", "T", "R", "Q", "P", "N", "M", "L", "K"],
    "M": ["K", "L", "J", "N", "P", "Q", "R", "T", "U", "W", "X"],
}


def is_valid_format(nric):
    """
    Validate the format of the NRIC.
    """
    return bool(re.match(r"^[STFGM]\d{7}[A-Z]$", nric))


def calculate_checksum(number):
    """
    Calculate the checksum for a given NRIC first character and digit string.

    Source: https://github.com/samliew/singapore-nric
    """
    firstchar = number[0]
    weights = [2, 7, 6, 5, 4, 3, 2]
    digits = list(map(int, number[1:]))
    weighted_sum = sum(w * d for w, d in zip(weights, digits))

    offset = 4 if firstchar in "TG" else (3 if firstchar == "M" else 0)
    index = (offset + weighted_sum) % 11
    if firstchar == "M":
        index = 10 - index

    for key in CHECKSUM_TABLES:
        if firstchar in key:
            return CHECKSUM_TABLES[key][index]

    raise ValidationError(f"Unable to find checksum table for '{firstchar}'")


def validate(number):
    """
    Validate a single NRIC.
    """
    if len(number) != 9:
        raise InvalidLength()
    elif not is_valid_format(number):
        raise InvalidFormat()
    if not number[-1] == calculate_checksum(number[:-1]):
        raise InvalidChecksum()
    return number


def is_valid(number):
    """Check if the number is a valid Singapore NRIC number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False
