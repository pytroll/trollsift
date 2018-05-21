#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from trollsift.tests import unittests, regressiontests, integrationtests

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest


def suite():
    """The global test suite.
    """
    mysuite = unittest.TestSuite()
    mysuite.addTests(unittests.suite())
    mysuite.addTests(regressiontests.suite())
    mysuite.addTests(integrationtests.suite())

    return mysuite


def load_tests(loader, tests, pattern):
    return suite()
