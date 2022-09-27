"""jc - JSON Convert shell_completions module"""

from string import Template
from .cli_data import long_options_map
from .lib import all_parser_info


bash_template = Template('''\
_jc()
{
    local cur prev words cword jc_commands jc_parsers jc_options \\
          jc_about_options jc_about_mod_options jc_help_options jc_special_options

    jc_commands=(${bash_commands})
    jc_parsers=(${bash_parsers})
    jc_options=(${bash_options})
    jc_about_options=(${bash_about_options})
    jc_about_mod_options=(${bash_about_mod_options})
    jc_help_options=(${bash_help_options})
    jc_special_options=(${bash_special_options})

    COMPREPLY=()
    _get_comp_words_by_ref cur prev words cword

    # if jc_about_options are found anywhere in the line, then only complete from jc_about_mod_options
    for i in "$${words[@]::$${#words[@]}-1}"; do
        if [[ " $${jc_about_options[*]} " =~ " $${i} " ]]; then
            COMPREPLY=( $$( compgen -W "$${jc_about_mod_options[*]}" \\
            -- "$${cur}" ) )
            return 0
        fi
    done

    # if jc_help_options and a parser are found anywhere in the line, then no more completions
    if
        (
            for i in "$${words[@]::$${#words[@]}-1}"; do
                if [[ " $${jc_help_options[*]} " =~ " $${i} " ]]; then
                    return 0
                fi
            done
            return 1
        ) && (
            for i in "$${words[@]::$${#words[@]}-1}"; do
                if [[ " $${jc_parsers[*]} " =~ " $${i} " ]]; then
                    return 0
                fi
            done
            return 1
        ); then
        return 0
    fi

    # if jc_help_options are found anywhere in the line, then only complete with parsers
    for i in "$${words[@]::$${#words[@]}-1}"; do
        if [[ " $${jc_help_options[*]} " =~ " $${i} " ]]; then
            COMPREPLY=( $$( compgen -W "$${jc_parsers[*]}" \\
            -- "$${cur}" ) )
            return 0
        fi
    done

    # if special options are found anywhere in the line, then no more completions
    for i in "$${words[@]::$${#words[@]}-1}"; do
        if [[ " $${jc_special_options[*]} " =~ " $${i} " ]]; then
            return 0
        fi
    done

    # if magic command is found anywhere in the line, use called command's autocompletion
    for i in "$${words[@]::$${#words[@]}-1}"; do
        if [[ " $${jc_commands[*]} " =~ " $${i} " ]]; then
            _command
            return 0
        fi
    done

    # if "/pr[oc]" (magic for Procfile parsers) is in the current word, complete with files/directories in the path
    if [[ "$${cur}" =~ "/pr" ]]; then
        _filedir
        return 0
    fi

    # if a parser arg is found anywhere in the line, only show options and help options
    for i in "$${words[@]::$${#words[@]}-1}"; do
        if [[ " $${jc_parsers[*]} " =~ " $${i} " ]]; then
            COMPREPLY=( $$( compgen -W "$${jc_options[*]} $${jc_help_options[*]}" \\
            -- "$${cur}" ) )
            return 0
        fi
    done

    # default completion
    COMPREPLY=( $$( compgen -W "$${jc_options[*]} $${jc_about_options[*]} $${jc_help_options[*]} $${jc_special_options[*]} $${jc_parsers[*]} $${jc_commands[*]}" \\
        -- "$${cur}" ) )
} &&
complete -F _jc jc
''')


zsh_template = Template('''\
#compdef jc

_jc() {
    local -a jc_commands jc_commands_describe \\
             jc_parsers jc_parsers_describe \\
             jc_options jc_options_describe \\
             jc_about_options jc_about_options_describe \\
             jc_about_mod_options jc_about_mod_options_describe \\
             jc_help_options jc_help_options_describe \\
             jc_special_options jc_special_options_describe

    jc_commands=(${zsh_commands})
    jc_commands_describe=(
        ${zsh_commands_describe}
    )
    jc_parsers=(${zsh_parsers})
    jc_parsers_describe=(
        ${zsh_parsers_describe}
    )
    jc_options=(${zsh_options})
    jc_options_describe=(
        ${zsh_options_describe}
    )
    jc_about_options=(${zsh_about_options})
    jc_about_options_describe=(
        ${zsh_about_options_describe}
    )
    jc_about_mod_options=(${zsh_about_mod_options})
    jc_about_mod_options_describe=(
        ${zsh_about_mod_options_describe}
    )
    jc_help_options=(${zsh_help_options})
    jc_help_options_describe=(
        ${zsh_help_options_describe}
    )
    jc_special_options=(${zsh_special_options})
    jc_special_options_describe=(
        ${zsh_special_options_describe}
    )

    # if jc_about_options are found anywhere in the line, then only complete from jc_about_mod_options
    for i in $${words:0:-1}; do
        if (( $$jc_about_options[(Ie)$${i}] )); then
            _describe 'commands' jc_about_mod_options_describe
            return 0
        fi
    done

    # if jc_help_options and a parser are found anywhere in the line, then no more completions
     if
        (
            for i in $${words:0:-1}; do
                if (( $$jc_help_options[(Ie)$${i}] )); then
                    return 0
                fi
            done
            return 1
        ) && (
            for i in $${words:0:-1}; do
                if (( $$jc_parsers[(Ie)$${i}] )); then
                    return 0
                fi
            done
            return 1
        ); then
        return 0
    fi

    # if jc_help_options are found anywhere in the line, then only complete with parsers
    for i in $${words:0:-1}; do
        if (( $$jc_help_options[(Ie)$${i}] )); then
            _describe 'commands' jc_parsers_describe
            return 0
        fi
    done

    # if special options are found anywhere in the line, then no more completions
    for i in $${words:0:-1}; do
        if (( $$jc_special_options[(Ie)$${i}] )); then
            return 0
        fi
    done

    # if magic command is found anywhere in the line, use called command's autocompletion
    for i in $${words:0:-1}; do
        if (( $$jc_commands[(Ie)$${i}] )); then
            # hack to remove options between jc and the magic command
            shift $$(( $${#words} - 2 )) words
            words[1,0]=(jc)
            CURRENT=$${#words}

            # run the magic command's completions
            _arguments '*::arguments:_normal'
            return 0
        fi
    done

    # if "/pr[oc]" (magic for Procfile parsers) is in the current word, complete with files/directories in the path
    if [[ "$${words[-1]}" =~ "/pr" ]]; then
        # run files completion
        _files
        return 0
    fi

    # if a parser arg is found anywhere in the line, only show options and help options
    for i in $${words:0:-1}; do
        if (( $$jc_parsers[(Ie)$${i}] )); then
            _describe 'commands' jc_options_describe -- jc_help_options_describe
            return 0
        fi
    done

    # default completion
    _describe 'commands' jc_options_describe -- jc_about_options_describe -- jc_help_options_describe -- jc_special_options_describe -- jc_parsers_describe -- jc_commands_describe
}

_jc
''')

