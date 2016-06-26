#!/usr/bin/env python
"""
System to "compile" regular expressions.

DEPRECATED, use do.py with targets instead
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

# Build goals
def target_regex(args, config):
    global DEPTH

    # Change directory to compile
    directory = os.path.join(os.path.dirname(sys.argv[0]), "..", config["regex-directory"])
    print("Switching directory to \"%s\"..." % directory)
    os.chdir(directory)

    # Compile regular expressions
    print("Compiling regex sources...")
    DEPTH += 1
    if not config["source-files"]:
        print("%s(nothing to do)" % (' ' * DEPTH))
    for source in config["source-files"]:
        compile_regex(source, args.dontoverwrite)
    DEPTH -= 1

    # Copy *.out files
    print("Copying compiled regex artifacts...")
    DEPTH += 1
    files = glob.iglob("*.out")
    if not files:
        print("%s(nothing to do)" % (' ' * DEPTH))
    for fn in files:
        for directory in config["copy-to"]:
            dest = os.path.join(directory, fn)
            print("%s[CP] %s -> %s" % (' ' * DEPTH, fn, dest))
            shutil.copy(fn, dest)
    DEPTH -= 1

    # Inject regular expressions in to the Javascript
    print("Injecting compiled regex artifacts...")
    DEPTH += 1
    if not config["to-inject"]:
        print("%s(nothing to do)" % (' ' * DEPTH))
    for fn, field in config["to-inject"].items():
        inject_regex(field, fn, config["inject-file"])
    DEPTH -= 1


def target_clean(args, config):
    global DEPTH

    pass


DEPTH = 0

TARGETS = {
    "default": target_regex,
    "regex": target_regex,
    "clean": target_clean,
}


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
    global DEPTH

    print("%s[DEP] %s" % (' ' * DEPTH, source))
    body = read_file(source)
    for depend in set(DEPENDENCY_REGEX.findall(body)):
        depend = DEPENDENCY_NAME_REGEX.match(depend).group(1)
        if depend not in depends.keys():
            depends[depend] = combine_regex(depend + ".regex", depends)
        body = body.replace("%%{%s}" % depend, depends[depend])
    return body.rstrip()


# Main functions
def compile_regex(name, dont_overwrite=False):
    global DEPTH

    print("%s[RE] %s" % (' ' * DEPTH, name))
    if name.endswith(".regex"):
        source = name
        target = name[:-6] + ".out"
    else:
        source = name + ".regex"
        target = name + ".out"

    DEPTH += 1
    try:
        compiled = combine_regex(source)
    except IOError as err:
        print("Unable to open \"%s\": %s" % (source, err))
        exit(1)
    DEPTH -= 1

    if os.path.exists(target) and dont_overwrite:
        print("\"%s\" already exists, not overwriting." % target)
        exit(1)

    try:
        write_to_file(target, compiled)
    except IOError as err:
        print("Unable to write to \"%s\": %s" % (target, err))
        exit(1)


def inject_regex(field_name, input_file, output_file):
    global DEPTH

    print("%s[INJ] %s:%s <- %s" % (' ' * DEPTH, output_file, field_name, input_file))

    to_replace = read_file(input_file).replace(r"\n", r"\\n").strip()
    output_text = read_file(output_file).rstrip()

    output_text = \
        re.sub(r"this\.%s\s*=\s*\/.*\/g;" % re.escape(field_name),
               "this.%s = /%s/g;" % (field_name, to_replace),
               output_text)

    write_to_file(output_file, output_text)


if __name__ == "__main__":
    # Get command-line arguments
    argparser = argparse.ArgumentParser(description=
            "Compile the regular expressions and inject the results into JavaScript sources.")
    argparser.add_argument("-c", "--config", nargs='?', default="build-config.json", help=\
            "Which Python configuration file to use. (default: config)")
    argparser.add_argument("-n", "--no-clobber", dest="dontoverwrite", action="store_true", help=\
            "Quit with an error instead of overwriting files.")
    argparser.add_argument("target", nargs='?', default="default", help=\
            "What build goal to execute.")
    args = argparser.parse_args(sys.argv[1:])
    config = jsonconfig.load(args.config)
    jsonconfig.sanity_check(config, CONFIG_FIELDS)

    target = TARGETS.get(args.target)
    if not target:
        print("No such build target: %s." % target)
        exit(1)

    start_time = time.time()
    target(args, config)
    print("Built target \"%s\" in %.4f seconds." % (args.target, time.time() - start_time))

