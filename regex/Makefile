.PHONY: all clean

all: $(OBJECTS)

%:
	python sub_regex.py $@.regex $@.out

clean:
	rm -f *.out

