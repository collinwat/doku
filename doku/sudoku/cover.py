import csv
import utils


class ExactCoverTable(object):

    rules = 4

    def __init__(self, size):
        """ Sudoku has 4 rules:
        - Each intersection of a row and column must contain exactly one number
        - Each row must contain each number exactly once
        - Each column must contain each number exactly once
        - Each box must contain each number exactly once
        """
        self.size = size
        self.box_size = utils.box_size(size)

        # Each sudoku rule has size*size choices.
        self.choices = size * size

        # Combine the choices for each rule to find the total number of
        # constraints
        self.constraints = self.rules * self.choices

        # Get the column offsets for each rule constraint set
        self.offset = [i * self.choices for i in xrange(self.rules)]

    def __iter__(self):
        for row in xrange(self.size):
            for column in xrange(self.size):
                for number in xrange(self.size):
                    possibility = (row + 1, column + 1, number + 1)
                    yield possibility, self.row(row, column, number)

    def row(self, row_index, column_index, number_index):
        # What cell are we in?
        cell = self.size * row_index + column_index

        # What row are we in? (offset for cell indexes)
        row = self.size * row_index + number_index
        row += self.offset[1]

        # What column are we in? (offset for cell and row indexes)
        column = self.size * column_index + number_index
        column += self.offset[2]

        # What box are we in?
        box_row = int(row_index / self.box_size)
        box_column = int(column_index / self.box_size)
        box = (box_row * self.box_size) + box_column
        box = box * self.size + number_index

        # Account for previous cell, row and column indexes
        box += self.offset[3]

        r = [None] * self.constraints
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
            for (possibility, row) in self:
                row.insert(0, '(%s,%s,%s)' % possibility)
                writer.writerow(row)
