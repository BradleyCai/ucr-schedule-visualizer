#!/usr/bin/env python
"""
The purpose of this script is to 'compile' the regular expressions
found in the regex/ directory and inject them into their respective
Javascript sources in the js/ directory. This is done by invoking a
Python script in regex/ that combines multiple *.regex files into
'compiled' *.out files. The purpose of this is to break down these
long and complicated regular expressions into more meaningful parts,
which can be fixed easier.  This means that whenever you need to
modify a regular expression, you should only modify the *.regex files
in regex/. The *.out files or the regular expressions in the javascript
sources should not be modified, as they will be overwritten.
"""

from __future__ import print_function, with_statement

import argparse
import glob
import os
import re
import shutil
import sys
import time

try:
    import jsonconfig
except ImportError:
    print("Cannot local modules. Are you in the right directory?")
    exit(1)

CONFIG_FIELDS = {
    "source-files": list,
    "regex-directory": str,
    "copy-to": list,
    "inject-file": str,
    "to-inject": dict,
}

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
        write_to_file(target, compiled)
    except IOError as err:
        print("Unable to write to \"%s\": %s" % (target, err))
        exit(1)


def inject_regex(field_name, input_file, output_file):
    print(" [INJ] %s:%s <- %s" % (output_file, field_name, input_file))

    to_replace = read_file(input_file).replace(r"\n", r"\\n").strip()
    output_text = read_file(output_file).rstrip()

    output_text = \
        re.sub(r"this\.%s\s*=\s*\/.*\/g;" % re.escape(field_name),
               "this.%s = /%s/g;" % (field_name, to_replace),
               output_text)

    write_to_file(output_file, output_text)


if __name__ == "__main__":
    start_time = time.time()

    # Get command-line arguments
    argparser = argparse.ArgumentParser(description=
            "Compile the regular expressions and inject the results into JavaScript sources.")
    argparser.add_argument("-c", "--config", nargs='?', default="build-config.json", help=
            "Which Python configuration file to use. (default: config)")
    argparser.add_argument("-n", "--no-clobber", dest="dontoverwrite", action="store_true", help=\
            "Quit with an error instead of overwriting files.")
    args = argparser.parse_args(sys.argv[1:])
    config = jsonconfig.load(args.config)
    jsonconfig.sanity_check(config, CONFIG_FIELDS)

    # Change directory to compile
    directory = os.path.join(os.path.dirname(sys.argv[0]), config["regex-directory"])
    print("Switching directory to \"%s\"..." % directory)
    try:
        os.chdir(directory)
    except FileNotFoundError:
        os.chdir(os.path.join("..", directory))

    # Compile regular expressions
    print("Compiling regex sources...")
    if not config["source-files"]:
        print(" (nothing to do)")
    for source in config["source-files"]:
        compile_regex(source, args.dontoverwrite)

    # Copy *.out files
    print("Copying compiled regex artifacts...")
    files = glob.iglob("*.out")
    if not files:
        print(" (nothing to do)")
    for fn in files:
        for directory in config["copy-to"]:
            dest = os.path.join(directory, fn)
            print(" [CP] %s -> %s" % (fn, dest))
            shutil.copy(fn, dest)

    # Inject regular expressions in to the Javascript
    print("Injecting compiled regex artifacts...")
    if not config["to-inject"]:
        print(" (nothing to do)")
    for fn, field in config["to-inject"].items():
        inject_regex(field, fn, config["inject-file"])

    # Report elapsed time
    print("Finished in %.4f seconds." % (time.time() - start_time))

