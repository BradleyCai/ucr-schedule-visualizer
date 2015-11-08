.PHONY: all inject clean

all: inject

inject:
	python update_regex.py regex input.out js/CourseParser.js
	python update_regex.py subCourseRegex session.out js/CourseParser.js

clean:
	rm *.out

