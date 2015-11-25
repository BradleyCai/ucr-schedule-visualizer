# The purpose of this and the other Makefiles is to 'compile' the regular
# expressions found in the regex/ directory and inject them into their
# respective Javascript sources in the js/ directory. This is done by invoking
# a Python script in regex/ that combines multiple *.regex files into 'compiled'
# *.out files. The purpose of this is to break down these long and complicated
# regular expressions into more meaningful parts, which can be fixed easier.
# 
# This means that whenever you need to modify a regular epxression, you should
# only modify the *.regex files in regex/. The *.out files or the regular expressions
# in the javascript sources should not be modified, as they will be overwritten by
# this Makefile chain.

.PHONY: all compile inject clean

OBJECTS = input session

all: compile inject

compile: $(OBJECTS)

%:
	make -C regex $@
	cp regex/$@.out js/

inject:
	make -C js inject

clean:
	make -C regex clean
	make -C js clean


