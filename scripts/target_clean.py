__all__ = ["config_fields", "run"]

from target import TargetProcess
import glob
import os

config_fields = {
}

def run(args, config):
    process = TargetProcess(args, config)

    for location in ("js", "tests"):
        process.run_job(job_clean, "Cleaning %s" % location, location)

    process.run_job(job_clean_no_remove_regex, "Cleaning regex", "regex")


def job_clean(process, location):
    path = os.path.join("..", location)
    files = glob.glob("%s/*.regex" % path) + glob.glob("%s/*.out" % path)

    for filename in files:
        process.print_operation("RM", os.path.basename(filename))
        try:
            os.remove(filename)
        except OSError as err:
            process.print_error(err)


def job_clean_no_remove_regex(process, location):
    path = os.path.join("..", location)
    files = glob.iglob("%s/*.out" % path)

    for filename in files:
        process.print_operation("RM", os.path.basename(filename))
        try:
            os.remove(filename)
        except OSError as err:
            process.print_error(err)

