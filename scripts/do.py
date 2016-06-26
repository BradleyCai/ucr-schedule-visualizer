#!/usr/bin/env python

from __future__ import print_function

import argparse
import os
import sys
import time
import traceback

try:
    import jsonconfig
except ImportError:
    print("Cannot local modules. Are you in the right directory?")
    exit(1)

DEFAULT_TARGET = "regex"


def print_success(target, usecolor, elapsed):
    if usecolor:
        start_color = "\033[32m"
        end_color = "\033[0m"
    else:
        start_color = ""
        end_color = ""

    print("%sRan target \"%s\" in %.4f seconds.%s" %
            (start_color, target, elapsed, end_color))


def print_failure(target, usecolor, ending):
    if usecolor:
        start_color = "\033[31m"
        end_color = "\033[0m"
    else:
        start_color = ""
        end_color = ""

    print("%sTarget \"%s\" did not complete successfully%s%s" %
            (start_color, target, ending, end_color))

if __name__ == "__main__":
    # Get command line arguments
    argparser = argparse.ArgumentParser(description=
            "Compile the regular expressions and inject the results into JavaScript sources.")
    argparser.add_argument("-c", "--config", nargs='?', help=\
            "Specify a certain configuration file to use.")
    argparser.add_argument("-n", "--no-clobber", dest="dontoverwrite", action="store_true", help=\
            "Quit with an error instead of overwriting files.")
    argparser.add_argument("-N", "--no-color", dest="usecolor", action="store_false", help=\
            "Use to disable colored text output.")
    argparser.add_argument("target", nargs='*', default=[DEFAULT_TARGET], help=\
            "What build goal to execute.")
    args = argparser.parse_args(sys.argv[1:])

    ret = 0
    for target in args.target:
        # Switch directory to where the targets are
        os.chdir(os.path.dirname(sys.argv[0]))

        # Load the target module
        try:
            module = __import__("target_%s" % target)
        except ImportError:
            print("No such build target: %s" % target)
            exit(1)

        if module.config_fields:
            # Load the configuration
            if args.config:
                config = jsonconfig.load(args.config)
            else:
                config = jsonconfig.load("%s-config.json" % target)

            # Check the configuration
            jsonconfig.sanity_check(config, module.config_fields)
        else:
            config = {}

        # Run target
        start_time = time.time()
        try:
            process = module.run(args, config)
            if not process.successful:
                raise SystemExit
        except SystemExit:
            print_failure(target, args.usecolor, ".")
            ret += 1
        except:
            print_failure(target, args.usecolor, ":")
            traceback.print_exc()
            ret += 1
        else:
            print_success(target, args.usecolor, time.time() - start_time)

    exit(ret)

