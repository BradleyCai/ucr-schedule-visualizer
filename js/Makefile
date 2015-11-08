.PHONY: all inject clean

all: inject

inject:
	python update_regex.py regex input.out CourseParser.js
	python update_regex.py subCourseRegex session.out CourseParser.js

clean:
	rm -f *.out

