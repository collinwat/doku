Doku
====

Doku is a general sudoku library. It can be used to solve classic sudoku
puzzles as well as sudoku variants.

The Dancing Links technique is used to implement Knuth's Algorithm X:

- http://en.wikipedia.org/wiki/Dancing_Links
- http://en.wikipedia.org/wiki/Knuth's_Algorithm_X

  **DISCLAIMER:**
  The current dlx technique was implmented as a learning exercise. There
  is probably a more optimal solution. This means the internals of this
  library are in flux and hence, should be treated as beta.

A simple cli is provided to work with sudoku puzzles on the command line
as well as provide hooks into the problem solving process.
