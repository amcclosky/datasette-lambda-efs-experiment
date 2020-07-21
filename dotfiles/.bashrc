#!/bin/bash
export BASH_SILENCE_DEPRECATION_WARNING=1

DOTROOT="/project/dotfiles"

export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

export HISTFILESIZE=1000000
export HISTSIZE=1000000
export HISTCONTROL=ignoreboth
export HISTIGNORE='ls:bg:fg:history'
export HISTTIMEFORMAT='%F %T '

export PROMPT_COMMAND='history -a'

export VIRTUAL_ENV_DISABLE_PROMPT=1

export PATH="${DOTROOT}/bin:$PATH"

if [ -f ${DOTROOT}/bin/fancy_prompt.sh ]; then
    source ${DOTROOT}/bin/fancy_prompt.sh
fi

source ${DOTROOT}/.alias

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
