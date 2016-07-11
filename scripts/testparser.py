"""
A parser that turns .test files into dictionaries with their corresponding
data items.
"""

from __future__ import print_function, with_statement
import re


COMMENT_REGEX = re.compile(r";.*", re.DOTALL)
SINGLE_LINE_TAG_REGEX = re.compile(r"\s*\[([a-zA-Z0-9]+)\]\s*(.+)", re.DOTALL)
OPEN_TAG_REGEX = re.compile(r"\s*\[([a-zA-Z0-9]+)\]\s*")
CLOSE_TAG_REGEX = re.compile(r"\s*\[/([a-zA-Z0-9]+)\]\s*")


class TestParser(object):
    def __init__(self):
        self.data = {}
        self.current_tag = None
        self.buffer = []

    def reset(self):
        self.data = {}
        self.current_tag = None
        self.buffer = []

    def parse(self, filename, lines):
        self.data["filename"] = filename

        lineno = 1
        for line in lines:
            line = line.rstrip()
            if self.current_tag:
                tag = self.get_close_tag(line)
                if tag is None:
                    self.check_buffer(filename, lineno, line)
                    self.buffer.append(line)
                elif tag == self.current_tag:
                    self.add_tag(tag, "\n".join(self.buffer))
                else:
                    print("%s:%d: Closing tag is \"%s\", expected \"%s\"." %
                          (filename, lineno, tag, self.current_tag))
                    exit(1)
            elif not self.ignore(line):
                tag, content = self.get_single_line_tag(line)

                if tag:
                    self.add_tag(tag, content)
                else:
                    tag = self.get_open_tag(line)

                    if tag:
                        self.buffer = []
                        self.current_tag = tag
                    else:
                        print("%s:%d: Invalid syntax." % (filename, lineno))

            lineno += 1
        data = self.data
        self.reset()
        return data

    def add_tag(self, tag, content):
        if tag in self.data.keys():
            self.data[tag].append(content)
        else:
            self.data[tag] = [content]
        self.current_tag = None

    def check_buffer(self, filename, lineno, line):
        tag, content = self.get_single_line_tag(line)
        if tag:
            print("%s:%d Embedded tag detected, \"%s\" inside \"%s\"." %
                  (filename, lineno, tag, self.current_tag))
            exit(1)

        tag = self.get_open_tag(line)
        if tag:
            print("%s:%d: Embedded tag detected, \"%s\" inside \"%s\"." %
                  (filename, lineno, tag, self.current_tag))
            exit(1)

        tag = self.ignore(line)
        if tag and line:
            print("%s:%d: Warning: treating comment-like line as text." % (filename, lineno))

    @staticmethod
    def ignore(line):
        line = line.lstrip()
        return (not line) or COMMENT_REGEX.match(line)

    @staticmethod
    def get_single_line_tag(line):
        match = SINGLE_LINE_TAG_REGEX.match(line)
        return match.groups() if match else (None, None)

    @staticmethod
    def get_open_tag(line):
        match = OPEN_TAG_REGEX.match(line)
        return match.group(1) if match else None

    @staticmethod
    def get_close_tag(line):
        match = CLOSE_TAG_REGEX.match(line)
        return match.group(1) if match else None



