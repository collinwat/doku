from __future__ import with_statement
import unittest
from pytest import raises

from doku.sudoku import StringParser


class StringParserTestCase(unittest.TestCase):

    def test_invalid_small_size(self):
        with raises(ValueError):
            StringParser(0)
