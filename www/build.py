import os
import shutil

import sys

from html.parser import HTMLParser
from html import escape as html_escape
from urllib.parse import quote_plus


class NavHTMLParser(HTMLParser):
    def __init__(self, *_, **__) -> None:
        super().__init__(*_, *__)
        self.title = None
        self.updates = 0

    def handle_starttag(self, tag, attrs):
        if tag == "meta":
            dict_attrs = {}
            for attr in attrs:
                dict_attrs[attr[0]] = attr[1] if len(attr) > 1 else None

            if dict_attrs.get("name", None) == "nav-title":
                self.title = dict_attrs.get("content", None)

                self.updates += 1
                print(f"     > Found nav-title {self.title}")


html_files = {}

for dir, subdirs, files in os.walk("./www"):
    print(
        f"==> Processing directory {dir} ({len(subdirs)} {'subdirectory' if len(subdirs) == 1 else 'subdirectories'}, {len(files)} {'file' if len(files) == 1 else 'files'})"
    )

    if (not subdirs and not files) or (
        all([file.startswith(".") for file in files])
        and all([subdir.startswith(".") for subdir in subdirs])
    ):
        shutil.rmtree(dir)
        print(f"  > Removed directory tree {dir}")
        continue

    if os.path.isfile(os.path.join(dir, ".rm")):
        print(f"  -> Found .rm file, processing...")
        for file in [
            os.path.join(dir, i.strip())
            for i in open(os.path.join(dir, ".rm"), "r").read().strip().splitlines()
        ]:
            if os.path.isdir(file):
                shutil.rmtree(file)
                print(f"     > Removed directory tree {file}")
            elif os.path.isfile(file):
                os.remove(file)
                print(f"     > Removed file {file}")

    for file in files:
        if file.startswith(".") or file.endswith(".ts"):
            os.remove(os.path.join(dir, file))
            print(f"  > Removed file {os.path.join(dir, file)}")
            continue

        if file.endswith(".html"):
            try:
                print(f"  -> Processing HTML file {os.path.join(dir, file)}")
                p = NavHTMLParser()
                p.feed(open(os.path.join(dir, file), "rb").read().decode())
                p.close()

                match p.title:
                    case None:
                        print("     > No nav-title found")

                    case "":
                        html_files[os.path.join(dir[6:], file)] = ""

                    case _:
                        html_files[os.path.join(dir[6:], file)] = p.title

                if p.updates > 1:
                    print(
                        f"     > Warning: More than 1 nav-title tags found ({p.updates}), only the last one will be used."
                    )
            except Exception as e:
                print(f"     > Failed ({e})")

if html_files:
    with open("./www/nav.html", "wb") as f:
        f.write("<html><head><title>Navigation</title></head><body>".encode())
        for file, title in html_files.items():
            f.write(f'<div><a href="{file}">{html_escape(file)}</a>'.encode())
            if title:
                f.write(f"&#58; {html_escape(title)}".encode())
            f.write(f"</div>".encode())
        f.write(
            f'<div style="margin-top:8px">{sys.argv[-1]}</div></body></html>'.encode()
        )
    print(
        f"==> Generated nav.html file ({len(html_files.items())} {'item' if len(html_files.items()) == 1 else 'items'}, {os.path.getsize('./www/nav.html')} bytes)"
    )
