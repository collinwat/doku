import unittest
from sudoku import StringParser


class StringParserTestCase(unittest.TestCase):

    def test_invalid_small_size(self):
        assert StringParser(0)
