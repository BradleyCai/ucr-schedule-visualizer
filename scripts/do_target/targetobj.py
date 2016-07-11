__all__ = [
    "TargetTracker",
    "get_target_module",

    "BLACK",
    "RED",
    "GREEN",
    "YELLOW",
    "BLUE",
    "MAGENTA",
    "CYAN",
    "WHITE",
    "RESET",
    "BLACK_BOLD",
    "RED_BOLD",
    "GREEN_BOLD",
    "YELLOW_BOLD",
    "BLUE_BOLD",
    "MAGENTA_BOLD",
    "CYAN_BOLD",
    "WHITE_BOLD",
]

from .static import PROGRAM_NAME

BLACK = "30"
RED = "31"
GREEN = "32"
YELLOW = "33"
BLUE = "34"
MAGENTA = "35"
CYAN = "36"
WHITE = "37"
RESET = "0"

BLACK_BOLD = "30;1"
RED_BOLD = "31;1"
GREEN_BOLD = "32;1"
YELLOW_BOLD = "33;1"
BLUE_BOLD = "34;1"
MAGENTA_BOLD = "35;1"
CYAN_BOLD = "36;1"
WHITE_BOLD = "37;1"


class TargetTracker(object):
    BLACK = BLACK
    RED = RED
    GREEN = GREEN
    YELLOW = YELLOW
    BLUE = BLUE
    MAGENTA = MAGENTA
    CYAN = CYAN
    WHITE = WHITE

    BLACK_BOLD = BLACK_BOLD
    RED_BOLD = RED_BOLD
    GREEN_BOLD = GREEN_BOLD
    YELLOW_BOLD = YELLOW_BOLD
    BLUE_BOLD = BLUE_BOLD
    MAGENTA_BOLD = MAGENTA_BOLD
    CYAN_BOLD = CYAN_BOLD
    WHITE_BOLD = WHITE_BOLD

    def __init__(self, args, config):
        self.args = args
        self.config = config
        self.depth = 0
        self.successful = True

    def failure(self):
        self.successful = False

    def terminate(self):
        raise SystemExit

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
        print("%s%s..." % (" " * self.depth, message))

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

    def print_operation(self, operation, item="", color=None):
        if color:
            print("%s[%s%s%s] %s" %
                    (" " * self.depth, self.get_color(color), operation, self.end_color(), item))
        else:
            print("%s[%s] %s" %
                    (" " * self.depth, operation, item))


def get_target_module(name):
    # Load the target module
    try:
        module = __import__("target_%s" % name)
    except ImportError:
        print("%s: No such build target: %s." % (PROGRAM_NAME, name))
        exit(1)

    # Perform sanity checks on the module
    if not hasattr(module, "depends"):
        print("%s: Target %s lacks a dependency list called \"depends\"." % (PROGRAM_NAME, name))
        exit(1)

    if not hasattr(module, "config_fields"):
        print("%s: Target %s lacks a configuration template called \"config_fields\"." %
                (PROGRAME_NAME, name))
        exit(1)

    if not hasattr(module, "run"):
        print("%s: Target %s lacks an execution directive called \"run\"." %
                (PROGRAM_NAME, name))
        exit(1)

    module.name = name
    return module

