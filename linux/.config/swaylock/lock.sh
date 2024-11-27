#!/bin/bash

# Discord status
systemctl --user start discordidle.service &

# Lock screen
swaylock -c "$(dirname $0)/config"
# Fallback if my dumbass didn't config correctly (idk i just found the idea cool)
if ! [ $? = 0 ]; then waylock; fi

# Reset discord status
systemctl --user stop discordidle.service
