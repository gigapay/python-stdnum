# __init__.py - collection of Swedish numbers
# coding: utf-8
#
# Copyright (C) 2012 Arthur de Jong
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

"""Collection of Swedish numbers."""

# provide aliases
from stdnum.se import personnummer as personalid  # noqa: F401
from stdnum.se import postnummer as postal_code  # noqa: F401
from stdnum.se import orgnr as businessid  # noqa: F401
from stdnum.se import personnummer as personal_tin  # noqa: F401
