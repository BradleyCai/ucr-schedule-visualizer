#!/usr/bin/env python

from __future__ import print_function
import argparse
import os
import re
import sys
import time

try:
    from testparser import TestParser
    from testobj import build_test
    import jsonconfig
    import testobj
except ImportError:
    print("Cannot local modules. Are you in the right directory?")
    exit(1)

CONFIG_FIELDS = {
    "test-dir": str,
    "recursive": bool,
    "ignore-tests": list,
    "regex": dict,
    "regex-order": list,
}

TEST_FILE_REGEX = re.compile(r".+\.test", re.IGNORECASE)


class TestableRegex(object):
    def __init__(self, config):
        flags = 0
        for flag in config.get("flags", ()):
            if not hasattr(re, flag):
                print("Invalid regex flag: \"%s\"." % flag)
                exit(1)

            flags |= getattr(re, flag)

        with open(config["source"], 'r') as fh:
            self.regex = re.compile(fh.read().rstrip(), flags)

        self.multiple = config.get("multiple", True)

    def test(self, input):
        result = self.regex.match(input)
        return result.groups() if result else None


def get_tests(recursive):
    gen = os.walk(".", followlinks=True)
    tests = []

    for dirpath, dirnames, filenames in gen:
        for filename in filenames:
            if TEST_FILE_REGEX.match(filename):
                tests.append(os.path.join(dirpath, filename))

        if not recursive:
            break

    return tests


def get_regular_expression_order(config):
    regex = []

    for name in config["regex-order"]:
        if name not in config["regex"].keys():
            print("Configuration error: regex \"%s\" mentioned in \"regex-order\" but not specified in \"regex\"." % name)
            exit(1)

        regex.append(TestableRegex(config["regex"][name]))

    return regex


def plural(num):
    return "" if num == 1 else "s"


def skip_test(test, ignore):
    return test in ignore or \
           test[:-5] in ignore or \
           os.path.basename(test) in ignore or \
           os.path.basename(test[:-5]) in ignore


def format_result(result, nocolor):
    if nocolor:
        if result:
            return "PASS"
        else:
            return "FAIL"
    else:
        if result:
            return "\033[32mPASS\033[0m"
        else:
            return "\033[31m\033[1mFAIL\033[0m"


if __name__ == "__main__":
    start_time = time.time()

    # Get command-line arguments
    argparser = argparse.ArgumentParser(description=
                                        "Perform tests on the regular expressions to ensure their stability.")
    argparser.add_argument("-c", "--config", nargs='?', default="test-config.json", help=
                           "Which Python configuration file to use. (default: config)")
    argparser.add_argument("-f", "--failfast", action="store_true", help=
                           "Whether to stop testing when a test fails. (default: false)")
    argparser.add_argument("-t", "--show-type", action="store_true", help=
                           "Print the test type when displaying test results. (default: false)")
    argparser.add_argument("--nocolor", action="store_true", help=
                           "Suppress color in the text output.")
    argparser.add_argument("-q", "--quiet", action="store_true", help=
                           "Suppress all output except warnings and errors.")
    args = argparser.parse_args(sys.argv[1:])
    config = jsonconfig.load(args.config)
    jsonconfig.sanity_check(config, CONFIG_FIELDS)

    if args.quiet:
        log = lambda x: None
    else:
        log = print

    SCREEN_HEIGHT, SCREEN_WIDTH = os.popen("stty size", 'r').read().split(" ")
    SCREEN_HEIGHT = int(SCREEN_HEIGHT)
    SCREEN_WIDTH = int(SCREEN_WIDTH)

    # Change directory
    startdir = os.path.dirname(sys.argv[0])
    directory = os.path.join(startdir, "tests")
    if not os.path.isdir(directory):
        directory = os.path.realpath(os.path.join(startdir, "../tests"))
    log("Switching directory to \"%s\"..." % directory)
    os.chdir(directory)

    # Load tests
    test_files = sorted(get_tests(config["recursive"]))
    config["ignore-tests"] = set(config["ignore-tests"])
    if not test_files:
        log("No .test files found. Exiting.")
        exit(0)

    log("Parsing %d .test file%s..." % (len(test_files), plural(len(test_files))))

    # Parse and create tests
    parser = TestParser()
    tests = []

    regex = get_regular_expression_order(config)

    for test in test_files:
        if skip_test(test, config["ignore-tests"]):
            log("Ignoring %s..." % test)
            continue

        with open(test, 'r') as fh:
            data = parser.parse(os.path.basename(test), fh.readlines())

        tests.append(build_test(data, regex))
    prep_elapsed = time.time() - start_time

    log("\nResults:")
    # Run tests
    start_time = time.time()
    passed = 0
    testcount = len(tests)

    for test in tests:
        result = test.run()

        # Print test result
        if args.show_type:
            testinfo = ("%s: %s" % (test.type, test.name)).ljust(SCREEN_WIDTH - 8)
        else:
            testinfo = test.name.ljust(SCREEN_WIDTH - 8)
        log("%s [%s]" % (testinfo, format_result(result, args.nocolor)))

        if not result and args.failfast:
            passed = -1
            break

    test_elapsed = time.time() - start_time

    # Report results
    log("\nTook %.2f seconds to prepare %d test%s." %
        (prep_elapsed, testcount, plural(testcount)))
    log("It took %.2f seconds to run the tests, each taking %.2f seconds on average." %
        (test_elapsed, test_elapsed / testcount))

    if args.failfast:
        if passed == -1:
            log("A test failed, so the suite was aborted.")
        else:
            log("All tests passed.")
    else:
        log("%d / %d (%.1f%%) of tests passed." % (passed, testcount, 100.0 * passed / testcount))

    sys.exit(testcount - passed)

