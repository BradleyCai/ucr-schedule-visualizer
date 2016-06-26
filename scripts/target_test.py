__all__ = ["config_fields", "run"]

from target import TargetProcess
from testparser import TestParser
import re
import os
import testobj

config_fields = {
    "fail-fast": bool,
    "test-dir": str,
    "recursive": bool,
    "ignore-tests": list,
    "regex": dict,
    "regex-order": list,
}

FAILED_TESTS_LOG_FILE = "failed.log"
TEST_FILE_REGEX = re.compile(r".+\.test", re.IGNORECASE)


def run(process):
    directory = "tests"
    if not os.path.isdir(directory):
        directory = "../tests"
    process.print_activity("Switching directory to \"%s\"" % directory)
    os.chdir(directory)

    process.print_activity("Getting screen size")
    SCREEN_HEIGHT, SCREEN_WIDTH = os.popen("stty size", 'r').read().split(" ")
    SCREEN_HEIGHT = int(SCREEN_HEIGHT)
    SCREEN_WIDTH = int(SCREEN_WIDTH)

    test_files = process.run_job(job_get_test_files, "Finding tests")
    process.config["ignore-tests"] = set(process.config["ignore-tests"])
    if not test_files:
        process.print_error("No *.test files found.")
        process.terminate()

    process.run_job(job_parse_tests, "Parsing %d test file%s" %
            (len(test_files), plural(len(test_files))), test_files)


### Defined jobs ###
def job_get_test_files(process):
    gen = os.walk(".", followlinks=True)
    test_files = []

    for dirpath, dirnames, filenames in gen:
        for filename in filenames:
            if TEST_FILE_REGEX.match(filename):
                test_files.append(os.path.join(dirpath, filename))

        if not process.config["recursive"]:
            break

    return sorted(test_files)


def job_parse_tests(process, test_files):
    regex = process.run_job(job_get_regular_expression_order, "Geting order of regular expressions")
    tests = process.run_job(job_add_tests, "Adding tests to queue", test_files, regex)


def job_add_tests(process, test_files, regex):
    parser = TestParser()
    tests = []

    for test in test_files:
        name = os.path.basename(test)

        if skip_test(test, process.config["ignore-tests"]):
            process.print_operation("SKIP", name)
            tests.append(testobj.SkipTest(name))
            continue

        try:
            with open(test, "r") as fh:
                data = parser.parse(name, fh.readlines())
        except IOError as err:
            process.print_error("Unable to open \"%s\": %s." % (test, err))
            process.terminate()

        process.print_operation("ADD", name)
        tests.append(testobj.build_test(data, process.config, regex))

    return tests


def job_get_regular_expression_order(process):
    regex = []

    for name in process.config["regex-order"]:
        process.print_operation("ITEM", name)
        regex.append(testobj.TestableRegex(name, process.config["regex"][name], process))

        if name not in process.config["regex"].keys():
            process.print_error(
                "Configuration error: regex \"%s\" mentioned in \"regex-order\" but not specified in \"regex\"."
                    % name)
            process.terminate()

    return tuple(regex)


### Helper functions ###
def plural(num):
    return "" if num == 1 else "s"


def skip_test(test, ignore):
    return test in ignore or \
           test[:-5] in ignore or \
           os.path.basename(test) in ignore or \
           os.path.basename(test[:-5]) in ignore

####

    log("\nResults:")
    # Run tests
    start_time = time.time()
    passed = 0
    skipped = 0
    testcount = len(tests)
    testsrun = testcount

    with open(FAILED_TESTS_LOG_FILE, 'a') as fail_fh:
        fail_fh.write("Test run on %s:\n" % time.ctime())

        for test in tests:
            test.set_error_log(fail_fh)
            result = test.run()

            # Print test result
            if args.show_type:
                testinfo = ("%s: %s" % (test.type, test.name)).ljust(SCREEN_WIDTH - 8)
            else:
                testinfo = test.name.ljust(SCREEN_WIDTH - 8)
            log("%s [%s]" % (testinfo, format_result(result, args.nocolor)))

            if result is None:
                skipped += 1
                testsrun -= 1
            elif not result and args.failfast:
                passed = -1
                break

    test_elapsed = time.time() - start_time

    # Report results
    log("\nRan %d test%s." % (testsrun, plural(testsrun)))
    log("Preparation: %.2f seconds per test, %.2f seconds total." % (prep_elapsed / testcount, prep_elapsed))

    if testsrun == 0:
        log("No tests were run.")
        sys.exit(0)

    log("Runtime:     %.2f seconds per test, %.2f seconds total." % (test_elapsed / testsrun, test_elapsed))

    if args.failfast:
        if passed == -1:
            log("A test failed, so the suite was aborted.")
        else:
            log("All tests passed.")
    else:
        log("%d / %d (%.1f%%) of tests passed." % (passed, testsrun, 100.0 * passed / testsrun))

    if passed < testcount:
        log("Wrote report for failed tests in \"tests/%s\"." % FAILED_TESTS_LOG_FILE)

    sys.exit(testsrun - passed)
####
