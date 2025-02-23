#
# ~/.bash_profile
#

if [ `tty` = "/dev/tty1" ] && uwsm check may-start; then
  exec uwsm start hyprland.desktop
fi

export TERM="linux"

[[ -f ~/.bashrc ]] && . ~/.bashrc
