import cover
import parse
import utils


class Board(object):

    def __init__(self, board, size=None):
        board = board.strip()

        if size is None:
            size = utils.box_size(len(board))

        if not size:
            msg = 'Size not specified and board string is not a perfect square'
            raise ValueError(msg)

        self.size = size
        self.box_size = boxes = utils.box_size(self.size)
        self.hr = '+%s+' % '+'.join(['-' * (boxes * 2 + 1)] * boxes)
        self.parser = parse.StringParser(self.size)
        self.known = self.parser.parse(board)
        self.rebuild()

    @property
    def solutions(self):
        if not getattr(self, '_solutions', None):
            self._solutions = self.solver.solve()
        return self._solutions

    def rebuild(self):
        self.solver = cover.DLXSolver(self.size, known=self.known)
        self._solutions = None
        self.reset()

    def reset(self):
        self.guesses = set()
        self.grid = [[None] * self.size for i in xrange(self.size)]

        for known in self.known:
            self.grid[known[0]][known[1]] = known[2] + 1

    def guess(self, guess):
        row, column, number = guess

        if guess in self.known or \
           guess in self.guesses or \
           row < 0 or row >= self.size or \
           column < 0 or column >= self.size or \
           number < 0 or number >= self.size:
            return

        row = self.grid[row]
        old = row[column]
        row[column] = number + 1
        self.guesses.add(guess)

        if old:
            old = (guess[0], guess[1], old)
            if old in self.guesses:
                self.guesses.remove(old)

    @property
    def ilines(self):
        boxes = self.box_size
        for row_index, row in enumerate(self.grid):
            if row_index % self.box_size == 0:
                yield self.hr

            row = ['%s' % i if i else '.' for i in row]
            segments = []

            for i in xrange(boxes):
                cells = row[i * boxes:i * boxes + boxes]
                segments.append(' '.join(cells))

            yield '| %s |' % ' | '.join(segments)

            if row_index == len(self.grid) - 1:
                yield self.hr

    @property
    def lines(self):
        return list(self.ilines)

    @property
    def text(self):
        return '\n'.join(self.ilines)

    @property
    def line(self):
        return ''.join(['%s' % cell if cell else '.'
                       for row in self.grid
                       for cell in row])

    def solve(self, index=0):
        if len(self.solutions) < 1:
            return

        for solution in self.solutions[index]:
            self.guess(solution)
