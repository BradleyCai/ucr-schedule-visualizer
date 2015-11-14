#!/usr/bin/python
import argparse, re, sys

class TestFailed(RuntimeError):
    pass

class TestConfig(object):
    def __init__(self, config):
        pass

class Test(object):
    def __init__(self, config, name, input, output):
        self.config = config
        self.name = name
        self.input = input
        self.output = output
    def __call__(self):
        for regex in self.config:
            result = regex.match(self.input)
            if (result == None) or (result.groups() != self.output):
                raise TestFailed

if __name__ == "__main__":
    # Parse command line arguments
    argparser = argparse.ArgumentParser(description="Test regular expressions to make sure they perform as expected.")
    argparser.add_argument("-c", "--config-file", nargs=1, type=open, help="Specify the configuration file to use when running tests.")
    argparser.add_argument("-F", "--fail-fast", action="store_true", help="Specifies that testing should terminate when a test fails.")
    argparser.add_argument("test file", nargs='+', type=open, help="The *.test files that describe the tests to be performed.")
    args = argparser.parse_args(sys.argv[1:])

    # Parse config file
    config = TestConfig(args.config_file[0].read())

    # Generate list of tests
    tests = []
    TEST_FILE_REGEX = re.compile(r"(?:%%%|!!!) *(.*)\n(.*?)", re.DOTALL)
    for fh in args.test_file:
        match = TEST_FILE_REGEX.match(fh.read())



    # Perform all the tests
    if args.fail_fast:
        for test in tests:
            if not test():
                break
    else:
        for test in tests:
            test()

    
