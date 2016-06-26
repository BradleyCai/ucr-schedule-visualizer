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

from target import TargetProcess

config_fields = {
    "source-files": list,
    "regex-directory": str,
    "copy-to": list,
    "inject-file": str,
    "to-inject": dict,
}

def run(args, config):
    target = TargetProcess(args, config)

