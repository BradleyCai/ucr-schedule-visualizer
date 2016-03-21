#!/usr/bin/env python

from __future__ import print_function
import argparse
import os
import re
import sys
import time

try:
    import jsonconfig
except ImportError:
    print("Cannot local modules. Are you in the right directory?")
    exit(1)

CONFIG_FIELDS = {
    "test-dir": str,
    "recursive": bool,
    "ignore-tests": list,
    "regex": dict,
}

TEST_FILE_REGEX = re.compile(r".+\.test", re.IGNORECASE)


def get_tests(recursive):
    gen = os.walk(".", followlinks=True)
    tests = {}

    if hasattr(gen, "next"):
        next = gen.next
    else:
        next = gen.__next__

    for dirpath, dirnames, filenames in next():
        dirpath = os.path.basename(dirpath)
        tests[dirpath] = []

        for filename in filenames:
            if TEST_FILE_REGEX.match(filename):
                tests[dirpath].append(filename)

        if not recursive:
            break

    return tests


class Test(object):
    pass


if __name__ == "__main__":
    start_time = time.time()

    # Get command-line arguments
    argparser = argparse.ArgumentParser(description=
                                        "Perform tests on the regular expressions to ensure their stability.")
    argparser.add_argument("-c", "--config", nargs='?', default="test-config.json", help=
                           "Which Python configuration file to use. (default: config)")
    argparser.add_argument("-f", "--failfast", nargs='?', action="store_true", help=
                           "Whether to stop testing when a test fails. (default: false)")
    argparser.add_argument("-q", "--quiet", nargs='?', action="store_true", help=
                           "Suppress all output except warnings and errors.")
    args = argparser.parse_args(sys.argv[1:])
    config = jsonconfig.load(args.config)
    jsonconfig.sanity_check(config, CONFIG_FIELDS)

    if args.quiet:
        log = lambda x: None
    else:
        log = print

    # Change directory
    startdir = os.path.dirname(sys.argv[0]);
    directory = os.path.join(startdir, "tests")
    if not os.path.isdir(directory):
        directory = os.path.realpath(os.path.join(startdir, "../tests"))
    log("Switching directory to \"%s\"..." % directory)
    os.chdir(directory)

    # Load tests
    test_list = get_tests(config["recursive"])

    # Parse tests


    # Run tests


    # Report results
