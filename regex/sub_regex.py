#!/usr/bin/env python
from __future__ import with_statement
import re, sys, time, os

NEEDS_COMPILE = re.compile(r".*%\{.*\}.*")

def regex_compile(source):
    files = os.walk(".").next()[2]
    for fn in files:
        parts = fn.split('.')

        if parts[-1].lower() == "re" or parts[-1].lower() == "regex":
            pattern = "%%{%s}" % ('.'.join(parts[:-1]))

            if not pattern in source:
                continue

            with open(fn, 'r') as fh:
                regex = fh.read()

                if NEEDS_COMPILE.match(regex):
                    regex = regex_compile(regex)

                if regex and regex[-1] == '\n':
                    regex = regex[:-1]

                try:
                    re.compile(regex)
                except StandardError as err:
                    print("Invalid regex in %s: %s" % (fn, err))
                    exit(1)

            source = source.replace(pattern, regex)
    return source

if __name__ == "__main__":
    start = time.time()

    if len(sys.argv) > 2:
        source = sys.argv[1]
        target = sys.argv[2]
    elif len(sys.argv) > 1:
        source = sys.argv[1]
        target = "master.out"
    else:
        source = "master.regex"
        target = "master.out"

    with open(source, 'r') as fh:
        regex = regex_compile(fh.read())

    if os.path.exists(target):
        print("warn: Overwriting %s..." % target)

    with open(target, 'w+') as fh:
        fh.write(regex)

    print("Compilation of %s finished in %.3f seconds." % (target, time.time() - start))

