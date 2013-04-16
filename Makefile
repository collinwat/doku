all: deps

deps:
	python setup.py develop easy_install doku[test] doku[dev]

clean:
	@find . -name "*.pyc" -exec rm -f {} \;
	@find . -name "__pycache__" -exec rm -rf {} \;

tests:
	@tox

.PHONY: all print.dlx tests
