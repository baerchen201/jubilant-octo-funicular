import os

for dir, subdirs, files in os.walk(os.path.dirname(__file__)):
    for file in files:
        os.replace(
            os.path.join(dir, file),
            os.path.join(dir, file.removesuffix("___format__.html")),
        )
