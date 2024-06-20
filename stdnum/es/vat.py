"""
Handles mutiple version of VAT, one for foreigners (NIE) and one for citizens (CIF)
"""

from stdnum.es import cif, nie


def is_valid(number):
    """Check if the number provided is a valid DNI number. This checks the
    length, formatting and check digit."""
    return cif.is_valid(number) or nie.is_valid(number)


