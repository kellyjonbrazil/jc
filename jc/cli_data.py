"""jc - JSON Convert cli_data module"""
from typing import List, Dict

long_options_map: Dict[str, List[str]] = {
    '--about': ['a', 'about jc'],
    '--force-color': ['C', 'force color output even when using pipes (overrides -m)'],
    '--debug': ['d', 'debug (double for verbose debug)'],
    '--help': ['h', 'help (--help --parser_name for parser documentation)'],
    '--monochrome': ['m', 'monochrome output'],
    '--pretty': ['p', 'pretty print output'],
    '--quiet': ['q', 'suppress warnings (double to ignore streaming errors)'],
    '--raw': ['r', 'raw output'],
    '--unbuffer': ['u', 'unbuffer output'],
    '--version': ['v', 'version info'],
    '--yaml-out': ['y', 'YAML output'],
    '--bash-comp': ['B', 'gen Bash completion: jc -B > /etc/bash_completion.d/jc'],
    '--zsh-comp': ['Z', 'gen Zsh completion: jc -Z > "${fpath[1]}/_jc"']
}

new_pygments_colors = {
    'black': 'ansiblack',
    'red': 'ansired',
    'green': 'ansigreen',
    'yellow': 'ansiyellow',
    'blue': 'ansiblue',
    'magenta': 'ansimagenta',
    'cyan': 'ansicyan',
    'gray': 'ansigray',
    'brightblack': 'ansibrightblack',
    'brightred': 'ansibrightred',
    'brightgreen': 'ansibrightgreen',
    'brightyellow': 'ansibrightyellow',
    'brightblue': 'ansibrightblue',
    'brightmagenta': 'ansibrightmagenta',
    'brightcyan': 'ansibrightcyan',
    'white': 'ansiwhite',
}

old_pygments_colors = {
    'black': '#ansiblack',
    'red': '#ansidarkred',
    'green': '#ansidarkgreen',
    'yellow': '#ansibrown',
    'blue': '#ansidarkblue',
    'magenta': '#ansipurple',
    'cyan': '#ansiteal',
    'gray': '#ansilightgray',
    'brightblack': '#ansidarkgray',
    'brightred': '#ansired',
    'brightgreen': '#ansigreen',
    'brightyellow': '#ansiyellow',
    'brightblue': '#ansiblue',
    'brightmagenta': '#ansifuchsia',
    'brightcyan': '#ansiturquoise',
    'white': '#ansiwhite',
}
