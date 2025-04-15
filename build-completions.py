#!/usr/bin/env python3
# build Bash and Zsh completion scripts and add to the completions folder
from jc.shell_completions import bash_completion, zsh_completion

with open('completions/jc_bash_completion.sh', 'w') as f:
    print(bash_completion(), file=f)

with open('completions/jc_zsh_completion.sh', 'w') as f:
    print(zsh_completion(), file=f)
