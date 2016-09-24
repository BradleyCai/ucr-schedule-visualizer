# Copyright (C) 2015-2016 Ammon Smith and Bradley Cai
# Available for use under the terms of the MIT License.

__all__ = [
    'depends',
    'config_fields',
    'run'
]

from do_target import targetobj
from testparser import TestParser
import re
import os
import testobj

depends = [
    'build',
]

config_fields = {
    'fail-fast': bool,
    'show-type': bool,
    'show-skipped': bool,
    'test-dir': str,
    'recursive': bool,
    'failed-test-log': (str, type(None)),
    'ignore-tests': list,
    'regex': dict,
    'regex-order': list,
}

TEST_FILE_REGEX = re.compile(r'.+\.test', re.IGNORECASE)


def run(tracker):
    if len(tracker.config['regex'].keys()) != len(tracker.config['regex-order']) or \
            not set(tracker.config['regex'].keys()).issubset(tracker.config['regex-order']):
        tracker.print_error("Configuration fields \"regex\" and \"regex-order\" don't match up.")
        tracker.print_error("\"regex-order\" should be an ordered list of the keys in \"regex\".")
        tracker.terminate()

    directory = 'tests'
    if not os.path.isdir(directory):
        directory = '../tests'
    tracker.print_activity("Switching directory to \"%s\"" % directory)
    os.chdir(directory)

    regex = tracker.run_job(job_get_regular_expression_order, "Geting order of regular expressions")
    test_files = tracker.run_job(job_get_test_files, "Finding tests")

    tracker.config['ignore-tests'] = set(tracker.config['ignore-tests'])
    if not test_files:
        tracker.print_error("No *.test files found.")
        tracker.terminate()

    tests = tracker.run_job(job_parse_tests, "Parsing %d test file%s" %
            (len(test_files), plural(len(test_files))), test_files, regex)

    passed, skipped, testcount, testsrun = \
            tracker.run_job(job_run_tests, "Running tests", tests)
    tracker.run_job(job_print_results, "Test results", \
            passed, skipped, testcount, testsrun)


### Defined jobs ###
def job_get_regular_expression_order(tracker):
    regex = []
    counter = 1

    for name in tracker.config['regex-order']:
        tracker.print_operation(counter, name)
        regex.append(testobj.TestableRegex(name, tracker.config['regex'][name], tracker))

        if name not in tracker.config['regex'].keys():
            tracker.print_error(
                "Configuration error: regex \"%s\" mentioned in \"regex-order\" but not specified in \"regex\"."
                    % name)
            tracker.terminate()
        counter += 1

    return tuple(regex)


def job_get_test_files(tracker):
    gen = os.walk('.', followlinks=True)
    test_files = []

    for dirpath, dirnames, filenames in gen:
        for filename in filenames:
            if TEST_FILE_REGEX.match(filename):
                test_files.append(os.path.join(dirpath, filename))

        if not tracker.config['recursive']:
            break

    return sorted(test_files)


def job_parse_tests(tracker, test_files, regex):
    parser = TestParser()
    tests = []

    if not test_files:
        tracker.print_string("(nothing to do)")

    for test_file in test_files:
        name = os.path.basename(test_file)

        if skip_test(test_file, tracker.config['ignore-tests']):
            if tracker.config['show-skipped']:
                tracker.print_operation('SKIP', name)
                tests.append(testobj.SkipTest(name))
            continue

        tracker.print_operation("ADD", name)
        try:
            with open(test_file, 'r') as fh:
                data = parser.parse(name, fh.readlines())
        except IOError as err:
            tracker.print_error("Unable to open \"%s\": %s." % (test_file, err))
            tracker.failure()

        # Take the collected data and build the test object
        test = tracker.run_job(job_build_test, None, data, regex)
        if test:
            tests.append(test)

    return tests


