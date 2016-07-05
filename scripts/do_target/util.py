# Copyright (C) 2015-2016 Ammon Smith and Bradley Cai
# Available for use under the terms of the MIT License.

__all__ = [
    "print_success",
    "print_failure",
]


def print_success(target, usecolor, elapsed):
    if usecolor:
        start_color = "\033[32m"
        end_color = "\033[0m"
    else:
        start_color = ""
        end_color = ""

    print("%sTarget \"%s\" ran successfully in %.4f seconds.%s" %
            (start_color, target, elapsed, end_color))


def print_failure(target, usecolor, ending):
    if usecolor:
        start_color = "\033[31m"
        end_color = "\033[0m"
    else:
        start_color = ""
        end_color = ""

    print("%sTarget \"%s\" was unsuccessful%s%s" %
            (start_color, target, ending, end_color))


