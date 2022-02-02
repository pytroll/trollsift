#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2014-2022 trollsift developers
#
# Author(s):
#
# Panu Lahtinen <panu.lahtinen@fmi.fi>
# Hróbjartur Thorsteinsson <hroi@vedur.is>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
"""Setup for trollsift."""
from setuptools import setup
import versioneer

version = versioneer.get_version()
README = open('README.rst', 'r').read()

setup(name="trollsift",
      version=version,
      cmdclass=versioneer.get_cmdclass(),
      description='String parser/formatter',
      long_description=README,
      long_description_content_type='text/x-rst',
      author='The Pytroll Team',
      author_email='pytroll@googlegroups.com',
      classifiers=["Development Status :: 5 - Production/Stable",
                   "Intended Audience :: Science/Research",
                   "License :: OSI Approved :: GNU General Public License v3 " +
                   "or later (GPLv3+)",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python",
                   "Topic :: Scientific/Engineering"],
      url="https://github.com/pytroll/trollsift",
      download_url="https://github.com/pytroll/trollsift/tarball/v" + version,
      packages=['trollsift'],
      keywords=["string parsing", "string formatting", "pytroll"],
      zip_safe=False,
      python_requires='>=3.6',
      install_requires=[],
      tests_require=['pytest']
      )
