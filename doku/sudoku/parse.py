class UnknownCharacterError(ValueError):
    FORMAT = 'Parser does not know how to handle the "%s" character'

    def __init__(self, character):
        super(UnknownCharacterError, self).__init__(self.FORMAT % character)


class StringParser(object):

    def parse(self, line):
        if not line or len(line) < 81:
            return
        return [self.parse_char(c) for c in line[0:81]]

    def parse_char(self, value):
        if not value or value == '.':
            return '.'

        result = self.parse_int(value)

        if not result or result < 1 or result > 9:
            raise UnknownCharacterError(value)

        return result

    def parse_int(self, value):
        try:
            return int(value)
        except (TypeError, ValueError):
            return
