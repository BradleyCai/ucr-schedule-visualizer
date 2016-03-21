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
            return "\0xx[31m\033[1mFAIL\033[0m"


if __name__ == "__main__":
    start_time = time.time()

    # Get command-line arguments
    argparser = argparse.ArgumentParser(description=
                                        "Perform tests on the regular expressions to ensure their stability.")
    argparser.add_argument("-c", "--config", nargs='?', default="test-config.json", help=
                           "Which Python configuration file to use. (default: config)")
    argparser.add_argument("-f", "--failfast", action="store_true", help=
                           "Whether to stop testing when a test fails. (default: false)")
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

    for test in test_files:
        if skip_test(test, config["ignore-tests"]):
            log("Ignoring %s..." % test)
            continue

        with open(test, 'r') as fh:
            data = parser.parse(os.path.basename(test), fh.readlines())

        tests.append(build_test(data, config))
    prep_elapsed = time.time() - start_time

    # Run tests
    start_time = time.time()
    passed = 0

    for test in tests:
        result = test.run()
        log("[%s] (%s) %s" % (format_result(result, args.nocolor), test.type, test.name))

        if not result and args.failfast:
            passed = -1
            break

    test_elapsed = time.time() - start_time

    # Report results
    log("Took %.2f seconds to prepare %d test%s." %
        (prep_elapsed, len(tests), plural(len(tests))))
    log("It took %.2f seconds to run the tests, each taking %.2f seconds on average." %
        test_elapsed, test_elapsed / len(tests))

    if args.failfast:
        if passed == -1:
            log("A test failed, so the suite was aborted.")
        else:
            log("All tests passed.")
    else:
        log("%d / %d (%.1%%) of tests passed.")

