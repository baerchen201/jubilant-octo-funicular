#!/bin/bash

# Discord status
python3 /usr/local/bin/setdiscordstatus.py -id "$(dirname $0)/discordstatus.json" -s idle

# Lock screen
swaylock -c "$(dirname $0)/config"

# Reset discord status
python3 /usr/local/bin/setdiscordstatus.py -ir "$(dirname $0)/discordstatus.json" -s online
