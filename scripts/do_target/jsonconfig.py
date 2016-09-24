# Copyright (C) 2015-2016 Ammon Smith and Bradley Cai
# Available for use under the terms of the MIT License.

"""
This modules loads a JSON file from the etc/ directory and provides it as a
Python dictionary for other scripts to utilize.
"""

__all__ = [
    'json2py',
    'load',
    'sanity_check',

    'CONFIG_DIRECTORY',
]

import json
import os

CONFIG_DIRECTORY = 'etc'

def json2py(data):
    if isinstance(data, dict):
        return {json2py(key): json2py(data) for key, data in data.items()}
    elif isinstance(data, list):
        return [json2py(element) for element in data]
    else:
        return data


def load(filename):
    old_cwd = os.getcwd()

    for directory in ('../%s', './%s'):
        directory = directory % CONFIG_DIRECTORY
        if os.path.isdir(directory):
            os.chdir(directory)
            break

    with open(filename, 'r') as fh:
        try:
            raw = json.load(fh)
        except json.decoder.JSONDecodeError as err:
            print("Unable to read config file \"%s\": %s" % (filename, err))
            return None

    os.chdir(old_cwd)
    dictionary = json2py(raw)
    dictionary["filename"] = filename
    return dictionary


def sanity_check(dictionary, fields):
    success = True

    for field, ftype in fields.items():
        if field not in dictionary.keys():
            print("%s: Config file does not have a \"%s\" value." % (dictionary['filename'], field))
            success = False
        elif type(ftype) == dictionary:
            success &= sanity_check(field, ftype)
        else:
            try:
                if type(dictionary[field]) not in ftype:
                    print("%s: Config file has invalid type for \"%s\": %s (expected one of %s)." %
                          (dictionary['filename'], field, type(dictionary[field]), ", ".join(ftype)))
                    success = False
            except:
                if type(dictionary[field]) != ftype:
                    print("%s: Config file has invalid type for \"%s\": %s (expected %s)." %
                          (dictionary['filename'], field, type(dictionary[field]), ftype))
                    success = False

    if not success:
        exit(1)

