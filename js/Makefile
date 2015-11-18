.PHONY: all inject clean

all: inject

inject:
	python update_regex.py regex input.regex CourseParser.js
	python update_regex.py subCourseRegex session.regex CourseParser.js

clean:
	rm -f *.regex

