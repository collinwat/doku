from __future__ import with_statement
import unittest
from pytest import raises

from doku.sudoku.parse import StringParser


class StringParserTestCase(unittest.TestCase):

    def test_invalid_small_size(self):
        with raises(ValueError):
            StringParser(0)

    def test_non_perfect_square_size(self):
        with raises(ValueError):
            StringParser(6)

    def test_invalid_large_size(self):
        with raises(ValueError):
            StringParser(36)

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

    def test_parse(self):
        parser = StringParser(4)
        results = parser.parse('2..1....4.1.31.2')

        assert len(results) == 7
        self.assertEqual(results[0], (0, 0, 1))
        self.assertEqual(results[1], (0, 3, 0))
        self.assertEqual(results[2], (2, 0, 3))
        self.assertEqual(results[3], (2, 2, 0))
        self.assertEqual(results[4], (3, 0, 2))
        self.assertEqual(results[5], (3, 1, 0))
        self.assertEqual(results[6], (3, 3, 1))

    def test_parse_limit(self):
        parser = StringParser(4)
        results = parser.parse('2..1....4.1.31.2.....1')
        assert len(results) == 7

    def test_parse_invalid(self):
        parser = StringParser(9)
        with raises(ValueError):
            parser.parse(None)
        with raises(ValueError):
            parser.parse('')
        with raises(ValueError):
            parser.parse('2..1')

    def test_parse_2d(self):
        parser = StringParser(4)
        results = parser.parse('\n'.join(["+-----+-----+",
                                          "| . 3 | . . |",
                                          "| . 1 | . . |",
                                          "+-----+-----+",
                                          "| . . | 4 . |",
                                          "| . . | 3 . |",
                                          "+-----+-----+"]))

        assert len(results) == 4
        self.assertEqual(results[0], (0, 1, 2))
        self.assertEqual(results[1], (1, 1, 0))
        self.assertEqual(results[2], (2, 2, 3))
        self.assertEqual(results[3], (3, 2, 2))

    def test_parse_invalid_2d(self):
        parser = StringParser(4)
        with raises(ValueError):
            parser.parse('\n'.join(["+-----+-----+",
                                    "|   3 |     |",
                                    "|   1 |     |",
                                    "+-----+-----+",
                                    "|     | 4   |",
                                    "|     | 3   |",
                                    "+-----+-----+"]))

    def test_parse_16(self):
        parser = StringParser(16)
        results = '\n'.join([
            "+-------------+-------------+-------------+-------------+",
            "| 13 .  .  10 | .  7  .  12 | 2  6  .  1  | .  .  .  .  |",
            "| 14 .  3  11 | .  .  .  12 | .  5  13 10 | 9  .  4  16 |",
            "| 6  15 7  12 | .  5  10 11 | .  .  .  16 | 3  .  .  14 |",
            "| .  11 8  .  | 14 4  .  .  | .  .  3  .  | .  16 .  7  |",
            "+-------------+-------------+-------------+-------------+",
            "| 10 .  5  6  | 13 16 11 .  | .  12 9  .  | 14 .  .  .  |",
            "| .  3  6  .  | 2  9  15 10 | .  11 .  .  | .  .  .  13 |",
            "| .  .  1  2  | .  6  .  7  | 4  .  .  11 | .  .  16 .  |",
            "| 4  .  .  .  | .  .  16 6  | 14 7  .  .  | 11 .  15 5  |",
            "+-------------+-------------+-------------+-------------+",
            "| 1  5  .  16 | .  .  9  2  | 3  14 .  .  | .  .  .  4  |",
            "| .  6  .  .  | 5  .  .  15 | 8  .  1  .  | 7  2  .  .  |",
            "| 12 .  .  .  | .  .  5  .  | 15 10 4  3  | .  7  13 .  |",
            "| .  .  .  4  | .  12 13 .  | .  9  15 6  | 8  1  .  10 |",
            "+-------------+-------------+-------------+-------------+",
            "| 11 .  12 .  | .  2  .  .  | .  .  5  15 | .  4  10 .  |",
            "| 9  .  .  15 | 16 .  .  .  | 10 3  14 .  | 6  5  8  12 |",
            "| 3  7  .  5  | 6  8  4  .  | 16 .  .  .  | 13 12 .  1  |",
            "| .  .  .  13 | .  10 2  5  | .  6  .  12 | .  .  11 .  |",
            "+-------------+-------------+-------------+-------------+"
        ])
        results = parser.parse(results)
        assert results
        assert len(results) == 132
