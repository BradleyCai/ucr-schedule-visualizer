# Copyright (C) 2015-2016 Ammon Smith and Bradley Cai
# Available for use under the terms of the MIT License.

"""
This modules loads a JSON file from the etc/ directory and provides it as a
Python dictionary for other scripts to utilize.
"""

import json
import os

CONFIG_DIRECTORY = "etc"

def json2py(data):
    if isinstance(data, dict):
        return {json2py(key): json2py(data) for key, data in data.items()}
    elif isinstance(data, list):
        return [json2py(element) for element in data]
    else:
        return data


def load(fn):
    old_cwd = os.getcwd()

    for directory in ("../%s", "./%s"):
        directory = directory % CONFIG_DIRECTORY
        if os.path.isdir(directory):
            os.chdir(directory)
            break

    with open(fn, 'r') as fh:
        try:
            raw = json.load(fh)
        except json.decoder.JSONDecodeError as err:
            print("Unable to read config file \"%s\": %s" % (fn, err))
            return None

    os.chdir(old_cwd)
    return json2py(raw)


def sanity_check(dictionary, fields):
    success = True

    for field, ftype in fields.items():
        if field not in dictionary.keys():
            print("Config file does not have a \"%s\" value." % field)
            success = False
        elif type(ftype) == dictionary:
            success &= sanity_check(field, ftype)
        elif type(dictionary[field]) != ftype:
            # Unicode literals are a special case
            if (type(dictionary[field]) == unicode and ftype == str):
                continue

            print("Config file has invalid type for \"%s\": %s (expected %s)." %
                  (field, type(dictionary[field]), ftype))
            return False

