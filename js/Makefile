.PHONY: all inject clean

all: inject

inject:
	python update_regex.py regex input.out CourseParser.js gm
	python update_regex.py subCourseRegex session.out CourseParser.js gm

clean:
	rm -f *.out

