# Copyright (C) 2015-2016 Ammon Smith and Bradley Cai
# Available for use under the terms of the MIT License.

__all__ = [
    'Tree',

    'TRUNK',
    'INTERSECTION',
    'BRANCH',
    'CORNER',
    'ASCII_TRUNK',
    'ASCII_INTERSECTION',
    'ASCII_BRANCH',
    'ASCII_CORNER',
]

TRUNK = b'\xe2\x94\x82'.decode('utf-8')
INTERSECTION = b'\xe2\x94\x9c'.decode('utf-8')
BRANCH = b'\xe2\x94\x80'.decode('utf-8')
CORNER = b'\xe2\x94\x94'.decode('utf-8')

ASCII_TRUNK = '|'
ASCII_INTERSECTION = '|'
ASCII_BRANCH = '-'
ASCII_CORNER = '`'


class Tree(object):
    def __init__(self, root, children):
        # Children in form {child: {grandchildren}}
        self.root = root
        self.children = children

    def display(self, use_ascii=False, bullet=""):
        print("%s%s" % (bullet, self.root))

        if use_ascii:
            character_set = {
                'trunk': ASCII_TRUNK,
                'intersect': ASCII_INTERSECTION,
                'branch': ASCII_BRANCH,
                'corner': ASCII_CORNER,
            }
        else:
            character_set = {
                'trunk': TRUNK,
                'intersect': INTERSECTION,
                'branch': BRANCH,
                'corner': CORNER,
            }

        self.display_subtree(self.children, [], character_set, bullet)

    def display_subtree(self, children, level, charset, bullet):
        child_list = list(children.keys())
        child_list.sort()

        for i in range(len(child_list)):
            notlast = (i < len(child_list) - 1)

            if notlast:
                corner = charset['intersect']
            else:
                corner = charset['corner']

            child = child_list[i]
            print("%s%s%s %s" %
                    (self.get_indent(level, charset['trunk'], bullet), corner, charset['branch'], child))

            if children[child]:
                self.display_subtree(children[child], level + [notlast], charset)

    @staticmethod
    def get_indent(level, trunk, bullet):
        separator = [' ' * len(bullet)]

        for active in level:
            if active:
                separator.append("%s  " % trunk)
            else:
                separator.append("    ")

        return ''.join(separator)

