#!/usr/bin/env bash
sudo flatpak override --filesystem=$HOME/.themes
sudo flatpak override --filesystem=$HOME/.icons
sudo flatpak override --env=GTK_THEME=breeze_dark
sudo flatpak override --env=ICON_THEME=breeze_dark
