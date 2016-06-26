__all__ = [
    "TargetProcess",
    "BLACK",
    "RED",
    "GREEN",
    "YELLOW",
    "BLUE",
    "MAGENTA",
    "CYAN",
    "WHITE",
    "BLACK_BOLD",
    "RED_BOLD",
    "GREEN_BOLD",
    "YELLOW_BOLD",
    "BLUE_BOLD",
    "MAGENTA_BOLD",
    "CYAN_BOLD",
    "WHITE_BOLD",
]

BLACK = "30"
RED = "31"
GREEN = "32"
YELLOW = "33"
BLUE = "34"
MAGENTA = "35"
CYAN = "36"
WHITE = "37"

BLACK_BOLD = "30;1"
RED_BOLD = "31;1"
GREEN_BOLD = "32;1"
YELLOW_BOLD = "33;1"
BLUE_BOLD = "34;1"
MAGENTA_BOLD = "35;1"
CYAN_BOLD = "36;1"
WHITE_BOLD = "37;1"


class TargetProcess(object):
    def __init__(self, args, config):
        self.args = args
        self.config = config
        self.depth = 0
        self.successful = True

    def failiure(self):
        self.successful = False

    def run_job(self, job, description, *extra_args):
        if description:
            self.print_activity(description)
        self.depth += 1
        value = job(self, *extra_args)
        self.depth -= 1
        return value

    def get_color(self, color):
        if self.args.usecolor:
            return "\033[%sm" % color
        else:
            return ""

    def end_color(self):
        if self.args.usecolor:
            return "\033[0m"
        else:
            return ""

    def print_activity(self, message):
        print("%s..." % message)

    def print_string(self, message):
        print("%s%s" % (" " * self.depth, message))

    def print_notice(self, message, prefix="INFO"):
        print("%s%s%s:%s %s" %
                (" " * self.depth, self.get_color(WHITE_BOLD), prefix, self.end_color(), message))

    def print_warning(self, message, prefix="WARN"):
        print("%s%s%s:%s %s" %
                (" " * self.depth, self.get_color(YELLOW), prefix, self.end_color(), message))

    def print_error(self, message, prefix="ERROR"):
        print("%s%s%s:%s %s" %
                (" " * self.depth, self.get_color(RED_BOLD), prefix, self.end_color(), message))

    def print_operation(self, operation, item):
        print("%s[%s] %s" %
                (" " * self.depth, operation, item))

