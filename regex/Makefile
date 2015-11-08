.PHONY: all clean

all: $(OBJECTS) inject

%:
	python sub_regex.py $@.regex $@.out

clean:
	rm -f *.out

