import os
import shutil

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
