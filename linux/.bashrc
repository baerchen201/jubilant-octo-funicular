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
	export PS1="\e[0m\e[91m\u\e[33m@\e[34m\H\e[0m \$(if [ \"\$PWD\" = \"\$HOME\" ];then echo \"~\";else echo \"\$PWD\";fi)\e[2m>>\e[0m "
	export PS2="\e[2m>> \e[0m"
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

