# tests.path_tests
# Testing for the path object wrapper that does most of the analysis.
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Fri Nov 27 14:15:20 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: path_tests.py [] benjamin@bengfort.com $

"""
Testing for the path object wrapper that does most of the analysis.
"""

##########################################################################
## Imports
##########################################################################

import os
import unittest

from mosaic.path import Path
from itertools import permutations

##########################################################################
## Path TestCase
##########################################################################


class PathTests(unittest.TestCase):
    """
    Tests for the path object -- performs most of the work, so important!
    """

    def test_initialization(self):
        """
        Test that the path string is expanded correctly
        """

        os.environ.setdefault('BOB', '/home/bob')
        homedir = os.path.expanduser('~')

        self.assertEqual(str(Path('$BOB/projects')), '/home/bob/projects')
        self.assertEqual(str(Path('~/projects')), '{}/projects'.format(homedir))

    def test_add(self):
        """
        Test adding two paths together
        """
        paths = (
            "projects/fixtures",
            "/home/bob/",
            "/home/bob/projects",
            "test.json",
        )

        paths = zip(map(os.path.normpath, paths), map(Path, paths))

        for ((pstr_a, pobj_a), (pstr_b, pobj_b)) in permutations(paths, r=2):
            self.assertEqual(pobj_a + pobj_b, os.path.join(pstr_a, pstr_b))

    def test_join(self):
        """
        Test joining two paths together
        """
        paths = (
            "projects/fixtures",
            "/home/bob/",
            "/home/bob/projects",
            "test.json",
        )

        paths = zip(map(os.path.normpath, paths), map(Path, paths))

        for ((pstr_a, pobj_a), (pstr_b, pobj_b)) in permutations(paths, r=2):
            self.assertEqual(pobj_a.join(pobj_b), os.path.join(pstr_a, pstr_b))

    def test_string_join(self):
        """
        Assert a string can be joined to a path.
        """
        self.assertEqual(
            Path('/home/bob/projects/').join('fixtures'),
            '/home/bob/projects/fixtures'
        )

    def test_multi_join(self):
        """
        Assert that multiple paths can be joined.
        """
        self.assertEqual(
            Path('/home/bob').join('fixtures', Path('project'), 'foo', Path('bar')),
            Path('/home/bob/fixtures/project/foo/bar')
        )

    def test_path_copy(self):
        """
        Assert a path can be copied from another path.
        """
        p1 = Path('project/fixtures/foo.txt')
        p2 = Path(p1)

        self.assertEqual(p1, p2)
        self.assertIsNot(p1, p2)

    def test_relative_depth(self):
        """
        Test the relative depth of two paths.
        """
        p1 = Path('project/fixtures')
        p2 = 'project/fixtures/data/testing/foo.txt'
        p3 = Path('data')

        self.assertEqual(p1.relative_depth(p2), 3)
        self.assertEqual(p1.relative_depth(p3), 1)

    def test_hidden(self):
        """
        Test hidden files/dirs checks
        """

        hidden = (
            '.ssh', '.passwd', '/home/bob/.ssh', '~$file.body', 'C:/Program Files/~tmp'
        )

        for fname in hidden:
            self.assertTrue(Path(fname).is_hidden(), '{} is not hidden?'.format(fname))

    def test_not_hidden(self):
        """
        Test visible files/dirs checks
        """

        visible = (
            'foo.txt', '~/bar/baz.txt', '.ssh/authorized_keys'
        )

        for fname in visible:
            self.assertFalse(Path(fname).is_hidden(), '{} is hidden?'.format(fname))
