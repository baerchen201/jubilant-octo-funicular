#!/usr/bin/env python3

import argparse
import pathlib
import os
import json
import subprocess
import sys

try:
    import PIL
    from PIL import Image
except ModuleNotFoundError:
    sys.stderr.write("PIL not installed, image editing/verification is unavailable\n")
    Image = None

parser = argparse.ArgumentParser(
        prog="wallpaperutil.py", description="Wallpaper utility for hyprland")
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
    help="Skips image verification and conversion",
)
set_args.add_argument(
    "--no-reload",
    dest="noreload",
    action="store_true",
    help="Does not reload hyprland automatically",
)
subparsers.add_parser("get")
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
            sys.stderr.write("No wallpaper set, use `wallpaperutil.py -h` for more information\n")
            raise SystemExit(1)
        try:
            print(configs["image"])
        except KeyError:
            try:
                print(configs["source_img"])
            except KeyError:
                sys.stderr.write("No wallpaper set\n")
                raise SystemExit(1)
