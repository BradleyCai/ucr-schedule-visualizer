"""
This modules loads a JSON file from the etc/ directory and provides it as a
Python dictionary for other scripts to utilize.
"""

from __future__ import with_statement

import json
import os


def json2py(data):
    if isinstance(data, dict):
        return {json2py(key): json2py(data) for key, data in data.items()}
    elif isinstance(data, list):
        return [json2py(element) for element in data]
    else:
        return data


def load(fn):
    old_cwd = os.getcwd()
    if os.path.isdir("../etc"):
        os.chdir("../etc")
    elif os.path.isdir("./etc"):
        os.chdir("./etc")

    with open(fn, 'r') as fh:
        try:
            raw = json.load(fh)
        except json.decoder.JSONDecodeError as err:
            print("Unable to read config file \"%s\": %s" % (fn, err))
            exit(1)

    os.chdir(old_cwd)
    return json2py(raw)


def sanity_check(dict, fields):
    for field, ftype in fields.items():
        if field not in dict.keys():
            print("Config file does not have a \"%s\" value." % field)
            exit(1)
        elif type(ftype) == dict:
            sanity_check(field, ftype)
        elif type(dict[field]) != ftype:
            # Unicode literals are a special case
            if (type(dict[field]) == unicode and ftype == str):
                continue

            print("Config file has invalid type for \"%s\": %s (expected %s)." %
                  (field, type(dict[field]), ftype))
            exit(1)
