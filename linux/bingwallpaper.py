#!/usr/bin/env python3
import argparse
import pathlib
import re
import subprocess
from typing import Literal
import requests
import os
import sys
import traceback
from datetime import datetime

try:
    parser = argparse.ArgumentParser()
    s = parser.add_subparsers(
        title="action", description="The action to perform", dest="action"
    )
    set = s.add_parser("set")
    set.add_argument(
        "command",
        type=str,
        nargs="*",
        help=r"The command used to set the wallpaper ({} will be replaced with the image path)",
    )
    set.add_argument(
        "-o",
        "--offset",
        type=int,
        required=False,
        default=0,
        choices=list(range(8)),
        help="The offset in days",
    )
    set.add_argument(
        "-r",
        "--reload",
        action="store_true",
        help="Whether to redownload existing image files",
    )
    download = s.add_parser("download")
    download.add_argument(
        "location",
        type=pathlib.Path,
        nargs="?",
        help="The output file location",
    )
    download.add_argument(
        "-o",
        "--offset",
        type=int,
        required=False,
        default=0,
        choices=list(range(8)),
        help="The offset in days",
    )
    download.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Overwrites existing files",
    )
    args = parser.parse_args()

    def locale() -> str:
        if "LANG" in os.environ:
            return ".".join(os.environ["LANG"].split(".")[:-1]).replace("_", "-")
        return ""

    print(">", locale())

    response = requests.get(
        f"https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=8&mkt={locale()}"
    )

    def date(date: str) -> datetime:
        match len(date):
            case 8:
                return datetime.strptime(date, r"%Y%m%d")
            case 12:
                return datetime.strptime(date, r"%Y%m%d%H%M")
            case _:
                raise ValueError("Invalid date string")

    try:
        data: dict[
            Literal["images", "tooltips"],
            list[dict[str, str | int | bool | list]]
            | dict[Literal["loading", "previous", "next", "walle", "walls"], str],
        ] = response.json()
        assert type(data["images"]) is list
        assert type(data["tooltips"]) is dict
    except requests.exceptions.JSONDecodeError:
        print("> Server returned invalid JSON, exiting", file=sys.stderr)
        raise SystemExit(1)
    except requests.exceptions.JSONDecodeError:
        print("> Server returned unknown data, exiting", file=sys.stderr)
        raise SystemExit(1)

    print("> Server returned", len(data["images"]), "of 8 images")
    for i, v in enumerate(data["images"]):
        print(
            f' >> Image "{v["title"]}" active {"since" if i==0 else "from"} {date(v["fullstartdate"]).strftime(r"%d.%m %H:%M")} {f"to {date(data['images'][i-1]["fullstartdate"]).strftime(r"%d.%m %H:%M")}" if i!=0 else ""}'
        )

    def size(num, suffix="B"):
        for unit in ("", "K", "M", "G", "T", "P", "E", "Z"):
            if abs(num) < 1024.0:
                return f"{num:3.1f}{unit}{suffix}"
            num /= 1024.0
        return f"{num:.1f}Yi{suffix}"

    match args.action:
        case "":
            pass
        case "set":
            if not args.command:
                print("> Empty command", file=sys.stderr)
                raise SystemExit(1)
            path = os.path.expanduser(
                f"~/.config/bingwallpaper/{data["images"][args.offset]["hsh"]}-{re.match(r"/.*[?&]id=([^&]+)", data['images'][args.offset]["url"]).group(1)}"
            )
            pathlib.PosixPath(os.path.dirname(path)).mkdir(parents=True, exist_ok=True)

            class _(Exception):
                pass

            try:
                print(f'> Saving to path "{path}"')
                if os.path.isfile(path):
                    print(
                        "> File already exists,",
                        "reloading" if args.reload else "skipping download",
                    )
                    if not args.reload:
                        raise _()
                elif os.path.isdir(path):
                    print("> Path already exists as a directory", file=sys.stderr)
                    raise SystemExit(1)
                img = requests.get(
                    "https://www.bing.com" + data["images"][args.offset]["url"]
                )
                with open(path, "wb") as f:
                    f.write(img.content)
                print(">", size(os.path.getsize(path)), "saved to disk")
            except IndexError:
                print("> Offset", args.offset, "is not available", file=sys.stderr)
                raise SystemExit(1)
            except requests.exceptions.ConnectionError:
                print(
                    "> A connection error occurred while attempting to download image",
                    file=sys.stderr,
                )
                raise SystemExit(1)
            except _:
                pass

            proc = subprocess.Popen(
                list([i.format(path, path=path) for i in args.command])
            )
            if proc.wait() != 0:
                print(
                    "> Wallpaper set process failed with code",
                    proc.returncode,
                    file=sys.stderr,
                )
                raise SystemExit(1)
            print("> Wallpaper set successfully")
        case "download":
            if not args.location:
                print("> Empty output location, saving to current directory")
                path = re.match(
                    r"/.*[?&]id=([^&]+)", data["images"][args.offset]["url"]
                ).group(1)
            else:
                path = str(args.location)

            try:
                print(f'> Saving to path "{path}"')
                if os.path.isfile(path):
                    print(
                        "> File already exists",
                        "" if not args.force else ", overwriting",
                        sep="",
                    )
                    if not args.force:
                        raise SystemExit(1)
                elif os.path.isdir(path):
                    print("> Path already exists as a directory", file=sys.stderr)
                    raise SystemExit(1)
                img = requests.get(
                    "https://www.bing.com" + data["images"][args.offset]["url"]
                )
                with open(path, "wb") as f:
                    f.write(img.content)
                print(">", size(os.path.getsize(path)), "saved to disk successfully")
            except IndexError:
                print("> Offset", args.offset, "is not available", file=sys.stderr)
                raise SystemExit(1)
            except requests.exceptions.ConnectionError:
                print(
                    "> A connection error occurred while attempting to download image",
                    file=sys.stderr,
                )
                raise SystemExit(1)
        case _:
            raise ValueError("Invalid action")
except Exception as e:
    print(
        f"\x1b[1;91m> {type(e).__name__}: {str(e)}\n{''.join(traceback.format_tb(e.__traceback__))}\x1b[0m"
    )
    raise SystemExit(1)
