# Check for interactive mode
if [[ $- == *i* ]]; then
	# Load user preferences
	if [ -f ~/.bash_preferences ]; then source ~/.bash_preferences; fi


	# Welcome message
	if ! [ "$hide_welcome_message" = "1" ]; then
		if ! (( $SHLVL > 1 )); then
			clear
			echo "Welcome, $USER!"
		fi
		date "+%A %d. %B %Y - %H:%M"
		echo -en "bash $(if ! [ ${BASH_VERSINFO[4]} = "release" ];then echo "${BASH_VERSINFO[4]} ";fi )${BASH_VERSINFO[0]}.${BASH_VERSINFO[1]}\e[90m.${BASH_VERSINFO[2]}.${BASH_VERSINFO[3]}\e[0m"
		if (( $SHLVL > 1 )); then echo -e " - nested level $(( $SHLVL - 1 ))"; else echo ""; fi
	fi


	# Command counter
	_COMMANDS=-1
	PROMPT_COMMAND="let _COMMANDS++"


	# Set up prompt
	_exitcode () {
		if ! [ $_COMMANDS = 0 ]; then 
			if [ $1 = 0 ]; then
				if ! [ "$display_zero_exitcode" = "1" ]; then return 0; fi
				echo -en "\e[90m"
			else
				echo -en "\e[1;91m"
			fi

			echo -en "Process exited with code $1\n\u200B"
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
\$(_exitcode \$?)\
\e[91m\u\e[33m@\e[34m\H\e[0m \
\$(_pWd)\
\$(_suffix)"


	# Git aliases
	_git_addandcommit () {
		if git add $@; then
			git commit
		fi
	}
	if ! [ "$disable_git_aliases" = "1" ]; then
		alias yeet="git push"
		alias yoink="git pull"
		alias yikes="git reset --hard"
		alias yes=_git_addandcommit
		alias yo="git status"
		alias yaa="git push -f"
	fi
fi
