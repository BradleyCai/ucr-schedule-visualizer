.PHONY: all regex inject clean

OBJECTS = input session

all: $(OBJECTS) inject

%:
	make -C regex $@
	cp regex/$@.out js/

inject:
	make -C js inject

clean:
	make -C regex clean
	make -C js clean


