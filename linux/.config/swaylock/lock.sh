#!/bin/bash

# Discord status
systemctl --user start discordidle.service &

# Generate lock image based on first argument
(
  if ! [ -f "$1" ]; then
    exit 1
  fi

  _sha=$(sha1sum "$1")
  if ! [ "$?" = "0" ]; then exit 1; fi

  _cat=$(cat "/tmp/${USER}_$(basename "$1")_sha")

  if ! [ "$_sha" = "$_cat" ]; then
    echo "$_sha" > "/tmp/${USER}_$(basename "$1")_sha"
    rm -f ~/.config/swaylock/lock.png
    python3 ~/.config/swaylock/lockimage.py "$1" ~/.config/swaylock/lock.png
    exit "$?"
  fi
  exit 0
)

# Lock screen
if [ "$?" = "0" ]; then
  swaylock
else
  swaylock -C "/dev/null"
fi

# Reset discord status
systemctl --user stop discordidle.service

exit 0
