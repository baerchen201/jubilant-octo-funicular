import os

for dir, subdirs, files in os.walk("."):
    for file in files:
        if file.endswith(".html") or file.endswith(".php"):
            os.replace(
                os.path.join(dir, file), os.path.join(dir, file + "___format__.html")
            )
