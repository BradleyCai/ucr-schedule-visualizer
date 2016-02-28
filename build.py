#!/usr/bin/env python
# The purpose of this script is to 'compile' the regular expressions
# found in the regex/ directory and inject them into their respective
# Javascript sources in the js/ directory. This is done by invoking a
# Python script in regex/ that combines multiple *.regex files into
# 'compiled' *.out files. The purpose of this is to break down these
# long and complicated regular expressions into more meaningful parts,
# which can be fixed easier.  This means that whenever you need to
# modify a regular epxression, you should only modify the *.regex files
# in regex/. The *.out files or the regular expressions in the javascript
# sources should not be modified, as they will be overwritten.

from __future__ import print_function, with_statement
import argparse
import glob
import os
import re
import shutil
import sys
import time

DEPENDENCY_REGEX = re.compile(r"%\{.*?\}")
DEPENDENCY_NAME_REGEX = re.compile(r"%\{(.*?)\}")

# Helper functions
def read_file(fn):
    with open(fn, 'r') as fh:
        return fh.read()


def write_to_file(fn, contents):
    with open(fn, 'w+') as fh:
        fh.write(contents)


def get_file_list(path):
    gen = os.walk(path)

    if hasattr(gen, "next"):
        return gen.next()[2]
    else:
        return gen.__next__()[2]


def combine_regex(source, depends={}):
    print("  [DEP] %s" % source)
    body = read_file(source)
    for depend in set(DEPENDENCY_REGEX.findall(body)):
        depend = DEPENDENCY_NAME_REGEX.match(depend).group(1)
        if depend not in depends.keys():
            depends[depend] = combine_regex(depend + ".regex", depends)
        body = body.replace("%%{%s}" % depend, depends[depend])
    return body.rstrip()


# Main functions
def compile_regex(name, dont_overwrite=False):
    print(" [CC] %s" % name)
    if name.endswith(".regex"):
        source = name
        target = name[:-6] + ".out"
    else:
        source = name + ".regex"
        target = name + ".out"

    try:
        compiled = combine_regex(source)
    except IOError as err:
        print("Unable to open \"%s\": %s" % (source, err))
        exit(1)

    if os.path.exists(target) and dont_overwrite:
        print("\"%s\" already exists, not overwriting." % target)
        exit(1)

    try:
        write_to_file(target + "\n", compiled)
    except IOError as err:
        print("Unable to write to \"%s\": %s" % (target, err))
        exit(1)


def inject_regex(field_name, input_file, output_file):
    print(" [INJ] %s:%s <- %s" % (output_file, field_name, input_file))

    to_replace = read_file(input_file).replace(r"\n", r"\\n").strip()
    output_text = read_file(output_file).rstrip()

    output_text = \
        re.sub(r"this\.%s\s*=\s*\/.*\/g;" % re.escape(field_name), \
               "this.%s = /%s/g;" % (field_name, to_replace), \
               output_text)

    write_to_file(output_file, output_text)


if __name__ == "__main__":
    start_time = time.time()

    # Get command-line arguments
    argparser = argparse.ArgumentParser(description=\
            "Compile the regular expressions and inject the results into JavaScript sources.")
    argparser.add_argument("-c", "--config", nargs='?', default="config", help=\
            "Which Python configuration file to use. (default: config)")
    argparser.add_argument("-n", "--no-clobber", dest="dontoverwrite", action="store_true", help=\
            "Quit with an error instead of overwriting files.")
    args = argparser.parse_args(sys.argv[1:])

    try:
        config = __import__(args.config)
    except ImportError as err:
        print("Unable to load config file \"%s\": %s" % (args.config, err))
        exit(1)

    # Change directory to compile
    directory = os.path.join(os.path.dirname(sys.argv[0]), config.REGEX_DIRECTORY)
    print("Switching directory to \"%s\"..." % directory)
    os.chdir(directory)

    # Compile regular expressions
    print("Compiling regex sources...")
    if not config.SOURCE_FILES:
        print(" (nothing to do)")
    for source in config.SOURCE_FILES:
        compile_regex(source, args.dontoverwrite)

    # Copy *.out files
    print("Copying compiled regex artifacts...")
    files = glob.iglob("*.out")
    if not files:
        print(" (nothing to do)")
    for fn in files:
        for directory in config.COPY_TO:
            dest = os.path.join(directory, fn)
            print(" [CP] %s -> %s" % (fn, dest))
            shutil.copy(fn, dest)

    # Change directory to inject
    os.chdir(config.INJECT_DIRECTORY)

    # Inject regular expressions in to the Javascript
    print("Injecting compiled regex artifacts...")
    if not config.TO_INJECT:
        print(" (nothing to do)")
    for fn, field in config.TO_INJECT.items():
        inject_regex(field, fn, config.INJECT_FILE)

    # Report elapsed time
    print("Finished in %.4f seconds." % (time.time() - start_time))

