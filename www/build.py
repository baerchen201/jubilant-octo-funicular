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

    def handle_starttag(self, tag, attrs):
        print("  HTML Tag:", tag, attrs, sep="\n    ")
        if tag == "meta":
            for attr in attrs:
                if attr[0] == "nav-title":
                    self.title = attr[1] if attr[1] else None


html_files = {}

for dir, subdirs, files in os.walk("./www"):
    if (not subdirs and not files) or (
        all([file.startswith(".") for file in files])
        and all([subdir.startswith(".") for subdir in subdirs])
    ):
        shutil.rmtree(dir)
        continue

    if os.path.isfile(os.path.join(dir, ".rm")):
        for file in [
            os.path.join(dir, i.strip())
            for i in open(os.path.join(dir, ".rm"), "r").read().strip().splitlines()
        ]:
            if os.path.isdir(file):
                shutil.rmtree(file)
            elif os.path.isfile(file):
                os.remove(file)

    for file in files:
        if file.startswith(".") or file.endswith(".ts"):
            os.remove(os.path.join(dir, file))
            continue

        if file.endswith(".html"):
            try:
                print(os.path.join(dir, file), "START")
                p = NavHTMLParser()
                p.feed(open(os.path.join(dir, file), "rb").read().decode())
                p.close()
                html_files[os.path.join(dir[6:], file)] = p.title
                print(os.path.join(dir, file), "SUCCESS")
            except Exception as e:
                print(os.path.join(dir, file), e)

if html_files:
    with open("./www/nav.html", "wb") as f:
        f.write("<html><head><title>Navigation</title></head><body>".encode())
        for file, title in html_files.items():
            f.write(f'<div><a href="{file}">{html_escape(file)}</a>'.encode())
            if title:
                f.write(f"&#58; {html_escape(title)}".encode())
            f.write(f"</div>".encode())
        f.write(
            f'<div style="margin-top:8px">{html_escape(sys.argv[-1])}</div></body></html>'.encode()
        )
