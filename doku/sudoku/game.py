class Game(object):

    def __init__(self, grid):
        self.grid = grid

    @property
    def irows(self):
        for i in xrange(9):
            yield self.row(i)

    @property
    def icolumns(self):
        for i in xrange(9):
            yield self.column(i)

    @property
    def ilines(self):
        for i, row in enumerate(self.irows):
            yield ' | '.join([
                ' '.join('%s' % v for v in row[0:3]),
                ' '.join('%s' % v for v in row[3:6]),
                ' '.join('%s' % v for v in row[6:9])
            ])

            if i == 2 or i == 5:
                yield '------+-------+-------'

    @property
    def text(self):
        return '\n'.join(self.ilines)

    def row(self, index):
        return self.grid[9 * index:9 * (index + 1)]

    def column(self, index):
        return [self.grid[index + 9 * i] for i in range(9)]
