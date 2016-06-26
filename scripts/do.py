#!/usr/bin/env python

from __future__ import print_function

import argparse
import os
import sys
import time

try:
    import jsonconfig
except ImportError:
    print("Cannot local modules. Are you in the right directory?")
    exit(1)

DEFAULT_TARGET = "regex"

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
    argparser.add_argument("target", nargs='?', default=DEFAULT_TARGET, help=\
            "What build goal to execute.")
    args = argparser.parse_args(sys.argv[1:])

    # Switch directory to where the targets are
    os.chdir(os.path.dirname(sys.argv[0]))

    # Load the target module
    try:
        module = __import__("target_" + args.target)
    except ImportError:
        print("No such build target: %s." % args.target)
        exit(1)

    if module.config_fields:
        # Load the configuration
        if args.config:
            config = jsonconfig.load(args.config)
        else:
            config = jsonconfig.load("%s-config.json" % args.target)

        # Check the configuration
        jsonconfig.sanity_check(config, module.config_fields)
    else:
        config = {}

    # Run target
    start_time = time.time()
    module.run(args, config)
    print("Ran target \"%s\" in %.4f seconds." % (args.target, time.time() - start_time))

