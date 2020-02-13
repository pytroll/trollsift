#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2014-2020 Martin Raspaud
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""Parser regression tests."""

import unittest
import datetime as dt

from trollsift.parser import parse


class TestParser(unittest.TestCase):

    def test_002(self):
        res = parse('hrpt16_{satellite:7s}_{start_time:%d-%b-%Y_%H:%M:%S.000}_{orbit_number:5d}',
                    "hrpt16_NOAA-19_26-NOV-2014_10:12:00.000_29889")
        self.assertEqual(res, {'orbit_number': 29889,
                               'satellite': 'NOAA-19',
                               'start_time': dt.datetime(2014, 11, 26, 10, 12)})
