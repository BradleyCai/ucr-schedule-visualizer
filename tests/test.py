#!/usr/bin/python
import argparse, json, re, sys

class TestFailed(RuntimeError):
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
                raise TestFailed(self.name)

def byteify(data):
    if isinstance(data, dict):
        return { byteify(key) : byteify(data) for key, data in data.iteritems() }
    elif isinstance(data, list):
        return [ byteify(element) for element in data ]
    elif isinstance(data, unicode):
        return data.encode("utf-8")
    else:
        return data

def sanity_check(config):
    def valid_regex(data):
        if not data.has_key("file") and not isinstance(config["file"], str):
            print("'file' property is missing or not a string.")
            return False
        if not data.has_key("groups"):
            print("'groups' property is missing.")
            return False
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

    if not config.has_key("regex") or not isinstance(config["regex"], dict):
        print("Missing or malformed 'regex' property.")
        return False
    if not valid_regex(config["regex"]):
        return False

    return True

if __name__ == "__main__":
    # Parse command line arguments
    argparser = argparse.ArgumentParser(description="Test regular expressions to make sure they perform as expected.")
    argparser.add_argument("-c", "--config-file", nargs=1, type=open, help="Specify the configuration file to use when running tests.")
    argparser.add_argument("-F", "--fail-fast", action="store_true", help="Specifies that testing should terminate when a test fails.")
    argparser.add_argument("test file", nargs='+', type=open, help="The *.test files that describe the tests to be performed.")
    args = argparser.parse_args(sys.argv[1:])

    # Parse config file
    config = byteify(json.loads(args.config_file[0].read()))
    if not sanity_check(config):
        print("Errors parsing configuration file.")
        exit(1)

    # Generate list of tests
    tests = []
    TEST_FILE_REGEX = re.compile(r"(?:%%%|!!!) *(.*)\n(?:.|\n)*?)~~~")
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

    
