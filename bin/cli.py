#!/usr/bin/env python
"""
Usage:
    test.py print_all
    test.py print_dlx
    test.py print_game INDEX
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


ROOT = os.path.abspath(os.path.dirname(__file__))
GAMES = os.path.join(ROOT, 'data', 'games.txt')


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


def main():
    args = sys.argv[1:]
    if len(args) == 1 and args[0] == 'print_all':
        print_all()
    elif len(args) == 1 and args[0] == 'print_dlx':
        print_dlx()
    elif len(args) == 2 and args[0] == 'print_game' and args[1]:
        print_game(int(args[1]))
    else:
        print __doc__.strip()
        print ""


if __name__ == '__main__':
    main()
