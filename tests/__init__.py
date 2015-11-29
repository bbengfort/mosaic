# tests
# Testing for the Mosaic file system usage analysis utility
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Fri Nov 27 12:56:50 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: __init__.py [] benjamin@bengfort.com $

"""
Testing for the Mosaic file system usage analysis utility
"""

##########################################################################
## Imports
##########################################################################

import unittest

##########################################################################
## Module Constants
##########################################################################

TEST_VERSION = "0.2.1" ## Also the expected version onf the package

##########################################################################
## Test Cases
##########################################################################

class InitializationTest(unittest.TestCase):

    def test_initialization(self):
        """
        Tests a simple world fact by asserting that 10**2 is 100.
        """
        self.assertEqual(10**2, 100)

    def test_import(self):
        """
        Can import mosaic
        """
        try:
            import mosaic
        except ImportError:
            self.fail("Unable to import the mosaic module!")

    def test_version(self):
        """
        Assert that the version is sane
        """
        import mosaic
        self.assertEqual(TEST_VERSION, mosaic.__version__)
