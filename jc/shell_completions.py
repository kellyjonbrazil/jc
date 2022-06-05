"""jc - JSON Convert shell_completions module"""

from string import Template
from .cli_data import long_options_map
from .lib import all_parser_info

# $(jc -a | jq -r '.parsers[] | .argument, .magic_commands[]?')
bash_template = Template('''\
complete -W "${bash_arguments}${bash_options}${bash_commands}" jc
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

    return list(set([i.split()[0] for i in command_list]))


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
    args = '\n'.join(get_arguments())
    options = '\n' + '\n'.join(get_options())
    commands = '\n' + '\n'.join(get_commands())
    return bash_template.substitute(bash_arguments=args,
                                    bash_options=options,
                                    bash_commands=commands)


def zsh_completion():
    commands = '\n    '.join(gen_zsh_command_descriptions(get_commands()))
    return zsh_template.substitute(zsh_commands=commands)
