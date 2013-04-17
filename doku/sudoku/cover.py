import csv

import doku.dlx as dlx
import utils


class ExactCoverTable(object):

    rules = 4

    def __init__(self, size):
        """ Sudoku has 4 rules:
        - Each intersection of a row and column must contain exactly one number
        - Each row must contain each number exactly once
        - Each column must contain each number exactly once
        - Each box must contain each number exactly once

        This table tracks all constraints as columns and all possible
        solutions as rows.

        """
        self.size = size
        self.box_size = utils.box_size(size)

        # Each sudoku rule has size*size choices.
        self.choices = size * size

        # Combine the choices for each rule to find the total number of
        # constraints
        self.constraints = self.rules * self.choices

        self.width = self.constraints
        self.height = self.size * self.size * self.size

        # Get the column offsets for each rule constraint set
        self.offset = [i * self.choices for i in xrange(self.rules)]

    def __iter__(self):
        for solution in self.isolutions:
            index = self.solution_index(solution)
            columns = self.solution_columns(solution)
            for column in columns:
                yield (index, column)

    @property
    def isolutions(self):
        for row in xrange(self.size):
            for column in xrange(self.size):
                for number in xrange(self.size):
                    yield (row, column, number)

    def solution_index(self, solution):
        row_index, column_index, number_index = solution
        index = row_index * self.size * self.size
        index += column_index * self.size
        return index + number_index

    def solution_columns(self, solution):
        row_index, column_index, number_index = solution

        # What cell are we in?
        cell = self.size * row_index + column_index

        # What row are we in? (offset for cell indexes)
        row = self.size * row_index + number_index
        row += self.choices

        # What column are we in? (offset for cell and row indexes)
        column = self.size * column_index + number_index
        column += 2 * self.choices

        # What box are we in?
        box_row = int(row_index / self.box_size)
        box_column = int(column_index / self.box_size)
        box = (box_row * self.box_size) + box_column
        box = box * self.size + number_index

        # Account for previous cell, row and column indexes
        box += 3 * self.choices

        return (cell, row, column, box)

    def row(self, solution):
        (cell, row, column, box) = self.solution_columns(solution)

        r = [None] * self.width
        r[cell] = 1
        r[row] = 1
        r[column] = 1
        r[box] = 1
        return r

    def write_csv(self, filename):
        header = ["(R,C,N)"]
        cells = []
        rows = []
        columns = []
        boxes = []

        for i in xrange(self.size):
            for j in xrange(self.size):
                cells.append('R%sC%s' % (i + 1, j + 1))
                rows.append('R%sN%s' % (i + 1, j + 1))
                columns.append('C%sN%s' % (i + 1, j + 1))
                boxes.append('B%sN%s' % (i + 1, j + 1))

        header.extend(cells)
        header.extend(rows)
        header.extend(columns)
        header.extend(boxes)

        with open(filename, 'wb+') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)

            for solution in self.isolutions:
                label = '(%s,%s,%s)'
                label %= (solution[0] + 1, solution[1] + 1, solution[2] + 1)
                row = self.row(solution)
                row.insert(0, label)
                writer.writerow(row)


class Solver(dlx.Matrix):

    def __init__(self, size, known=None):
        self.known = known
        super(Solver, self).__init__(ExactCoverTable(size))

    def build(self, table):
        """ This is an optimized version of the dlx Matrix implementation.
        It is optimized because the empty cells are not iterated over. The
        filled nodes are the only nodes in the matrix touched.
        """
        self.table = table
        self.solutions = None
        self.root = dlx.ColumnNode('root')

        node = None
        columns = {}

        for i in xrange(table.width):
            name = 'c%s' % (i + 1)
            column = dlx.ColumnNode(name)
            if node:
                node.addRight(column)
            columns[i] = column
            node = column

        node = None
        for i, solution in enumerate(table.isolutions):
            column_indexes = table.solution_columns(solution)

            for j in column_indexes:
                name = int('%s%s' % (i + 1, j + 1))
                column = columns[j]
                cell = dlx.Node(name=name, column=column)
                cell.row_index = i
                cell.column_index = j
                cell.solution = solution
                column.addAbove(cell)
                if not node or node.row_index != cell.row_index:
                    node = cell
                else:
                    node.addLeft(cell)

        if self.known:
            for solution in self.known:
                column = self.table.solution_columns(solution)[0]
                self.hide(columns[column])
