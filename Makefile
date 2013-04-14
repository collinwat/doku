all: tests

print.dlx:
	@python bin/cli.py print_dlx

tests:
	@python -m unittest discover tests '*_test.py'

.PHONY: all print.dlx tests
