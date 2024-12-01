#!/bin/bash

# Discord status
systemctl --user start discordidle.service &

# Generate lock image
(
  _sha=$(sha1sum ~/.config/hypr/wallpaper.png)
  if ! [ "$?" = "0" ]; then exit 1; fi

  _cat=$(cat "/tmp/${USER}_wallpaper_sha")

  if ! [ "$_sha" = "$_cat" ]; then
    echo "$_sha" > "/tmp/${USER}_wallpaper_sha"
    rm -f ~/.config/swaylock/lock.png
    python3 ~/.config/swaylock/lockimage.py
    exit "$?"
  fi
  exit 0
)

# Lock screen
if [ "$?" = "0" ]; then
  swaylock -C "$(dirname $0)/config"
else
  swaylock -C "/dev/null"
fi

# Reset discord status
systemctl --user stop discordidle.service

exit 0
