#!/usr/bin/env bash
flatpak override --user --reset org.mozilla.firefox
flatpak override --user --filesystem=$HOME/.themes org.mozilla.firefox
flatpak override --user --filesystem=$HOME/.icons org.mozilla.firefox
flatpak override --user --env=GTK_THEME=Breeze-Dark org.mozilla.firefox
flatpak override --user --env=ICON_THEME=breeze_dark org.mozilla.firefox
