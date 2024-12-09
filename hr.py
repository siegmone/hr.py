#! /bin/python

import sys
import time
import subprocess
import os
from datetime import datetime


class Watchdog:
    def __init__(self, target):
        self.target = os.path.abspath(target)
        self.target_basename = os.path.basename(self.target)
        self.last_modified = os.path.getmtime(self.target)

    def start(self):
        self.last_check = os.path.getmtime(self.target)
        stdout, stderr = self.run_script()
        self.print_output(stdout, stderr)
        while True:
            dt = datetime.now()
            dt_fmt = dt.strftime("%Y-%m-%d %H:%M:%S")
            if self.detect_changes():
                start_time = time.time()
                stdout, stderr = self.run_script()
                end_time = time.time()
                elapsed = 1000 * (end_time - start_time)
                execution_time_str = f"Executed in: {elapsed:.3f}ms"
                print(f"{dt_fmt} | {self.target_basename} - {execution_time_str}")
                self.print_output(stdout, stderr)
            time.sleep(0.1)

    def run_script(self) -> (str, str):
        try:
            result = subprocess.run(
                ["python", self.target],
                capture_output=True,
                text=True
            )
            return result.stdout, result.stderr
        except Exception as e:
            print(f"Error running script: {e}")

    def print_output(self, stdout, stderr) -> None:
        if stdout:
            print_bold()
            print("\nSTDOUT:", end="")
            print_reset()
            print_green()
            print(stdout)
            print_reset()
        if stderr:
            print_bold()
            print("\nSTDERR:", end="")
            print_reset()
            print_red()
            print(stderr)
            print_reset()

    def detect_changes(self) -> bool:
        last_change = os.path.getmtime(self.target)
        changed = (last_change != self.last_check)
        self.last_check = last_change
        return changed


def print_reset():
    print("\033[0m")


def print_clear():
    print("\033[H\033[2J", end="")


def print_hide_cursor():
    print("\033[?25l", end="")


def print_show_cursor():
    print("\033[?25h", end="")


def print_bold():
    print("\033[1m", end="")


def print_red():
    print("\033[31m", end="")


def print_green():
    print("\033[32m", end="")


def print_blue():
    print("\033[34m", end="")


def print_usage():
    print(f"Usage: {program} <target-script.py>")

# ]]]]]]]]]
# idx why the lsp can't comprehend that those aren't real brackets smh


if __name__ == "__main__":
    argv = sys.argv
    program, *argv = argv

    if len(argv) == 0:
        print("Please provide a target script.")
        print_usage()
        sys.exit(1)
    if len(argv) > 1:
        print("Too many arguments.")
        print_usage()
        sys.exit(1)
    if argv[0] == "help":
        print_usage()
        sys.exit(0)

    target = argv[0]

    if not os.path.isfile(target):
        print(f"Error: File {target} does not exist.")
        sys.exit(1)

    print(f"Starting watchdog on {target}")

    watchdog = Watchdog(target)
    watchdog.start()
