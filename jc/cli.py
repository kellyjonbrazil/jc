#!/usr/bin/env python3
"""jc - JSON CLI output utility
JC cli module
"""
import sys
import os
import shlex
import importlib
import textwrap
import signal
import json
import jc.utils


class info():
    version = '1.9.3'
    description = 'jc cli output JSON conversion tool'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'


__version__ = info.version

parsers = [
    'airport',
    'airport-s',
    'arp',
    'blkid',
    'crontab',
    'crontab-u',
    'csv',
    'df',
    'dig',
    'du',
    'env',
    'file',
    'free',
    'fstab',
    'group',
    'gshadow',
    'history',
    'hosts',
    'id',
    'ifconfig',
    'ini',
    'iptables',
    'jobs',
    'last',
    'ls',
    'lsblk',
    'lsmod',
    'lsof',
    'mount',
    'netstat',
    'ntpq',
    'passwd',
    'pip-list',
    'pip-show',
    'ps',
    'route',
    'shadow',
    'ss',
    'stat',
    'systemctl',
    'systemctl-lj',
    'systemctl-ls',
    'systemctl-luf',
    'timedatectl',
    'uname',
    'uptime',
    'w',
    'who',
    'xml',
    'yaml'
]


def ctrlc(signum, frame):
    """exit with error on SIGINT"""
    sys.exit(1)


def parser_shortname(parser_argument):
    """short name of the parser with dashes and no -- prefix"""
    return parser_argument[2:]


def parser_argument(parser):
    """short name of the parser with dashes and with -- prefix"""
    return f'--{parser}'


def parser_mod_shortname(parser):
    """short name of the parser's module name (no -- prefix and dashes converted to underscores)"""
    return parser.replace('--', '').replace('-', '_')


def parser_module(parser):
    """import the module just in time and return the module object"""
    importlib.import_module('jc.parsers.' + parser_mod_shortname(parser))
    return getattr(jc.parsers, parser_mod_shortname(parser))


def parsers_text(indent=0, pad=0):
    """return the argument and description information from each parser"""
    ptext = ''
    for parser in parsers:
        parser_arg = parser_argument(parser)
        parser_mod = parser_module(parser)

        if hasattr(parser_mod, 'info'):
            parser_desc = parser_mod.info.description
            padding = pad - len(parser_arg)
            padding_char = ' '
            indent_text = padding_char * indent
            padding_text = padding_char * padding
            ptext += indent_text + parser_arg + padding_text + parser_desc + '\n'

    return ptext


def about_jc():
    """return jc info and the contents of each parser.info as a dictionary"""
    parser_list = []

    for parser in parsers:
        parser_mod = parser_module(parser)

        if hasattr(parser_mod, 'info'):
            info_dict = {}
            info_dict['name'] = parser_mod.__name__.split('.')[-1]
            info_dict['argument'] = parser_argument(parser)
            parser_entry = vars(parser_mod.info)

            for k, v in parser_entry.items():
                if not k.startswith('__'):
                    info_dict[k] = v

        parser_list.append(info_dict)

    return {
        'name': 'jc',
        'version': info.version,
        'description': info.description,
        'author': info.author,
        'author_email': info.author_email,
        'parser_count': len(parser_list),
        'parsers': parser_list
    }


def helptext(message):
    """return the help text with the list of parsers"""
    parsers_string = parsers_text(indent=12, pad=17)

    helptext_string = f'''
    jc:     {message}

    Usage:  COMMAND | jc PARSER [OPTIONS]

            or magic syntax:

            jc [OPTIONS] COMMAND

    Parsers:
{parsers_string}
    Options:
            -a               about jc
            -d               debug - show trace messages
            -p               pretty print output
            -q               quiet - suppress warnings
            -r               raw JSON output

    Example:
            ls -al | jc --ls -p

            or using the magic syntax:

            jc -p ls -al
    '''
    print(textwrap.dedent(helptext_string), file=sys.stderr)


def json_out(data, pretty=False):
    if pretty:
        print(json.dumps(data, indent=2))
    else:
        print(json.dumps(data))


def generate_magic_command(args):
    """
    Returns a tuple with a boolean and a command, where the boolean signifies that
    the command is valid, and the command is either a command string or None.
    """

    # Parse with magic syntax: jc -p ls -al
    if len(args) <= 1 or args[1].startswith('--'):
        return False, None

    # correctly parse escape characters and spaces with shlex
    args_given = ' '.join(map(shlex.quote, args[1:])).split()
    options = []

    # find the options
    for arg in list(args_given):
        # parser found - use standard syntax
        if arg.startswith('--'):
            return False, None

        # option found - populate option list
        elif arg.startswith('-'):
            options.extend(args_given.pop(0)[1:])

        # command found if iterator didn't already stop - stop iterating
        else:
            break

    # all options popped and no command found - for case like 'jc -a'
    if len(args_given) == 0:
        return False, None

    magic_dict = {}
    parser_info = about_jc()['parsers']

    # Create a dictionary of magic_commands to their respective parsers.
    for entry in parser_info:
        # Update the dict with all of the magic commands for this parser, if they exist.
        magic_dict.update({mc: entry['argument'] for mc in entry.get('magic_commands', [])})

    # find the command and parser
    one_word_command = args_given[0]
    two_word_command = ' '.join(args_given[0:2])

    # Try to get a parser for two_word_command, otherwise get one for one_word_command
    found_parser = magic_dict.get(two_word_command, magic_dict.get(one_word_command))

    # construct a new command line using the standard syntax: COMMAND | jc --PARSER -OPTIONS
    run_command = ' '.join(args_given)
    if found_parser:
        cmd_options = ('-' + ''.join(options)) if options else ''
        return True, ' '.join([run_command, '|', 'jc', found_parser, cmd_options])
    else:
        return False, run_command


def magic():
    valid_command, run_command = generate_magic_command(sys.argv)
    if valid_command:
        os.system(run_command)
        exit()
    elif run_command is None:
        return
    else:
        helptext(f'parser not found for "{run_command}"')
        sys.exit(1)


def main():
    # break on ctrl-c keyboard interrupt
    signal.signal(signal.SIGINT, ctrlc)

    # try magic syntax first: e.g. jc -p ls -al
    magic()

    options = []

    # options
    for opt in sys.argv:
        if opt.startswith('-') and not opt.startswith('--'):
            options.extend(opt[1:])

    debug = 'd' in options
    pretty = 'p' in options
    quiet = 'q' in options
    raw = 'r' in options

    if 'a' in options:
        json_out(about_jc(), pretty=pretty)
        exit()

    if sys.stdin.isatty():
        helptext('missing piped data')
        sys.exit(1)

    data = sys.stdin.read()

    found = False

    if debug:
        for arg in sys.argv:
            parser_name = parser_shortname(arg)

            if parser_name in parsers:
                # load parser module just in time so we don't need to load all modules
                parser = parser_module(arg)
                result = parser.parse(data, raw=raw, quiet=quiet)
                found = True
                break
    else:
        for arg in sys.argv:
            parser_name = parser_shortname(arg)

            if parser_name in parsers:
                # load parser module just in time so we don't need to load all modules
                parser = parser_module(arg)
                try:
                    result = parser.parse(data, raw=raw, quiet=quiet)
                    found = True
                    break
                except Exception:
                    jc.utils.error_message(
                        f'{parser_name} parser could not parse the input data. Did you use the correct parser?\n         For details use the -d option.')
                    sys.exit(1)

    if not found:
        helptext('missing or incorrect arguments')
        sys.exit(1)

    json_out(result, pretty=pretty)


if __name__ == '__main__':
    main()
