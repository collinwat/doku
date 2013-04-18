"""
Usage:
    doku (-h | --help)
    doku dlx_example
    doku exact_cover_csv (-4 | -9) FILE
    doku solve [(-4 | -9)] [BOARD]

Options:
    -h, --help
"""

from __future__ import with_statement

from docopt import docopt

from doku import dlx
from doku import sudoku


SUDOKU_EXAMPLE_4 = '.3..' \
                   '.1..' \
                   '..4.' \
                   '..3.'

SUDOKU_EXAMPLE_9 = '.........' \
                   '.....3.85' \
                   '..1.2....' \
                   '...5.7...' \
                   '..4...1..' \
                   '.9.......' \
                   '5......73' \
                   '..2.1....' \
                   '....4...9'


def print_v2(v2):
    for row in v2:
        print ' '.join(['%s' % cell for cell in row])


def print_matrix(a):
    s = dlx.UIMatrix(a).solve()

    print ""
    print "Matrix:"
    print "-------"
    print_v2(a)

    if len(s) > 0:
        for i, result in enumerate(s):
            print ""
            print "Solution %s:" % (i + 1)
            print "------------"
            print_v2(result)
        print ""
    else:
        print ""
        print "No Solution."
        print ""


def dlx_example(opts):
    print_matrix([[0, 0, 1, 0, 1, 1, 0],
                  [1, 0, 0, 1, 0, 0, 1],
                  [0, 1, 1, 0, 0, 1, 0],
                  [1, 0, 0, 1, 0, 0, 0],
                  [0, 1, 0, 0, 0, 0, 1],
                  [0, 0, 0, 1, 1, 0, 1]])

    print "=============="

    print_matrix([[1, 1, 0],
                  [1, 0, 1],
                  [0, 1, 1]])

    print "=============="

    print_matrix([[1, 1, 0],
                  [1, 0, 1],
                  [0, 0, 1],
                  [0, 1, 0]])


def exact_cover_csv(opts):
    size = 4 if opts['-4'] else 9
    sudoku.ExactCoverTable(size).write_csv(opts['FILE'])


def solve(opts):
    if opts.get('BOARD'):
        board = sudoku.Board(opts['BOARD'])
    if opts['-4']:
        board = sudoku.Board(SUDOKU_EXAMPLE_4)
    else:
        board = sudoku.Board(SUDOKU_EXAMPLE_9)

    print "Board:"
    print "==========="
    print board.text
    for i, solution in enumerate(board.solutions):
        board.solve(index=i)
        print ""
        print ""
        print "Solution %s:" % (i + 1)
        print "==========="
        print ""
        print board.line
        print ""
        print board.text
        board.reset()


def main():
    args = docopt(__doc__)

    commands = {
        "dlx_example": dlx_example,
        "exact_cover_csv": exact_cover_csv,
        "solve": solve,
    }

    for command in commands:
        if args.get(command):
            commands[command](args)


if __name__ == '__main__':
    main()
