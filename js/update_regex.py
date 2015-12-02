#!/usr/bin/python
from __future__ import with_statement
import re, sys

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: update_regex.py field-name input-file output-file [flags]")
        exit(1)

    field = sys.argv[1]

    with open(sys.argv[2], 'r') as fh:
        to_replace = fh.read()

    with open(sys.argv[3], 'r') as fh:
        output_text = fh.read()

    if len(sys.argv) > 4:
        flags = sys.argv[4]
    else:
        flags = "g"

    to_replace = to_replace.replace("\\n", "\\\\n").strip()

    output_text = \
        re.sub(r"this\.%s\s*=\s*\/.*\/%s;" % (re.escape(field), flags), \
               "this.%s = /%s/%s;" % (field, to_replace, flags), \
               output_text)
     
    with open(sys.argv[3], 'w+') as fh:
        fh.write(output_text)


