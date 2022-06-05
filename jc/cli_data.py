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
