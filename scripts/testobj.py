"""
This module contains the definitions for all test-related objects.
"""


class Test(object):
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def run(self):
        raise NotImplementedError("Abstract method.")


class NormalTest(Test):
    def __init__(self, name, type):
        Test.__init__(self, name, type)


class FailTest(Test):
    def __init__(self, name, type):
        Test.__init__(self, name, type)


def build_test(data, config):
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
        return build_normal_test(data, config)
    elif data["Type"] == "fail":
        return build_fail_test(data, config)
    else:
        print("%s: Unknown test type: \"%s\"." % data["filename"])
        print("%s: Supported types: normal, fail." % data["filename"])
        exit(1)


def build_normal_test(data, config):
    pass


def build_fail_test(data, config):
    pass

