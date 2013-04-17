from __future__ import with_statement
import unittest

from doku.sudoku.cover import Solver
from doku.sudoku.parse import StringParser


class SudokuSolverTestCase(unittest.TestCase):
    def test_solver(self):
        parser = StringParser(4)
        known = parser.parse('.3...1....4...3.')
        solution = '2314412332411432'
        solver = Solver(4, known=known)
        assert solution == solver.solve()
