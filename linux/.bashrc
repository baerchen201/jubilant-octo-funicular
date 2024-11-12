# Check for interactive mode
if [[ $- == *i* ]]; then
	# NEW: SMART Welcome message
	if ! (( $SHLVL > 1 )); then
		clear
		echo "Welcome, $USER!"
	fi
	date "+%A %d. %B %Y - %H:%M"
	echo -en "bash $(if ! [ ${BASH_VERSINFO[4]} = "release" ];then echo "${BASH_VERSINFO[4]} ";fi )${BASH_VERSINFO[0]}.${BASH_VERSINFO[1]}\e[90m.${BASH_VERSINFO[2]}.${BASH_VERSINFO[3]}\e[0m"
	if (( $SHLVL > 1 )); then echo -e " - nested level $(( $SHLVL - 1 ))"; else echo ""; fi
	
	# Set up prompt
	_exitcode () {
		if ! [ $LINENO = 0 ]; then 
			if [ $1 = 0 ]; then
				echo -en "\e[90m"
			fi;
			echo "Process exited with code $1"
		fi
	}
	_pWd () {
		if [ "$PWD" = "$HOME" ]; then
			echo "~"
		else
			echo "$PWD"
		fi
	}
	_suffix () { echo -en "\e[2m>> \e[0m"; }
	PS2="\$(_suffix)"
	PS1="\e[0m\
\$(_exitcode \$?)
\e[91m\u\e[33m@\e[34m\H\e[0m \
\$(_pWd)\
\$(_suffix)"

fi

# Git aliases
alias yeet="git push"
alias yoink="git pull"
alias yikes="git reset --hard"
yes () {
	if git add $@; then
		git commit
	fi
}
alias yo="git status"
alias yaa="git push -f"

