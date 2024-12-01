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

  _cat=$(cat "/tmp/${USER}_wall_sha")

  if ! [ -f "~/.config/swaylock/lock.png" ] || [ "$_sha" != "$_cat" ]; then
    echo "$_sha" > "/tmp/${USER}_wall_sha"
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
