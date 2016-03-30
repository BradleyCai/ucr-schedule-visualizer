"""
This module contains the definitions for all test-related objects.
"""
import codecs
import re

MULTIPLE_REGEX_FIELD_NAME_REGEX = re.compile(r"Allow([A-Za-z]+)Multiple")
OUTPUT_FIELD_NAME_REGEX = re.compile(r"([A-Za-z]+)Output")
PYTHON_ESCAPE_SEQUENCE_REGEX = re.compile(r"""(\\U........|\\u....|\\x..|\\[0-7]{1,3}|\\N\{[^}]+\}|\\[\\'"abfnrtv])""")


class Test(object):
    def __init__(self, type, name, input, regex):
        self._logfh = None
        self.type = type
        self.name = name
        self.input = input
        self.regex = regex

    def set_error_log(self, fh):
        self._logfh = fh

    def log_error(self, message):
        if self._logfh:
            self._logfh.write(message)
            self._logfh.write("\n")

    def run(self):
        raise NotImplementedError("Abstract method.")


class NormalTest(Test):
    def __init__(self, name, input, regex, outputs):
        Test.__init__(self, "normal", name, input, regex)
        self.outputs = outputs

    def run(self):
        print(self.outputs)


class FailTest(Test):
    def __init__(self, name, input, regex):
        Test.__init__(self, "fail", name, input, regex)

    def run(self):
        pass


def get_boolean_option(filename, string):
    string = string.lower()
    if string in ("true", "yes", "enable", "enabled", "set", "1"):
        return True
    elif string in ("false", "no", "disable", "disabled", "unset", "0"):
        return False
    else:
        print("%s: Unknown boolean: \"%s\"." % (filename, string))
        exit(1)


def decode_escapes(string):
    def decode_match(match):
        return codecs.decode(match.group(0), "unicode-escape")
    return PYTHON_ESCAPE_SEQUENCE_REGEX.sub(decode_match, string)


def get_outputs(groups, escape):
    if not escape:
        return tuple(tuple(string.splitlines()) for string in groups)
    else:
        outputs = []

        for string in groups:
            lines = []

            for line in string.splitlines():
                lines.append(decode_escapes(line))

            outputs.append(tuple(lines))
        return tuple(outputs)


def build_test(data, config, regex):
    if "Name" not in data.keys():
        print("%s: No name specified." % data["filename"])
        exit(1)

    if len(data["Name"]) > 1:
        print("%s: Multiple names specified." % data["filename"])
        exit(1)

    data["Name"] = data["Name"][0]

    if "Type" not in data.keys():
        print("%s: No test type specified." % data["filename"])
        exit(1)

    if len(data["Type"]) > 1:
        print("%s: Multiple test types specified." % data["filename"])
        exit(1)

    data["Type"] = data["Type"][0]

    if "EscapeStrings" in data.keys():
        if len(data["EscapeStrings"]) > 1:
            print("%s: Setting 'EscapeStrings' set multiple times." % data["filename"])
            exit(1)

        data["EscapeStrings"] = get_boolean_option(data["filename"], data["EscapeStrings"][0])
    else:
        data["EscapeStrings"] = False

    for key in data.keys():
        match = MULTIPLE_REGEX_FIELD_NAME_REGEX.match(key)
        if match:
            name = match.group(1).lower()
            regex[name].multiple = get_boolean_option(data["filename"], data[key])

    if data["Type"] == "normal":
        return build_normal_test(data, regex)
    elif data["Type"] == "fail":
        return build_fail_test(data, regex)
    else:
        print("%s: Unknown test type: \"%s\"." % data["filename"])
        print("%s: Supported types: normal, fail." % data["filename"])
        exit(1)


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

