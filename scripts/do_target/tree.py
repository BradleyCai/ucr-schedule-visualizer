# Copyright (C) 2015-2016 Ammon Smith and Bradley Cai
# Available for use under the terms of the MIT License.

__all__ = [
    "Tree",

    "TRUNK",
    "INTERSECTION",
    "BRANCH",
    "CORNER",
    "ASCII_TRUNK",
    "ASCII_INTERSECTION",
    "ASCII_BRANCH",
    "ASCII_CORNER",
]

TRUNK = "\xe2\x94\x82"
INTERSECTION = "\xe2\x94\x9c"
BRANCH = "\xe2\x94\x80"
CORNER = "\xe2\x94\x94"

ASCII_TRUNK = "|"
ASCII_INTERSECTION = "|"
ASCII_BRANCH = "-"
ASCII_CORNER = "`"


class Tree(object):
    def __init__(self, root, children):
        # Children in form {child: {grandchildren}}
        self.root = root
        self.children = children

    def display(self, use_ascii=False):
        print(self.root)

        if use_ascii:
            character_set = {
                "trunk": ASCII_TRUNK,
                "intersect": ASCII_INTERSECTION,
                "branch": ASCII_BRANCH,
                "corner": ASCII_CORNER,
            }
        else:
            character_set = {
                "trunk": TRUNK,
                "intersect": INTERSECTION,
                "branch": BRANCH,
                "corner": CORNER,
            }

        self.display_subtree(self.children, [], character_set)

    def display_subtree(self, children, level, charset):
        child_list = list(children.keys())
        child_list.sort()

        for i in range(len(child_list)):
            notlast = (i < len(child_list) - 1)

            if notlast:
                corner = charset["intersect"]
            else:
                corner = charset["corner"]

            child = child_list[i]
            print("%s%s%s %s" %
                    (self.get_indent(level, charset["trunk"]), corner, charset["branch"], child))

            if children[child]:
                self.display_subtree(children[child], level + [notlast], charset)

    def get_indent(self, level, trunk):
        separator = []

        for active in level:
            if active:
                separator.append("%s  " % trunk)
            else:
                separator.append("    ")

        return "".join(separator)

