"""jc - JSON Convert shell_completions module"""

from string import Template
from .cli_data import long_options_map
from .lib import all_parser_info


bash_template = Template('''\
_jc()
{
    local cur prev words cword jc_commands jc_parsers jc_options

    jc_commands=(${bash_commands})
    jc_parsers=(${bash_arguments})
    jc_options=(${bash_options})

    COMPREPLY=()
    _get_comp_words_by_ref cur prev words cword

    # if magic command is found anywhere in the line, use called command's autocompletion
    for i in "$${words[@]}"; do
        if [[ " $${jc_commands[*]} " =~ " $${i} " ]]; then
            _command
            return 0
        fi
    done

    # if a parser arg is found anywhere in the line, only show options
    for i in "$${words[@]}"; do
        if [[ " $${jc_parsers[*]} " =~ " $${i} " ]]; then
            COMPREPLY=( $$( compgen -W "$${jc_options[*]}" \\
            -- "$${cur}" ) )
           return 0
        fi
    done

    # default completion
    COMPREPLY=( $$( compgen -W "$${jc_options[*]} $${jc_parsers[*]} $${jc_commands[*]}" \\
        -- "$${cur}" ) )
} &&
complete -F _jc jc
''')


zsh_template = Template('''\
#compdef jc

_jc() {
  # autogenerate completions based on jc --help output
  _arguments --

  # add commands supported by magic syntax
  local -a commands
  commands=(
    # e.g. 'arp:run arp with magic syntax.'
    ${zsh_commands}
  )

  _describe -t commands 'commands' commands
  return 0
}

_jc
''')


def get_commands():
    command_list = []
    for cmd in all_parser_info():
        if 'magic_commands' in cmd:
            command_list.extend(cmd['magic_commands'])

    return sorted(list(set([i.split()[0] for i in command_list])))


def get_options():
    options_list = []
    for opt in long_options_map:
        options_list.append(opt)
        options_list.append('-' + long_options_map[opt][0])

    return options_list


def get_arguments():
    arg_list = []
    for cmd in all_parser_info():
        if 'argument' in cmd:
            arg_list.append(cmd['argument'])

    return arg_list


def gen_zsh_command_descriptions(command_list):
    zsh_commands = []
    for cmd in command_list:
        zsh_commands.append(f"""'{cmd}:run "{cmd}" command with magic syntax.'""")

    return zsh_commands


def bash_completion():
    args = ' '.join(get_arguments())
    options = ' '.join(get_options())
    commands = ' '.join(get_commands())
    return bash_template.substitute(bash_arguments=args,
                                    bash_options=options,
                                    bash_commands=commands)


def zsh_completion():
    commands = '\n    '.join(gen_zsh_command_descriptions(get_commands()))
    return zsh_template.substitute(zsh_commands=commands)
