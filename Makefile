all: deps

deps:
	python setup.py develop easy_install xpsudoku[test] xpsudoku[dev]

clean:
	find . -name "*.pyc" -exec rm -f {} \;

tests:
	@python -m unittest discover tests '*_test.py'

.PHONY: all print.dlx tests
