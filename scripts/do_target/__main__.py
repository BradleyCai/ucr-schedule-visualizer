# Copyright (C) 2015-2016 Ammon Smith and Bradley Cai
# Available for use under the terms of the MIT License.

from . import dependencies
from . import jsonconfig
from . import targetobj
from .static import PROGRAM_NAME
from .util import print_success, print_failure

import argparse
import os
import sys
import time
import traceback


def main(argv=None):
    # Get command line arguments
    argparser = argparse.ArgumentParser(description=
            "Run builds by writing target modules.")
    argparser.add_argument("-c", "--config", nargs='?', help=\
            "Specify a certain configuration file to use.")
    argparser.add_argument("-d", "--config-directory", nargs='?', help=\
            "Specify which directory to look for config files in. (Ignored if -c is set).")
    argparser.add_argument("-n", "--no-clobber", dest="dontoverwrite", action="store_true", help=\
            "Quit with an error instead of overwriting files.")
    argparser.add_argument("-N", "--no-color", dest="usecolor", action="store_false", help=\
            "Use to disable colored text output.")
    argparser.add_argument("-v", "--verbose", action="store_true", help=\
            "Print detailed information when running.")
    argparser.add_argument("target", nargs='*', help=\
            "What build goal to execute.")
    args = argparser.parse_args((sys.argv if argv is None else argv)[1:])

    if not args.target:
        print("%s: No targets specified.\nUse the \"--help\" option if you're lost." %
                PROGRAM_NAME)
        exit(1)

    if args.config_directory:
        jsonconfig.CONFIG_DIRECTORY = args.config_directory

    # Switch directory to where the targets are
    os.chdir(os.path.join(os.path.dirname(sys.argv[0]), ".."))

    # Determine build order
    targets = dependencies.resolve_full_build_order(args.target, args.verbose)

    # Run the targets
    ret = 0
    for target in targets:
        if target.config_fields:
            # Load the configuration
            if args.config:
                config = jsonconfig.load(args.config)
            else:
                config = jsonconfig.load("%s-config.json" % target.name)

            # Check the configuration
            jsonconfig.sanity_check(config, target.config_fields)
        else:
            config = {}

        # Create target tracker
        tracker = targetobj.TargetTracker(args, config)

        # Run target
        start_time = time.time()
        try:
            target.run(tracker)
            if not tracker.successful:
                raise SystemExit
        except SystemExit:
            print_failure(target.name, args.usecolor, ".")
            ret += 1
        except:
            print_failure(target.name, args.usecolor, ":")
            traceback.print_exc()
            ret += 1
        else:
            print_success(target.name, args.usecolor, time.time() - start_time)

    exit(ret)


if __name__ == "__main__":
    main()

