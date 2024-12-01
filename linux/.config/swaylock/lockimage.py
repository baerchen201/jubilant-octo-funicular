import os
from PIL import Image, ImageEnhance, ImageFilter

i = Image.open(os.path.expanduser("~/.config/hypr/wallpaper.png"))

i = ImageEnhance.Brightness(i).enhance(0.3)
i = i.filter(ImageFilter.GaussianBlur(4))

i.save(os.path.expanduser("~/.config/swaylock/lock.png"), format="png")
