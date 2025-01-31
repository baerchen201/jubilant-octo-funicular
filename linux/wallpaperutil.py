#!/usr/bin/env python3

import argparse
import pathlib
import os
import json
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument(
    "-c",
    "--config",
    help="The path to the config directory",
    metavar="dir",
    dest="config",
    type=pathlib.Path,
    default=os.path.expanduser("~/.config/wallpaperutil.py"),
)
subparsers = parser.add_subparsers(dest="cmd")
set_args = subparsers.add_parser("set")
set_args.add_argument(
    "image",
    help="The Image file to set the wallpaper to",
    metavar="file",
    type=pathlib.Path,
)
set_args.add_argument(
    "-f",
    "--force",
    action="store_true",
    dest="force",
    help="Skips the image verification - TODO: IMPLEMENT",
)
set_args.add_argument(
    "--no-reload",
    dest="noreload",
    action="store_true",
    help="Does not reload hyprland automatically",
)
override_args = subparsers.add_parser("override")
args = parser.parse_args()


try:
    args.config.mkdir(parents=True, exist_ok=True)
except FileExistsError:
    print("The provided config directory already exists as a file")
    raise SystemExit(1)

match args.cmd:
    case "set":
        try:
            with open(args.config / "config.json", "r") as f:
                configs = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            configs = {}
        configs["image"] = str(args.image.absolute())
        with open(args.config / "config.json", "w") as f:
            json.dump(configs, f)
        if not args.noreload:
            subprocess.run(["hyprctl", "reload"], stdout=subprocess.PIPE)

    case "override":
        print("override mode")  # TODO: IMPLEMENT
        print("TODO: IMPLEMENT")
        raise SystemExit(1)

    case _:
        try:
            with open(args.config / "config.json", "rb") as f:
                configs = json.load(f)
        except FileNotFoundError:
            raise SystemExit(1)
        try:
            print(configs["image"])
        except KeyError:
            raise SystemExit(1)
