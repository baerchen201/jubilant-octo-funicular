#!/bin/bash

# Discord status
systemctl --user start discordidle.service &

# Lock screen
swaylock -c "$(dirname $0)/config"

# Reset discord status
systemctl --user stop discordidle.service

exit 0
