import sys
import subprocess
import os
import re

name = re.fullmatch(r"(.*)\..+", sys.argv[-1]).group(1)
print(name)
subprocess.Popen(
    ["ffmpeg", "-i", sys.argv[-1], "-map", "0:a", "-c:a", "libopus", name + ".tmp.webm"]
).wait()
os.remove(sys.argv[-1])
os.rename(name + ".tmp.webm", name + ".webm")
