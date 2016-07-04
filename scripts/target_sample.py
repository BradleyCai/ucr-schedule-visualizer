__all__ = ["depends", "config_fields", "run"]

import random

depends = [
    # Specify dependencies here. Each of these is a target
    # as specified in a target_* file.
]

config_fields = {
    # Settings can be passed to a target as a JSON file
    # Specify the types of each field here

    # If this dictionary is empty, it tells build.py to
    # not load a config file
}

def run(tracker):
    tracker.run_job(job_hello_world, "Printing \"hello world\"")
    tracker.print_notice("Important notice here")
    tracker.run_job(job_foo_bar, "Fooing bars")
    tracker.print_warning("Something possibly bad happened")


def job_hello_world(tracker):
    tracker.print_operation("PRINT", "Hello")
    tracker.print_operation("PRINT", "World")


def job_foo_bar(tracker):
    for i in range(11):
        tracker.print_operation("FOO", "bar %d" % i)

        if i % 3 == 0:
            tracker.run_job(job_crunch_numbers, "Crunching numbers")

        if random.random() < 0.2:
            tracker.print_error("Oh noes!")


def job_crunch_numbers(tracker):
    for i in range(random.randint(2, 7)):
        tracker.print_operation("CALC", str(random.randint(-100, 100)))