def job_build_test(tracker, data, regex):
    if 'Name' not in data.keys():
        tracker.print_error("%s: No name specified." % data['filename'])
        tracker.failure()
        return None

    if len(data['Name']) > 1:
        tracker.print_error("%s: Multiple names specified." % data['filename'])
        tracker.failure()
        return None

    data['Name'] = data['Name'][0]

    if 'Type' not in data.keys():
        tracker.print_error("%s: No test type specified." % data['filename'])
        tracker.failure()
        return None

    if len(data['Type']) > 1:
        tracker.print_error("%s: Multiple test types specified." % data['filename'])
        tracker.failure()
        return None

    data['Type'] = data['Type'][0]

    if 'Input' not in data.keys():
        tracker.print_error("%s: No input value specified." % data['filename'])
        tracker.failure()
        return None

    if len(data['Input']) > 1:
        tracker.print_error("%s: Multiple input values specified." % data['filename'])
        tracker.failure()
        return None

    data['Input'] = data['Input'][0] + '\n'

    if 'EscapeStrings' in data.keys():
        if len(data['EscapeStrings']) > 1:
            tracker.print_error("%s: Setting 'EscapeStrings' set multiple times." % data['filename'])
            tracker.failure()
            return None

        data['EscapeStrings'] = get_boolean_option(tracker, data['filename'], data['EscapeStrings'][0])

        if data['EscapeStrings'] is None:
            return None
    else:
        data['EscapeStrings'] = False

    for key in data.keys():
        match = testobj.MULTIPLE_REGEX_FIELD_NAME_REGEX.match(key)
        if match:
            name = match.group(1).lower()
            regex[name].multiple = get_boolean_option(tracker, data['filename'], data[key])
            if regex[name].multiple is None:
                return None

    for regex_value in regex:
        regex_value.group = tracker.config['regex'][regex_value.name].get('group', 0)

    try:
        return testobj.TEST_BUILDERS[data['Type']](data, regex)
    except KeyError:
        tracker.print_error("%s: Unknown test type: \"%s\"." % data['filename'])
        tracker.print_notice("Supported test types: %s." % (', '.join(testobj.TEST_BUILDERS.keys())))
        tracker.failure()
        return None


def job_run_tests(tracker, tests):
    passed = 0
    skipped = 0
    testcount = len(tests)
    testsrun = testcount

    testobj.Test.set_up_error_log(tracker.config['failed-test-log'])

    for test in tests:
        result = test.run()

        if tracker.config['show-type']:
            testinfo = "%s (%s)" % (test.name, test.type)
        else:
            testinfo = test.name

        if result is None:
            tracker.print_operation("SKIP", testinfo)
            skipped += 1
        elif result is True:
            tracker.print_operation("PASS", testinfo, targetobj.GREEN)
            passed += 1
        elif result is False:
            tracker.print_operation("FAIL", testinfo, targetobj.RED)

            if tracker.config['fail-fast']:
                passed = -1
                return
        else:
            tracker.print_error("Invalid test return value: %s\n" % result)
            tacker.terminate()

    return passed, skipped, testcount, testsrun


def job_print_results(tracker, passed, skipped, testcount, testsrun):
    if passed < testsrun and tracker.args.usecolor:
        label = "%sRESULTS%s" % (tracker.get_color(tracker.RED), tracker.end_color())
    else:
        label = "RESULTS"

    tracker.print_operation(label, "Ran %d test%s." % (testsrun, plural(testsrun)))

    if testsrun == 0:
        tracker.print_notice("No tests were run.")
        return

    if tracker.config['fail-fast']:
        if passed == -1:
            tracker.print_operation(label, "A test failed, so the suite was aborted.")
        else:
            tracker.print_operation(label, "All tests passed.")
    else:

        tracker.print_operation(label,
                "%d / %d (%.1f%%) of tests passed." %
                (passed, testsrun, 100.0 * passed / testsrun))

    if passed < testcount and tracker.config['failed-test-log']:
        tracker.print_notice("A report for failed tests was written in \"%s\"." % \
                os.path.abspath(tracker.config['failed-test-log']))


### Helper functions ###
def plural(num):
    return '' if num == 1 else 's'


def skip_test(test, ignore):
    return test in ignore or \
           test[:-5] in ignore or \
           os.path.basename(test) in ignore or \
           os.path.basename(test[:-5]) in ignore


def get_boolean_option(tracker, filename, string):
    string = string.lower()
    if string in ('true', 'yes', 'enable', 'enabled', 'set', '1'):
        return True
    elif string in ('false', 'no', 'disable', 'disabled', 'unset', '0'):
        return False
    else:
        tracker.print_error('%s: Unknown boolean value: \'%s\'.' % (filename, string))
        tracker.failure()
        return None

