from __future__ import with_statement
import unittest
from pytest import raises

from doku.sudoku.parse import (StringParser,
                               UnknownCharacterError,
                               IncompleteError)


class StringParserTestCase(unittest.TestCase):

    def test_invalid_small_size(self):
        with raises(ValueError):
            StringParser(0)

    def test_non_perfect_square_size(self):
        with raises(ValueError):
            StringParser(6)

    def test_invalid_large_size(self):
        with raises(ValueError):
            StringParser(16)

    def test_size_4(self):
        parser = StringParser(4)
        assert parser.size == 4
        assert parser.length == 16
        assert parser.box_size == 2

    def test_size_9(self):
        parser = StringParser(9)
        assert parser.size == 9
        assert parser.length == 81
        assert parser.box_size == 3

    def test_parse_int(self):
        parser = StringParser(4)
        assert parser.parse_int('1') == 1
        assert parser.parse_int('0') == 0
        assert parser.parse_int('') is None
        assert parser.parse_int(None) is None
        assert parser.parse_int('.') is None
        assert parser.parse_int('a') is None

    def test_parse_char(self):
        parser = StringParser(4)
        assert parser.parse_char('1') == 1
        assert parser.parse_char('.') is None
        with raises(UnknownCharacterError):
            parser.parse_char('')
        with raises(UnknownCharacterError):
            parser.parse_char('0')
        with raises(UnknownCharacterError):
            parser.parse_char('10')
        with raises(UnknownCharacterError):
            parser.parse_char('a')
        with raises(UnknownCharacterError):
            parser.parse_char(None)

    def test_iparse(self):
        parser = StringParser(4)
        parser = parser.iparse('2..1....4.1.31.2')
        self.assertEqual(parser.next(), (0, 0, 1))
        self.assertEqual(parser.next(), (0, 3, 0))
        self.assertEqual(parser.next(), (2, 0, 3))
        self.assertEqual(parser.next(), (2, 2, 0))
        self.assertEqual(parser.next(), (3, 0, 2))
        self.assertEqual(parser.next(), (3, 1, 0))
        self.assertEqual(parser.next(), (3, 3, 1))
        with raises(StopIteration):
            parser.next()

    def test_iparse_limit(self):
        parser = StringParser(4)
        parser = parser.iparse('2..1....4.1.31.2.....1')
        [parser.next() for i in xrange(7)]
        with raises(StopIteration):
            parser.next()

    def test_iparse_invalid(self):
        parser = StringParser(9)
        with raises(IncompleteError):
            parser.iparse(None).next()
        with raises(IncompleteError):
            parser.iparse('').next()
        with raises(IncompleteError):
            parser.iparse('2..1....4.1.31.2').next()
