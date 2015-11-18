.PHONY: all test

TESTS=*.test

all: test

compile-check:
	@echo Checking for compiled *.out files.
	@echo This Makefile will fail if you haven\'t compiled first.
	[ -f input.out ]
	[ -f session.out ]

test: compile-check
	python test.py -f test-conf.json $(TESTS)

sanity: compile-check
	python test.py -f test-conf.json --fail-fast $(TESTS)

clean:
	@true

