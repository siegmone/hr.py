#! /bin/python

import sys
import time
from subprocess import run
import os
from datetime import datetime


class Watchdog:
    def __init__(self, target):
        self.target = target
        self.last_check = 0.0

    def start(self):
        self.last_check = os.path.getmtime(self.target)

    def stop(self):
        pass

    def detect_changes(self) -> bool:
        last_change = os.path.getmtime(self.target)
        changed = (last_change != self.last_check)
        self.last_check = last_change
        return changed


def usage() -> None:
    print(f"Usage: {program} <target-script.py>")


if __name__ == "__main__":
    argv = sys.argv
    program, *argv = argv
    if len(argv) == 0:
        print("Please provide a target script.")
        usage()
        exit(1)
    if argv[0] == "help":
        usage()
        exit(0)
    if len(argv) > 1:
        print("Too many arguments.")
        usage()
        exit(1)

    target = argv[0]
    watchdog = Watchdog(target)
    watchdog.start()

    try:
        while True:
            dt = datetime.now()
            dt_fmt = dt.strftime("%Y-%m-%d %H:%M:%S")
            if watchdog.detect_changes():
                print(dt_fmt)
                print()
                run(["python", target])
            time.sleep(0.5)
    except KeyboardInterrupt:
        watchdog.stop()
