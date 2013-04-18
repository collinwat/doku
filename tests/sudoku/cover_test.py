from __future__ import with_statement
import unittest

from doku.sudoku.cover import DLXSolver
from doku.sudoku.parse import StringParser


class SudokuDLXSolverTestCase(unittest.TestCase):
    def test_solver_4(self):
        parser = StringParser(4)
        known = parser.parse('.3...1....4...3.')
        solution = parser.parse('2314412332411432')
        solver = DLXSolver(4, known=known)
        solutions = solver.solve()

        assert len(solutions) == 1
        assert len(solutions[0]) == 16

        for i, cell in enumerate(solutions[0]):
            self.assertEqual(solution[i], cell)

    def test_solver_9(self):
        parser = StringParser(9)

        known = parser.parse('.........'
                             '.....3.85'
                             '..1.2....'
                             '...5.7...'
                             '..4...1..'
                             '.9.......'
                             '5......73'
                             '..2.1....'
                             '....4...9')

        solution = parser.parse('987654321'
                                '246173985'
                                '351928746'
                                '128537694'
                                '634892157'
                                '795461832'
                                '519286473'
                                '472319568'
                                '863745219')

        solver = DLXSolver(9, known=known)
        solutions = solver.solve()

        assert len(solutions) == 1
        assert len(solutions[0]) == 81

        for i, cell in enumerate(solutions[0]):
            self.assertEqual(solution[i], cell)
