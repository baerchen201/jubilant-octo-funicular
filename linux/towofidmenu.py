import sys
import re

import argparse

argparser = argparse.ArgumentParser(
    prog="towofidmenu", description="Add display names to wofi dmenu mode"
)
argparser.add_argument("file", help="the input file")
argparser.add_argument(
    "-c", help="reads a display name from stdin and returns the associated command"
)
argparser.add_argument(
    "-C", help="use command as prefix if not explicitly specified", action="store_true"
)
argparser.add_argument(
    "-l", help="always clear SHLVL variable for process", action="store_true"
)
args = argparser.parse_args()

with open(args.file, "rb") as f:
    for item in f.read().decode().strip().splitlines():
        if not re.sub(r"#[^\n]*", "", item.strip()).strip():
            continue
        line = item.split("|", 2)  # Split only twice to allow commands with pipes
        command, display, prefix = [None for _ in range(3)]  # Initialize variables
        match len(line):
            case 1:  # Only command, use as display name, no prefix
                command = line[0]
                display = command
            case 2:  # Command and display name, no prefix*
                command = line[1]
                display = line[0]
                if args.C:
                    prefix = command.split()[
                        0
                    ]  # If -C argument used, use command as prefix
            case 3:  # Command, display name and prefix specified, assign values
                command = line[2]
                display = line[0]
                prefix = line[1]
        if prefix:
            display = f"[{prefix}] {display}"  # Adjust display name if prefix present

        if args.c:  # If -c argument specified, test for match
            if args.c == display:
                print(("SHLVL=0 " if args.l else "") + command)
                raise SystemExit(0)
        else:
            print(display)

raise SystemExit(
    int(bool(args.c))
)  # Smart usage of int(bool(x)), if -c argument specified no match was found, so exit code 1, otherwise 0
