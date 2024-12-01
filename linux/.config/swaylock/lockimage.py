import argparse

argparser = argparse.ArgumentParser(
    prog="lockimage.py", description="lockscreen image generator"
)
argparser.add_argument("imagein", type=argparse.FileType("rb"))
argparser.add_argument("imageout", type=argparse.FileType("wb"))
args = argparser.parse_args()

import os
from PIL import Image, ImageEnhance, ImageFilter

i = Image.open(args.imagein)
i = i.convert("RGBA")

i = ImageEnhance.Brightness(i).enhance(0.3)
i = i.filter(ImageFilter.GaussianBlur(4))

i.save(args.imageout, format=args.imageout.name.split(".")[-1])
