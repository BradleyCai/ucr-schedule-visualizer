__all__ = ["config_fields", "run"]

from target import TargetProcess
import random

config_fields = {
    # Settings can be passed to a target as a JSON file
    # Specify the types of each field here

    # If this dictionary is empty, it tells build.py to
    # not load a config file
}

def run(args, config):
    process = TargetProcess(args, config)
    process.run_job(job_hello_world, "Printing \"hello world\"")
    process.print_notice("Important notice here")
    process.run_job(job_foo_bar, "Fooing bars")
    process.print_warning("Something possibly bad happened")
    return process


def job_hello_world(process):
    process.print_operation("PRINT", "Hello")
    process.print_operation("PRINT", "World")


def job_foo_bar(process):
    for i in range(11):
        process.print_operation("FOO", "bar %d" % i)

        if i % 3 == 0:
            process.run_job(job_crunch_numbers, "Crunching numbers")

        if random.random() < 0.2:
            process.print_error("Oh noes!")


def job_crunch_numbers(process):
    for i in range(random.randint(2, 7)):
        process.print_operation("CALC", str(random.randint(-100, 100)))

