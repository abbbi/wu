"""foo

Usage:
  wu.py [--timeout=<seconds>] file <name> exists
  wu.py [--timeout=<seconds>] file <name> exists and delete it
  wu.py [--timeout=<seconds>] file <name> exists and contains <string>

"""
import os
import sys
from docopt import docopt
from busypie import wait
from busypie.awaiter import ConditionTimeoutError
from busypie import set_default_timeout


def exists(filename):
    """Check file exists"""
    return os.path.exists(filename) and os.path.isfile(filename)


def contains(filename, string):
    """Check file contains"""
    with open(filename, "rb") as filehandle:
        data = filehandle.read().decode()
        return string in data


def delete(filename):
    """Remove file"""
    if not os.path.exists(filename):
        return True

    return os.remove(filename)


def main(args):
    """main magic"""
    checks = []
    timeout = int(10)
    if args["--timeout"]:
        print("set timeout: ", args["--timeout"])
        timeout = int(args["--timeout"])
        set_default_timeout(timeout)
    if args["file"]:
        name = args["<name>"]
        if name and all(name):
            checks.append(lambda: exists(name))
        string = args["<string>"]
        if string and all(string):
            checks.append(lambda: contains(name, string))
        if args["delete"]:
            checks.append(lambda: delete(name))

    for check in checks:
        try:
            wait().until(check)
        except ConditionTimeoutError as err:
            print("Failed to meet condition: ", err)
            sys.exit(1)

    print("OK")


if __name__ == "__main__":
    arguments = docopt(__doc__)
    main(arguments)
