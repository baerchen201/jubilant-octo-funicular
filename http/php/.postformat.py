import os
import re

for dir, subdirs, files in os.walk(os.path.dirname(__file__)):
    for file in files:
        if file.endswith(".php___format__.html"):
            with open(os.path.join(dir, file), "rb") as f:
                php = f.read().decode()
            php = re.sub(r"[ \t]*<\?php", "<?php", php)
            with open(os.path.join(dir, file), "wb") as f:
                f.write(php.encode())

        os.replace(
            os.path.join(dir, file),
            os.path.join(dir, file.removesuffix("___format__.html")),
        )
