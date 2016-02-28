# Configuration settings for build.py
# This file should not run any code, just define variables.

# Which files should be compiled.
SOURCE_FILES = ["session", "input"]

# The directory that contains all the *.regex files.
REGEX_DIRECTORY = "regex"

# Which directories the *.out files should be copied to.
COPY_TO = ["../js", "../tests"]

# The directory that contains the injection file.
INJECT_DIRECTORY = "../js"

# The file to have the regular expressions injected into.
INJECT_FILE = "CourseParser.js"

# What variables should be injected with which compiled regexes.
# These items should be in the form: {'output-file' : 'field name'}.
TO_INJECT = {
    "input.out": "regex",
    "session.out": "subCourseRegex",
}

