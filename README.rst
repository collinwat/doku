Doku
====

Doku is a general sudoku library. It can be used to solve classic sudoku
puzzles as well as sudoku variants.

A simple cli is provided to work with sudoku puzzles on the command line
as well as provide hooks into the problem solving process.

Solver
------
The Sudoku puzzle solver uses the Dancing Links technique to implement
Knuth's Algorithm X.

**Warning:** The current dlx technique was implmented as a learning exercise. There
is probably a more optimal solution. This means that the internals of this
library are in flux and should not be considered production ready.

References
----------
- http://www-cs-faculty.stanford.edu/~knuth/preprints.html
- http://en.wikipedia.org/wiki/Dancing_Links
- http://en.wikipedia.org/wiki/Knuth's_Algorithm_X
- http://www.ocf.berkeley.edu/~jchu/publicportal/sudoku/sudoku.paper.html
- http://www.ocf.berkeley.edu/~jchu/publicportal/sudoku/0011047.pdf
- http://en.wikipedia.org/wiki/Exact_cover
- http://buzzard.ups.edu/talks/beezer-2010-stellenbosch-sudoku.pdf
