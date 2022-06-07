"""jc - JSON Convert shell_completions module"""

from string import Template
from .cli_data import long_options_map
from .lib import all_parser_info


bash_template = Template('''\
_jc()
{
    local cur prev words cword jc_commands jc_parsers jc_options jc_special_options

    jc_commands=(${bash_commands})
    jc_parsers=(${bash_arguments})
    jc_options=(${bash_options})
    jc_special_options=(${bash_special_opts})

    COMPREPLY=()
    _get_comp_words_by_ref cur prev words cword

    # if special options are found anywhere in the line, then no more completions
    for i in "$${words[@]}"; do
        if [[ " $${jc_special_options[*]} " =~ " $${i} " ]]; then
            return 0
        fi
    done

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
    COMPREPLY=( $$( compgen -W "$${jc_options[*]} $${jc_special_options[*]} $${jc_parsers[*]} $${jc_commands[*]}" \\
        -- "$${cur}" ) )
} &&
complete -F _jc jc
''')


zsh_template = Template('''\
#compdef jc

_jc() {

    # if magic command is found anywhere in the line, use called command's autocompletion

    # if a parser arg is found anywhere in the line, only show options

    # default completion
  # autogenerate completions based on jc --help output
  # _arguments --

  # add commands supported by magic syntax
  #   local -a commands
  #   commands=(
  #     # e.g. 'arp:run arp with magic syntax.'
  #     ${zsh_commands}
  #   )

  #   _describe -t commands 'commands' commands
  #   return 0
}

_jc
''')

special_options = ['--about', '-a', '--version', '-v', '--bash-comp', '-B', '--zsh-comp', '-Z']

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
    opts_no_special = get_options()
    for option in special_options:
        opts_no_special.remove(option)
    options = ' '.join(opts_no_special)
    s_options = ' '.join(special_options)
    commands = ' '.join(get_commands())
    return bash_template.substitute(bash_arguments=args,
                                    bash_special_opts=s_options,
                                    bash_options=options,
                                    bash_commands=commands)


def zsh_completion():
    commands = '\n    '.join(gen_zsh_command_descriptions(get_commands()))
    return zsh_template.substitute(zsh_commands=commands)
