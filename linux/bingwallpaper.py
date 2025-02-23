#!/usr/bin/env python3
import argparse
import pathlib
import re
import shutil
import subprocess
from typing import Literal
import requests
import os
import sys
import traceback
from datetime import datetime
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QFrame,
    QPushButton,
    QScrollArea,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QMessageBox,
    QGroupBox,
)

try:
    parser = argparse.ArgumentParser()
    s = parser.add_subparsers(
        title="action",
        description="The action to perform",
        dest="action",
        required=True,
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
    gui = s.add_parser("gui")
    gui.add_argument(
        "command",
        type=str,
        nargs="*",
        help=r"The command used to set the wallpaper ({} will be replaced with the image path)",
    )
    args = parser.parse_args()

    def locale() -> str:
        if "LANG" in os.environ:
            return ".".join(os.environ["LANG"].split(".")[:-1]).replace("_", "-")
        return ""

    print(">", args)

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
            f' >> Image "{v["title"]}" active {"since" if i==0 else "from"} {date(v["fullstartdate"]).strftime(r"%d.%m. %H:%M")} {f"to {date(data['images'][i-1]["fullstartdate"]).strftime(r"%d.%m. %H:%M")}" if i!=0 else ""}'
        )

    def size(num, suffix="B"):
        for unit in ("", "K", "M", "G", "T", "P", "E", "Z"):
            if abs(num) < 1024.0:
                return f"{num:3.1f}{unit}{suffix}"
            num /= 1024.0
        return f"{num:.1f}Yi{suffix}"

    def set(offset, command, reload, data):
        if not command:
            print("> Empty command", file=sys.stderr)
            raise SystemExit(1)
        path = os.path.expanduser(
            f"~/.config/bingwallpaper/{data["images"][offset]["hsh"]}-{re.match(r"/.*[?&]id=([^&]+)", data['images'][offset]["url"]).group(1)}"
        )
        pathlib.PosixPath(os.path.dirname(path)).mkdir(parents=True, exist_ok=True)

        class _(Exception):
            pass

        try:
            print(f'> Saving to path "{path}"')
            if os.path.isfile(path):
                print(
                    "> File already exists,",
                    "reloading" if reload else "skipping download",
                )
                if not reload:
                    raise _()
            elif os.path.isdir(path):
                print("> Path already exists as a directory", file=sys.stderr)
                raise SystemExit(1)
            img = requests.get("https://www.bing.com" + data["images"][offset]["url"])
            with open(path, "wb") as f:
                f.write(img.content)
            print(">", size(os.path.getsize(path)), "saved to disk")
        except IndexError:
            print("> Offset", offset, "is not available", file=sys.stderr)
            raise SystemExit(1)
        except requests.exceptions.ConnectionError:
            print(
                "> A connection error occurred while attempting to download image",
                file=sys.stderr,
            )
            raise SystemExit(1)
        except _:
            pass

        proc = subprocess.Popen(list([i.format(path, path=path) for i in command]))
        if proc.wait() != 0:
            print(
                "> Wallpaper set process failed with code",
                proc.returncode,
                file=sys.stderr,
            )
            raise SystemExit(1)
        print("> Wallpaper set successfully")

    def download(location, force, offset, data):
        if not location:
            print("> Empty output location, saving to current directory")
            path = re.match(r"/.*[?&]id=([^&]+)", data["images"][offset]["url"]).group(
                1
            )
        else:
            path = str(location)

        try:
            print(f'> Saving to path "{path}"')
            if os.path.isfile(path):
                print(
                    "> File already exists",
                    "" if not force else ", overwriting",
                    sep="",
                )
                if not force:
                    raise SystemExit(1)
            elif os.path.isdir(path):
                print("> Path already exists as a directory", file=sys.stderr)
                raise SystemExit(1)
            img = requests.get("https://www.bing.com" + data["images"][offset]["url"])
            with open(path, "wb") as f:
                f.write(img.content)
            print(">", size(os.path.getsize(path)), "saved to disk successfully")
        except IndexError:
            print("> Offset", offset, "is not available", file=sys.stderr)
            raise SystemExit(1)
        except requests.exceptions.ConnectionError:
            print(
                "> A connection error occurred while attempting to download image",
                file=sys.stderr,
            )
            raise SystemExit(1)

    def download_inline(i, overwrite=False):
        path = os.path.expanduser(
            f"~/.config/bingwallpaper/{i["hsh"]}-{re.match(r"/.*[?&]id=([^&]+)", i["url"]).group(1)}"
        )
        pathlib.PosixPath(os.path.dirname(path)).mkdir(parents=True, exist_ok=True)

        try:
            print(f'> Downloading to path "{path}"')
            if os.path.isfile(path):
                print(
                    f"> File already exists, {"skipping" if not overwrite else "overwriting"}"
                )
                if not overwrite:
                    return path
            elif os.path.isdir(path):
                print(
                    f"> Path already exists as a directory{", deleting" if overwrite else ""}"
                )
                if overwrite:
                    shutil.rmtree(path)
                    return download_inline(i)
                return None
            img = requests.get("https://www.bing.com" + i["url"])
            with open(path, "wb") as f:
                f.write(img.content)
            print(">", size(os.path.getsize(path)), "saved to disk successfully")
            return path
        except requests.exceptions.ConnectionError:
            print("> A connection error occurred while attempting to download image")
            return None

    class _gui(QMainWindow):
        def __init__(self, data, *_, **__):
            super().__init__(*_, **__)
            self.gui()

        def gui(self):
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            self.setCentralWidget(scroll_area)
            widget = QWidget()
            scroll_area.setWidget(widget)
            widget.setLayout(QVBoxLayout())

            class _btns(QWidget):
                def __init__(self, i, path, parent):
                    super().__init__()
                    self.setLayout(QVBoxLayout())

                    apply = QPushButton("Apply Wallpaper")
                    apply.clicked.connect(lambda: parent.apply(i))
                    self.layout().addWidget(apply)
                    reload = QPushButton("Redownload Wallpaper")

                    def _():
                        download_inline(i, True)
                        parent.gui()
                        QMessageBox(
                            QMessageBox.Icon.Information,
                            "Success",
                            "Downloaded wallpaper",
                            parent=parent,
                        ).exec()

                    reload.clicked.connect(_)
                    self.layout().addWidget(reload)
                    delete = QPushButton("Delete Wallpaper File")

                    def _():
                        try:
                            open(path, "wb").close()
                        except (FileNotFoundError, IsADirectoryError):
                            pass
                        parent.gui()
                        QMessageBox(
                            QMessageBox.Icon.Information,
                            "Success",
                            "File deleted successfully",
                            parent=parent,
                        ).exec()

                    delete.clicked.connect(_)
                    self.layout().addWidget(delete)

            for i in data["images"]:
                _ = abs((date(i["enddate"]) - date(data["images"][0]["enddate"])).days)
                w = QGroupBox(
                    title=f"{"Today" if _==0 else f"{_} day{"s" if _ != 1 else ""} ago"} - {i["title"]}"
                )
                w.setLayout(QHBoxLayout())
                widget.layout().addWidget(w)
                img = download_inline(i)
                if img is not None:
                    label = QLabel()
                    label.setPixmap(QPixmap(img).scaledToHeight(200))
                else:
                    label = QLabel("Image failed to download")
                    label.setStyleSheet("font-style: italic;")
                w.layout().addWidget(label)
                w.layout().addItem(
                    QSpacerItem(
                        0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
                    )
                )
                b = _btns(i, img, self)
                w.layout().addWidget(b)

            widget.layout().addItem(
                QSpacerItem(
                    0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
                )
            )
            reset = QPushButton("Full reset (deletes all files)")

            def _():
                shutil.rmtree(os.path.expanduser("~/.config/bingwallpaper"))
                self.gui()

            reset.clicked.connect(_)
            widget.layout().addWidget(reset)

        def apply(self, i):
            path = download_inline(i, True)
            if not args.command:
                print("> Empty command", file=sys.stderr)
                raise SystemExit(1)

            proc = subprocess.Popen(
                list([i.format(path, path=path) for i in args.command])
            )
            if proc.wait() != 0:
                print(
                    "> Wallpaper set process failed with code",
                    proc.returncode,
                    file=sys.stderr,
                )
                QMessageBox(
                    QMessageBox.Icon.Critical,
                    "Error",
                    "Wallpaper set process failed with code " + str(proc.returncode),
                    parent=self,
                ).exec()
                self.gui()
                return
            print("> Wallpaper set successfully")
            QMessageBox(
                QMessageBox.Icon.Information,
                "Success",
                "Wallpaper applied successfully",
                parent=self,
            ).exec()
            self.gui()

    def gui(data):
        if not args.command:
            print("> Empty command", file=sys.stderr)
            raise SystemExit(1)
        root = QApplication([])
        root.setStyle("Fusion")
        app = _gui(data)
        app.show()
        root.exec()

    match args.action:
        case "set":
            set(args.offset, args.command, args.reload, data)
        case "download":
            download(args.location, args.force, args.offset, data)
        case "gui":
            gui(data)
        case _:
            raise ValueError("Invalid action")
except Exception as e:
    print(
        f"\x1b[1;91m> {type(e).__name__}: {str(e)}\n{''.join(traceback.format_tb(e.__traceback__))}\x1b[0m"
    )
    raise SystemExit(1)
