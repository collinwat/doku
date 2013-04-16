"""
Usage:
    doku (-h | --help)
    doku (-v | --version)
    doku print_dlx
    doku save_cover_csv (-4 | -9) FILE

Options:
    -h, --help
    -v, --version
"""

from __future__ import with_statement
import os
import pkg_resources

from docopt import docopt

from doku import dlx
from doku import sudoku


def resource_path(*args):
    args = os.path.join(*args)
    return pkg_resources.resource_filename('doku', args)


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


def print_dlx(opts):
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


def save_cover_csv(opts):
    size = 4 if opts['-4'] else 9
    sudoku.ExactCoverTable(size).write_csv(opts['FILE'])


def main():
    args = docopt(__doc__)

    commands = {
        "print_dlx": print_dlx,
        "save_cover_csv": save_cover_csv
    }

    for command in commands:
        if args.get(command):
            commands[command](args)


if __name__ == '__main__':
    main()
