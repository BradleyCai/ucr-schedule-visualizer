"""
This module contains the definitions for all test-related objects.
"""


class Test(object):
    def __init__(self, type, name, input, regex):
        self.type = type
        self.name = name
        self.input = input
        self.regex = regex

    def run(self):
        raise NotImplementedError("Abstract method.")


class NormalTest(Test):
    def __init__(self, name, input, regex, outputs):
        Test.__init__(self, "normal", name, input, regex)
        self.outputs = outputs

    def run(self):
        pass


class FailTest(Test):
    def __init__(self, name, input, regex):
        Test.__init__(self, "fail", name, input, regex)

    def run(self):
        pass


def build_test(data, regex):
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
        if key.endswith("Output"):
            key_name = key[:-6].lower()
            outputs[key_name] = tuple(string.splitlines() for string in data[key])

    return NormalTest(data["Name"], data["Input"], regex, outputs)


def build_fail_test(data, regex):
    return FailTest(data["Name"], data["Input"], regex)

