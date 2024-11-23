import sys

import argparse
argparser = argparse.ArgumentParser(prog="towofidmenu", description="Add display names to wofi dmenu mode")
argparser.add_argument("file", help="The input file")
argparser.add_argument("-c", help="Get the command by display name")
argparser.add_argument("-C", help="Use command as prefix if none specified", action="store_true")
args = argparser.parse_args()

with open(args.file, "rb") as f:
    for item in f.read().decode().strip().splitlines():
        line = item.split("|", 2)
        command, display, prefix = [None for _ in range(3)]
        match len(line):
            case 1:
                command = line[0]
                display = command
            case 2:
                command = line[1]
                display = line[0]
                if args.C: prefix = command.split()[0]
            case 3:
                command = line[2]
                display = line[0]
                prefix = line[1]
        if prefix:
            display = f"[{prefix}] {display}"
        if args.c:
            if args.c == display:
                print(command)
                raise SystemExit(0)
        else:
            print(display)
raise SystemExit(int(bool(args.c)))
