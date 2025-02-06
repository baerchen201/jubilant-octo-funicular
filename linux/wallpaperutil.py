#!/usr/bin/env python3

import argparse
import pathlib
import os
import json
import subprocess
import sys
from typing import Literal

try:
    import PIL
    from PIL import Image
except ModuleNotFoundError:
    sys.stderr.write("PIL not installed, image editing/verification is unavailable\n")
    PIL = None
    Image = None

parser = argparse.ArgumentParser(
    prog="wallpaperutil.py", description="Wallpaper utility for hyprland"
)
parser.add_argument(
    "-c",
    "--config",
    help="path to the config directory",
    metavar="dir",
    dest="config",
    type=pathlib.Path,
    default=os.path.expanduser("~/.config/wallpaperutil.py"),
)
subparsers = parser.add_subparsers(dest="cmd")
set_args = subparsers.add_parser("set", help="Set static wallpaper")
set_args.add_argument(
    "image",
    help="The Image file to set the wallpaper to",
    metavar="file",
    type=pathlib.Path,
)
set_conversion_args = set_args.add_mutually_exclusive_group()
set_conversion_args.add_argument(
    "-f",
    "--force",
    action="store_true",
    dest="force",
    help="Skips image verification and conversion",
)
set_conversion_args.add_argument(
    "-g",
    "--geometry",
    type=int,
    dest="geometry",
    help="Resize image to fit a preset - TODO: IMPLEMENT",
    metavar="preset",
)
set_args.add_argument(
    "--no-reload",
    dest="noreload",
    action="store_true",
    help="Does not reload hyprland automatically",
)
subparsers.add_parser("presets", help="\\  Display presets for image resizing")
subparsers.add_parser("get", help="Display wallpaper and overrides")
override_args = subparsers.add_parser(
    "override", help="Change wallpaper conditionally - TODO: IMPLEMENT"
)
args = parser.parse_args()


try:
    args.config.mkdir(parents=True, exist_ok=True)
except FileExistsError:
    print("The provided config directory already exists as a file")
    raise SystemExit(1)

RESIZE_PRESETS: dict[int, tuple[bool, int, int]] = {
    0: (False, 1920, 1080),
    1: (True, 1920, 1080),
    2: (False, 2560, 1440),
    3: (True, 2560, 1440),
}

match args.cmd:
    case "presets":
        for k, v in RESIZE_PRESETS.items():
            print(
                (
                    " "
                    * (
                        len(str(sorted(list(RESIZE_PRESETS.keys()))[-1]))
                        + 2
                        - len(str(k))
                    )
                )
                + str(k)
                + ":",
                "CUT" if v[0] else "PAD",
                (
                    (
                        len(
                            str(
                                sorted(list([i[1] for i in RESIZE_PRESETS.values()]))[
                                    -1
                                ]
                            )
                        )
                        - len(str(v[1]))
                    )
                    * " "
                )
                + str(v[1])
                + "x"
                + str(v[2]),
                sep=" ",
            )
        raise SystemExit(0)
    case "set":
        try:
            with open(args.config / "config.json", "r") as f:
                configs = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            configs = {}
        configs["source_img"] = str(args.image.absolute())
        if Image and not args.force:
            try:
                with Image.open(args.image) as f:
                    f.convert("RGB")
                    f.save(args.config / "wallpaper.png", format="png")
                args.image = args.config / "wallpaper.png"
            except PIL.UnidentifiedImageError:
                print(
                    "Image verification failed, please confirm if the provided file is a valid image or use -f to skip verification"
                )
                raise SystemExit(1)
        configs["image"] = str(args.image.absolute())
        with open(args.config / "config.json", "w") as f:
            json.dump(configs, f)
        if not args.noreload:
            subprocess.run(["hyprctl", "reload"], stdout=subprocess.PIPE)

    case "get":
        try:
            with open(args.config / "config.json", "rb") as f:
                configs = json.load(f)
        except FileNotFoundError:
            print("No wallpaper set")
            raise SystemExit(1)

        try:
            print("[ORIGINAL]", configs["source_img"])
            if configs["source_img"] != configs["image"]:
                print("[CONVERTED]", configs["image"])
        except KeyError:
            print("No wallpaper set")
            raise SystemExit(1)

    case "override":
        print("override mode")  # TODO: IMPLEMENT
        print("TODO: IMPLEMENT")
        raise SystemExit(1)

    case _:
        try:
            with open(args.config / "config.json", "rb") as f:
                configs = json.load(f)
        except FileNotFoundError:
            sys.stderr.write(
                "No wallpaper set, use `wallpaperutil.py -h` for more information\n"
            )
            raise SystemExit(1)
        try:
            print(configs["image"])
        except KeyError:
            try:
                print(configs["source_img"])
            except KeyError:
                sys.stderr.write("No wallpaper set\n")
                raise SystemExit(1)
