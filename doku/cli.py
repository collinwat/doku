"""
Usage:
    doku print_all
     print_dlx
     print_game INDEX
     write_exact_cover
     write_exact_cover4
     write_exact_cover9
"""

import os
import sys
import linecache

BIN = os.path.abspath(os.path.dirname(__file__))
ROOT = os.path.dirname(BIN)

if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import dlx
import game
import parse
import sudoku


BIN = os.path.abspath(os.path.dirname(__file__))
ROOT = os.path.dirname(BIN)
DATA = os.path.join(ROOT, 'data')
GAMES = os.path.join(DATA, 'games.txt')


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


def print_dlx():
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


def print_all():
    with open(GAMES, 'r') as fd:
        lines = fd.readlines()

    parser = parse.StringParser()
    for i, line in enumerate(lines):
        if i != 0:
            print ''
            print '======================'
            print ''
        print 'Game %s:' % (i + 1)
        print ''
        print game.Game(parser.parse(line)).text


def print_game(pos):
    parser = parse.StringParser()
    line = linecache.getline(GAMES, pos)
    grid = parser.parse(line)
    print 'Game %s:' % pos
    print ''
    print game.Game(grid).text


def write_exact_cover(*args):
    if len(args) < 1:
        args = (4, 9)

    for size in args:
        filename = os.path.join(DATA, 'exact-cover-%sx%s.csv' % (size, size))
        sudoku.ExactCoverTable(size).write_csv(filename)

commands = {
    'print_all': print_all,
    'print_dlx': print_dlx,
    'write_exact_cover': write_exact_cover,
    'write_exact_cover4': lambda: write_exact_cover(4),
    'write_exact_cover9': lambda: write_exact_cover(9),
}


def main():
    args = sys.argv[1:]
    length = len(args)
    if length == 1 and args[0] in commands:
        commands[args[0]]()
    elif length == 2 and args[0] == 'print_game' and args[1]:
        print_game(int(args[1]))
    else:
        print __doc__.strip()
        print ""


if __name__ == '__main__':
    main()
