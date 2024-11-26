#!/bin/bash

# Discord status
python3 /usr/local/bin/setdiscordstatus.py -id "$(dirname $0)/discordstatus.json" -s idle -t "afk" &

# Lock screen
swaylock -c "$(dirname $0)/config"
# Fallback if my dumbass didn't config correctly (idk i just found the idea cool)
if ! [ $? = 0 ]; then waylock; fi

# Wait for setdiscordstatus.py to exit (might fail if by some miracle python was fast but who cares i didn't set -e)
wait %1

# Reset discord status
python3 /usr/local/bin/setdiscordstatus.py -ir "$(dirname $0)/discordstatus.json" -s online -t ""
