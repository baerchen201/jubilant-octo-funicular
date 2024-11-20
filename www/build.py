import os
import shutil
import sys

from html import escape as html_escape

if sys.argv[-1] != "":
    with open("./www/commit.html", "wb") as f:
        f.write(
            f'<html><head><title>Latest deployment</title><link rel="stylesheet" href="css/global.css" /></head><body style="font-size: 40px" >{html_escape(sys.argv[-1])}</body></html>'.encode()
        )

from html.parser import HTMLParser


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
                self.title = dict_attrs.get("content", "")
                if self.title is None:
                    self.title = ""

                self.updates += 1
                print(f"     > Found nav-title {self.title}")


nav_files = {}
nav_status = {"failure": 0, "success": 0}

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
                        nav_files[os.path.join(dir[6:], file)] = ""

                    case _:
                        nav_files[os.path.join(dir[6:], file)] = p.title

                if p.updates > 1:
                    print(
                        f"     > Warning: More than 1 nav-title tags found ({p.updates}), only the last one will be used."
                    )
                nav_status["success"] += 1
            except Exception as e:
                nav_status["failure"] += 1
                print(f"     > Failed ({e})")

with open("./www/nav.html", "wb") as f:
    f.write(
        '<html><head><title>Navigation</title><link rel="stylesheet" href="css/global.css" /></head><body>'.encode()
    )
    if nav_files:
        for file, title in nav_files.items():
            f.write(f'<div><a href="{file}">{html_escape(file)}</a>'.encode())
            if title:
                f.write(f"&#58; {html_escape(title)}".encode())
            f.write(f"</div>".encode())
    else:
        f.write(f"<h1>Hello, World!</h1>".encode())
    f.write(
        f'<div style="margin-top:8px"><img style="width: 75px" src="secret.gif" /></div></body></html>'.encode()
    )

    print(
        f"==> Generated nav.html file ({len(nav_files.items())} {'item' if len(nav_files.items()) == 1 else 'items'}, {os.path.getsize('./www/nav.html')} bytes)"
    )
e = 0
if nav_status["failure"] > 0 and nav_status["success"] < nav_status["failure"]:
    e = 1


os.remove(__file__)
raise SystemExit(e)