about_options = ['--about', '-a']
about_mod_options = ['--pretty', '-p', '--yaml-out', '-y', '--monochrome', '-m', '--force-color', '-C']
help_options = ['--help', '-h']
special_options = ['--version', '-v', '--bash-comp', '-B', '--zsh-comp', '-Z']

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


def get_parsers():
    p_list = []
    for cmd in all_parser_info(show_hidden=True):
        if 'argument' in cmd:
            p_list.append(cmd['argument'])

    return p_list


def get_parsers_descriptions():
    pd_list = []
    for p in all_parser_info(show_hidden=True):
        if 'description' in p:
            pd_list.append(f"'{p['argument']}:{p['description']}'")

    return pd_list


def get_zsh_command_descriptions(command_list):
    zsh_commands = []
    for cmd in command_list:
        zsh_commands.append(f"""'{cmd}:run "{cmd}" command with magic syntax.'""")

    return zsh_commands


def get_descriptions(opt_list):
    """Return a list of options:description items."""
    opt_desc_list = []

    for item in opt_list:
        # get long options
        if item in long_options_map:
            opt_desc_list.append(f"'{item}:{long_options_map[item][1]}'")
            continue

        # get short options
        for k, v in long_options_map.items():
            if item[1:] == v[0]:
                opt_desc_list.append(f"'{item}:{v[1]}'")
                continue

    return opt_desc_list


def bash_completion():
    parsers_str = ' '.join(get_parsers())
    opts_no_special = get_options()

    for s_option in special_options:
        opts_no_special.remove(s_option)

    for a_option in about_options:
        opts_no_special.remove(a_option)

    for h_option in help_options:
        opts_no_special.remove(h_option)

    options_str = ' '.join(opts_no_special)
    about_options_str = ' '.join(about_options)
    about_mod_options_str = ' '.join(about_mod_options)
    help_options_str = ' '.join(help_options)
    special_options_str = ' '.join(special_options)
    commands_str = ' '.join(get_commands())
    return bash_template.substitute(
        bash_parsers=parsers_str,
        bash_special_options=special_options_str,
        bash_about_options=about_options_str,
        bash_about_mod_options=about_mod_options_str,
        bash_help_options=help_options_str,
        bash_options=options_str,
        bash_commands=commands_str
    )


def zsh_completion():
    parsers_str = ' '.join(get_parsers())
    parsers_describe = '\n        '.join(get_parsers_descriptions())
    opts_no_special = get_options()

    for s_option in special_options:
        opts_no_special.remove(s_option)

    for a_option in about_options:
        opts_no_special.remove(a_option)

    for h_option in help_options:
        opts_no_special.remove(h_option)

    options_str = ' '.join(opts_no_special)
    options_describe = '\n        '.join(get_descriptions(opts_no_special))
    about_options_str = ' '.join(about_options)
    about_options_describe = '\n        '.join(get_descriptions(about_options))
    about_mod_options_str = ' '.join(about_mod_options)
    about_mod_options_describe = '\n        '.join(get_descriptions(about_mod_options))
    help_options_str = ' '.join(help_options)
    help_options_describe = '\n        '.join(get_descriptions(help_options))
    special_options_str = ' '.join(special_options)
    special_options_describe = '\n        '.join(get_descriptions(special_options))
    commands_str = ' '.join(get_commands())
    commands_describe = '\n        '.join(get_zsh_command_descriptions(get_commands()))

    return zsh_template.substitute(
        zsh_parsers=parsers_str,
        zsh_parsers_describe=parsers_describe,
        zsh_special_options=special_options_str,
        zsh_special_options_describe=special_options_describe,
        zsh_about_options=about_options_str,
        zsh_about_options_describe=about_options_describe,
        zsh_about_mod_options=about_mod_options_str,
        zsh_about_mod_options_describe=about_mod_options_describe,
        zsh_help_options=help_options_str,
        zsh_help_options_describe=help_options_describe,
        zsh_options=options_str,
        zsh_options_describe=options_describe,
        zsh_commands=commands_str,
        zsh_commands_describe=commands_describe
    )
