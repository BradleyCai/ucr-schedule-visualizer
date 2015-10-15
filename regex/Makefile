# Compiles all multi-regexes.

.PHONY: all clean
OBJECTS = input session

all: $(OBJECTS)

%:
	python sub_regex.py $@.regex $@.out

clean:
	rm *.out

