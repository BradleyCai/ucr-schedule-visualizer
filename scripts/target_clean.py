__all__ = ["depends", "config_fields", "run"]

import glob
import os

depends = [
]

config_fields = {
}

def run(tracker):
    for location in ("js", "tests"):
        tracker.run_job(job_clean, "Cleaning %s" % location, location)

    tracker.run_job(job_clean_no_remove_regex, "Cleaning regex", "regex")


def job_clean(tracker, location):
    path = os.path.join("..", location)
    files = glob.glob("%s/*.regex" % path) + glob.glob("%s/*.out" % path)

    if not files:
        tracker.print_string("(nothing to do)")

    for filename in files:
        tracker.print_operation("RM", filename)
        try:
            os.remove(filename)
        except OSError as err:
            tracker.print_error(err)
            tracker.failure()


def job_clean_no_remove_regex(tracker, location):
    path = os.path.join("..", location)
    files = glob.glob("%s/*.out" % path)

    if not files:
        tracker.print_string("(nothing to do)")

    for filename in files:
        tracker.print_operation("RM", filename)
        try:
            os.remove(filename)
        except OSError as err:
            tracker.print_error(err)
            tracker.failure()

