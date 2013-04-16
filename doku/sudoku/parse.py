import utils


class UnknownCharacterError(ValueError):
    FORMAT = 'Parser does not know how to handle the "%s" character'

    def __init__(self, character):
        super(UnknownCharacterError, self).__init__(self.FORMAT % character)


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

        if size != 4 and size != 9:
            msg = 'The size "%s" is invalid. Size can only be 4 or 9.'
            raise ValueError(msg, size)

        self.size = size
        self.length = size * size
        self.box_size = utils.box_size(size)

    def iparse(self, line):
        if not line or len(line) < self.length:
            return
        row = 0
        column = 0
        count = 0

        for c in line:
            c = c.strip()

            if c == '':
                continue

            number = self.parse_char(c)

            if number:
                yield (row, column, number - 1)

            count += 1
            if column == self.size - 1:
                row += 1
                column = 1
            else:
                column += 1

            if count == self.length:
                return

    def parse_char(self, value):
        if value == '.':
            return

        result = self.parse_int(value)

        if not result or result < 1 or result > 9:
            raise UnknownCharacterError(value)

        return result

    def parse_int(self, value):
        try:
            return int(value)
        except (TypeError, ValueError):
            return
