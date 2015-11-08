# Compiles all multi-regexes.

.PHONY: all inject clean
OBJECTS = input session

all: $(OBJECTS) inject

%:
	python sub_regex.py $@.regex $@.out

inject:
	python update_regex.py regex input.out ../js/CourseParser.js
	python update_regex.py subCourseRegex session.out ../js/CourseParser.js

clean:
	rm *.out

