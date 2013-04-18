import re
import doku.utils as utils


class StringParser(object):

    def __init__(self, size):
        """
        This parser expects that strings only contain numberic characters and
        '.' to represent an empty cell. It assumes that each character
        represents a cell.

        Here is a 4x4 example:
            2..1....4.1.31.2

        Due to these assumptions, the only acceptable sudoku perfect square
        sizes are 4 and 9, since they do not require a number larger than a
        single digit.
        """

        if size != 4 and size != 9 and size != 16:
            msg = 'The size "%s" is invalid. Size can only be 4, 9 or 16.'
            raise ValueError(msg, size)

        self.size = size
        self.length = size * size
        self.box_size = utils.box_size(size)
        if self.size < 10:
            self.pattern = re.compile('([1-%s]|\.)' % self.size)
        else:
            self.pattern = re.compile('([1-9]+|[\.]+)')

    def parse(self, text):
        matches = self.pattern.findall(text or '')

        if len(matches) < self.length:
            msg = 'Board parsing found %s cells but requires %s cells.'
            raise ValueError(msg % (len(matches), self.length))

        row = 0
        column = 0
        count = 0
        results = []

        for match in matches:
            number = self.parse_int(match)

            if number:
                results.append((row, column, number - 1))

            count += 1
            if column == self.size - 1:
                row += 1
                column = 0
            else:
                column += 1

            if count == self.length:
                break

        return results

    def parse_int(self, value):
        try:
            return int(value)
        except (TypeError, ValueError):
            return
