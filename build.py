import os
import shutil

from html.parser import HTMLParser


class _HTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("HTML Tag:", tag, attrs, sep="\n  ")


for dir, subdirs, files in os.walk("./www"):
    if (not subdirs and not files) or (
        all([file.startswith(".") for file in files])
        and all([subdir.startswith(".") for subdir in subdirs])
    ):
        shutil.rmtree(dir)
        continue

    for file in files:
        if file.startswith(".") or file.endswith(".ts"):
            os.remove(os.path.join(dir, file))
            continue

        if file.endswith(".html"):
            try:
                p = _HTMLParser()
                p.feed(open(os.path.join(dir, file), "rb").read().decode())
                p.close()
                print(os.path.join(dir, file), "SUCCESS")
            except Exception as e:
                print(os.path.join(dir, file), e)
