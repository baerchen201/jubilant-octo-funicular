#
# ~/.bash_profile
#

if uwsm check may-start; then
  exec uwsm start hyprland.desktop
fi

export TERM="linux"

[[ -f ~/.bashrc ]] && . ~/.bashrc
