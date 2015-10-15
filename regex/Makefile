# Compiles all multi-regexes.

.PHONY: all clean
OBJECTS = master session

all: $(OBJECTS)

%:
	python sub_regex.py $@.regex $@.out

clean:
	rm *.out

