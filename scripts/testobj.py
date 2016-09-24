# Copyright (C) 2015-2016 Ammon Smith and Bradley Cai
# Available for use under the terms of the MIT License.

"""
This module contains the definitions for all test-related objects.
"""

__all__ = [
    'TestableRegex',
    'Test',
    'SkipTest',
    'NormalTest',
    'FailTest',
    'build_normal_test',
    'build_fail_test',
    'build_skip_test',

    'TEST_BUILDERS',
]

import codecs
import re

TEST_FILE_REGEX = re.compile(r'(.+)\.test', re.IGNORECASE)
MULTIPLE_REGEX_FIELD_NAME_REGEX = re.compile(r'Allow([A-Za-z]+)Multiple')
OUTPUT_FIELD_NAME_REGEX = re.compile(r'([A-Za-z]+)Output')
PYTHON_ESCAPE_SEQUENCE_REGEX = re.compile(
    r'''(\\U.{8}|\\u.{4}|\\x.{2}|\\[0-7]{1,3}|\\N\{[^}]+\}|\\[\\'"abfnrtv])''')


# Class definitions
class TestableRegex(object):
    def __init__(self, name, config, target):
        flags = 0
        for flag in config.get('flags', ()):
            if not hasattr(re, flag):
                print("Invalid regex flag: \"%s\"." % flag)
                exit(1)

            flags |= getattr(re, flag)

        with open(config['source'], 'r') as fh:
            self.regex = re.compile(fh.read().rstrip(), flags)

        self.name = name
        self.multiple = config.get('multiple', True)
        self.group = config.get('group', 0)
        self.target = target

    def test(self, input):
        if self.multiple:
            match = self.regex.match(input)

            if match:
                groups = match.groups()
            else:
                groups = None

            return groups
        else:
            return self.regex.findall(input)


class Test(object):
    error_file_handle = None

    @staticmethod
    def set_up_error_log(filename):
        if filename is None:
            filename = os.devnull

        # Let target_test deal with any exceptions
        Test.error_file_handle = open(filename, 'w')

    def __init__(self, type, name, input, regex):
        self.type = type
        self.name = name
        self.input = input
        self.regex = regex
        self.wrote_to_error_log = False

    def run(self):
        raise NotImplementedError("Abstract method.")

    def write_test_name_to_error_log(self):
        if not self.wrote_to_error_log:
            self.wrote_to_error_log = True
            self.write_to_error_log("[%s]" % self.name)

    def write_to_error_log(self, message):
        self.write_test_name_to_error_log()
        if Test.error_file_handle:
            Test.error_file_handle.write(message)
            Test.error_file_handle.write("\n")

    def results_equal(self, expected, actual):
        expected = expected[0]

        if actual and type(actual[0]) != str:
            actual = actual[0]

        for i in range(len(expected)):
            if expected[i] != actual[i]:
                self.write_test_name_to_error_log()
                self.write_to_error_log("Expected: %s" % expected)
                self.write_to_error_log("Actual: %s" % actual)
                return False

        return True

    def __hash__(self):
        return hash(self.type) ^ hash(self.name)

    def __eq__(self, other):
        return type(self) == type(other) and hash(self) == hash(other)

    def __repr__(self):
        return "%s: \"%s\"" % (type(self).__name__, self.name)


class SkipTest(Test):
    def __init__(self, name):
        Test.__init__(self, 'skip', self.format_test_name(name), None, None)

    def run(self):
        return None

    @staticmethod
    def format_test_name(string):
        match = TEST_FILE_REGEX.match(string.title())
        if match:
            return match.group(1)
        else:
            return string


class NormalTest(Test):
    def __init__(self, name, input, regex, outputs):
        Test.__init__(self, 'normal', name, input, regex)
        self.outputs = outputs

    def run(self):
        input = self.input
        for regex in self.regex:
            results = regex.test(input)

            if not results:
                self.write_to_error_log("The following input produced no input:\n%s\n***" % input)
                return False

            if not self.results_equal(self.outputs[regex.name], results):
                return False

            print(self.outputs[regex.name])
            print(results)
            print(self.outputs)

            if regex.group <= 0:
                break

            input = results[0][regex.group - 1]
            print(input)
            exit(-1)

        return True


class FailTest(Test):
    def __init__(self, name, input, regex):
        Test.__init__(self, "fail", name, input, regex)

    def run(self):
        # TODO
        return None


# Helper functions
def decode_escapes(string):
    def decode_match(match):
        return codecs.decode(match.group(0), 'unicode-escape')
    return PYTHON_ESCAPE_SEQUENCE_REGEX.sub(decode_match, string)


def get_outputs(groups, escape):
    if not escape:
        return [string.splitlines() for string in groups]
    else:
        outputs = []

        for string in groups:
            lines = []

            for line in string.splitlines():
                lines.append(decode_escapes(line))

            outputs.append(lines)
        return outputs


# Factory functions
def build_normal_test(data, regex):
    outputs = {}
    for key in data.keys():
        match = OUTPUT_FIELD_NAME_REGEX.match(key)
        if match:
            name = match.group(1).lower()
            outputs[name] = get_outputs(data[key], data["EscapeStrings"])

    return NormalTest(data["Name"], data["Input"], regex, outputs)


def build_fail_test(data, regex):
    return FailTest(data["Name"], data["Input"], regex)


def build_skip_test(data, regex):
    return SkipTest(data["Name"])


TEST_BUILDERS = {
    "normal": build_normal_test,
    "fail": build_fail_test,
}

