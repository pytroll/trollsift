#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2014, 2015

# Author(s):

# Panu Lahtinen <panu.lahtinen@fmi.fi>
# Hróbjartur Thorsteinsson <hroi@vedur.is>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Setup for trollsift.
"""
from setuptools import setup
import imp

version = imp.load_source('trollsift.version', 'trollsift/version.py')

setup(name="trollsift",
      version=version.__version__,
      description='String parser/formatter',
      author='Panu Lahtinen',
      author_email='panu.lahtinen@fmi.fi',
      classifiers=["Development Status :: 3 - Alpha",
                   "Intended Audience :: Science/Research",
                   "License :: OSI Approved :: GNU General Public License v3 " +
                   "or later (GPLv3+)",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python",
                   "Topic :: Scientific/Engineering"],
      url="https://github.com/pnuu/trollsift",
      download_url="https://github.com/pnuu/trollsift/tarball/" + version.__version__,
      packages=['trollsift'],
      keywords=["string parsing", "string formatting", "pytroll"],
      zip_safe=False,
      install_requires=['six'],
      test_suite='trollsift.tests.suite',
      )
