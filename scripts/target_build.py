__all__ = ["config_fields", "run"]

"""
The purpose of this target is to 'compile' the regular expressions
found in the regex/ directory and inject them into their respective
Javascript sources in the js/ directory. This is done by invoking a
Python script in regex/ that combines multiple *.regex files into
'compiled' *.out files. The purpose of this is to break down these
long and complicated regular expressions into more meaningful parts,
which can be fixed easier.  This means that whenever you need to
modify a regular expression, you should only modify the *.regex files
in regex/. The *.out files or the regular expressions in the javascript
sources should not be modified, as they will be overwritten.
"""

import glob
import os
import re
import shutil

DEPENDENCY_REGEX = re.compile(r"%\{.*?\}")
DEPENDENCY_NAME_REGEX = re.compile(r"%\{(.*?)\}")

REGEX_INJECTION_PATTERN = r"this\.%s\s*=\s*\/.\/g;"
REGEX_REPLACE_PATTERN = r"this.%s = /%s/g;"

config_fields = {
    "source-files": list,
    "regex-directory": str,
    "copy-to": list,
    "inject-file": str,
    "to-inject": dict,
}

def run(tracker):
    directory = os.path.join("..", tracker.config["regex-directory"])
    tracker.print_activity("Switching directory to \"%s\"" % directory)
    try:
        os.chdir(directory)
    except OSError as err:
        tracker.print_error("Unable to change directory to %s: %s" % (directory, err))
        tracker.terminate()

    tracker.run_job(job_compile_regexes, "Compiling regex sources")
    tracker.run_job(job_copy_out_files, "Copying compiled regex artifacts")
    tracker.run_job(job_inject_regex_artifacts, "Injecting compiled regex artifacts")


### Defined jobs ###
def job_compile_regexes(tracker):
    if not tracker.config["source-files"]:
        tracker.print_string("(nothing to do)")

    for source in tracker.config["source-files"]:
        tracker.run_job(job_compile_regex, None, source)


def job_compile_regex(tracker, name):
    if name.endswith(".regex"):
        source = name
        target = name[:-6] + ".out"
    else:
        source = name + ".regex"
        target = name + ".out"

    if os.path.exists(target):
        if tracker.args.dontoverwrite:
            tracker.print_notice("Not overwriting \"%s\"." % target)
            return
        else:
            tracker.print_warning("Overwriting \"%s\"." % target)
    tracker.print_operation("REGEX", target)
    compiled = tracker.run_job(job_combine_regex, None, source)

    if compiled is None:
        return

    try:
        with open(target, "w") as fh:
            fh.write(compiled)
    except IOError as err:
        tracker.print_error("Unable to write to \"%s\": %s." % (target, err))
        tracker.failure()


def job_combine_regex(tracker, source, depends={}):
    tracker.print_operation("DEP", source)

    try:
        with open(source, "r") as fh:
            body = fh.read()
    except IOError as err:
        tracker.print_error("Unable to read from \"%s\": %s." % (source, err))
        tracker.failure()
        return None

    for depend in set(DEPENDENCY_REGEX.findall(body)):
        depend = DEPENDENCY_NAME_REGEX.match(depend).group(1)
        if depend not in depends.keys():
            depends[depend] = tracker.run_job(job_combine_regex, None, depend + ".regex", depends)
        else:
            tracker.print_operation("DEP", "%s (cached)" % source)
        body = body.replace("%%{%s}" % depend, depends[depend])
    return body.rstrip()


def job_copy_out_files(tracker):
    files = glob.glob("*.out")

    if not files:
        tracker.print_string("(nothing to do)")
    for filename in files:
        for directory in tracker.config["copy-to"]:
            dest = os.path.join(directory, filename)
            tracker.print_operation("COPY", "%s -> %s" % (filename, dest))
            try:
                shutil.copy(filename, dest)
            except (OSError, IOError) as err:
                tracker.print_error("Unable to copy file: %s.\n" % err)
                tracker.failure()


def job_inject_regex_artifacts(tracker):
    if not tracker.config["to-inject"]:
        tracker.print_string("(nothing to do)")

    output_file = tracker.config["inject-file"]
    for input_file, field in tracker.config["to-inject"].items():
        tracker.print_operation("INJ", "%s:%s <- %s" % (output_file, field, input_file))

        # Get artifact
        try:
            with open(input_file, "r") as fh:
                to_replace = fh.read()
        except IOError as err:
            tracker.print_error("Unable to read from \"%s\": %s." % (input_file, err))
            tracker.failure()
            continue
        else:
            to_replace = to_replace.replace(r"\n", r"\\n").strip()

        # Replace pattern with artifact
        try:
            with open(output_file, "r") as fh:
                output_text = fh.read()
        except IOError as err:
            tracker.print_error("Unable to read from \"%s\": %s." % (output_file, err))
            tracker.failure()
            continue
        else:
            output_text = \
                    re.sub(REGEX_INJECTION_PATTERN % re.escape(field),
                           REGEX_REPLACE_PATTERN % (field, to_replace),
                           output_text.rstrip())

        # Write result to file
        try:
            with open(output_file, "w") as fh:
                fh.write(output_text)
        except IOError as err:
            tracker.print_error("Unable to write to \"%s\": %s." % (output_file, err))
            tracker.failure()

