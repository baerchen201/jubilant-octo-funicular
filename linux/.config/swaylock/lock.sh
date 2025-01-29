#!/bin/bash

# Discord status
systemctl --user start discordidle.service &

if [ -n "$1" ] && [ -n "$2" ]; then
  # Generate lock image based on first argument
  if ! [ -f "$2" ]; then
    magick "$1" -gaussian-blur "5x5" -colorize "75%" "$2"
  fi
  # Lock screen
  swaylock -i "$2"
else
  swaylock
fi

# Reset discord status
systemctl --user stop discordidle.service

exit 0
