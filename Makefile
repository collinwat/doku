all: deps

deps:
	python setup.py develop easy_install doku[test] doku[dev]

clean:
	@find . -name "*.pyc" -exec rm -f {} \;
	@find . -name "__pycache__" -exec rm -rf {} \;

data:
	doku save_cover_csv -4 doku/data/sudoku-cover-4x4.csv
	doku save_cover_csv -9 doku/data/sudoku-cover-9x9.csv

tests:
	@tox

.PHONY: all print.dlx tests
