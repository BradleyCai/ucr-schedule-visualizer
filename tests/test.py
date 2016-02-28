#!/usr/bin/python
from __future__ import division, print_function
import argparse
import json
import re
import sys

TEST_FILE_REGEX = re.compile(r"(%%%|!!!) *([^\n]*)\n(.*?)~~~", re.DOTALL)


class Test(object):
    def __init__(self, config, name, input, output):
        self.config = config
        self.name = name
        self.input = input
        self.output = output

    def __call__(self, fail_fast=False):
        print("Test \"%s\":" % self.name)
        failed = 0
        for regex in self.config:
            result = regex.match(self.input)
            # TODO
            passed = (result is not None) and (result.groups() == self.output)
            if passed:
                print(" [PASSED] %s" % self.input)
            else:
                print(" [FAILED] %s" % self.input)
                if fail_fast:
                    return False
                else:
                    failed += 1

            if fail_fast:
                return True
            else:
                return failed


def convert_json(data):
    if isinstance(data, dict):
        return { convert_json(key) : convert_json(data) for key, data in data.items() }
    elif isinstance(data, list):
        return [ convert_json(element) for element in data ]
    else:
        return data


def sanity_check(config):
    def valid_regex(data):
        if "file" not in data.keys() and not isistance(config["file"], str):
            print("'file' property is missing or not a string.")
            return False
        elif "groups" not in data.keys():
            print("'groups' property is missing.")
            return False
        else:
            return valid_groups(data["groups"])

    def valid_groups(data):
        if not isinstance(data, list):
            print("'groups' property must be a list.")
            return False
        for element in data:
            if not isinstance(element, bool) and not valid_regex(element):
                print("'groups' element must be a boolean or valid 'regex' object.")
                return False
        return True

    if not "regex" in config.keys() or not isinstance(config["regex"], dict):
        print("Missing or malformed 'regex' property.")
        return False
    if not valid_regex(config["regex"]):
        return False

    return True


if __name__ == "__main__":
    # Parse command line arguments
    argparser = argparse.ArgumentParser(description=\
            "Test regular expressions to make sure they perform as expected.")
    argparser.add_argument("-c", "--config-file", nargs=1, type=open, help=\
            "Specify the configuration file to use when running tests.")
    argparser.add_argument("-F", "--fail-fast", action="store_true", help=\
            "Specifies that testing should terminate when a test fails.")
    argparser.add_argument("test-file", nargs='+', type=open, help=\
            "The *.test files that describe the tests to be performed.")
    args = argparser.parse_args(sys.argv[1:])

    # Parse config file
    config = convert_json(json.loads(args.config_file[0].read()))
    if not sanity_check(config):
        print("Errors parsing configuration file.")
        exit(1)

    # Generate list of tests
    tests = []
    for fh in getattr(args, "test-file"):
        matches = TEST_FILE_REGEX.findall(fh.read())
        for match in matches:
            print(match)
            print(match[2].split("~\n"))
            #tests.append(Test(

    testcount = len(tests)
    plural = "" if testcount == 1 else "s"

    # Perform all the tests
    print("Running %d test%s..." % (testcount, plural))

    if args.fail_fast:
        failed = False
        for test in tests:
            if not test(True):
                failed = True
                break

        if failed:
            print("Not all tests passed.")
            exit(1)
        else:
            print("All tests passed.")
            exit(0)
    else:
        passed = testcount
        for test in tests:
            passed -= test(False)

        if testcount:
            print("%d / %d test%s passed (%.2f%%)." % (passed, testcount, plural, passed / testcount))
        else:
            print("0 / 0 tests passed.")
        exit(testcount - passed)

