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
    version = '1.7.5'
    description = 'jc cli output JSON conversion tool'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'


__version__ = info.version

parsers = [
    'arp',
    'crontab',
    'crontab-u',
    'df',
    'dig',
    'du',
    'env',
    'free',
    'fstab',
    'history',
    'hosts',
    'id',
    'ifconfig',
    'ini',
    'iptables',
    'jobs',
    'ls',
    'lsblk',
    'lsmod',
    'lsof',
    'mount',
    'netstat',
    'pip-list',
    'pip-show',
    'ps',
    'route',
    'ss',
    'stat',
    'systemctl',
    'systemctl-lj',
    'systemctl-ls',
    'systemctl-luf',
    'uname',
    'uptime',
    'w',
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

            or

            COMMAND | jc [OPTIONS] PARSER

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


def magic():
    """Parse with magic syntax: jc -p ls -al"""
    if len(sys.argv) > 1 and not sys.argv[1].startswith('--'):
        parser_info = about_jc()['parsers']
        # correctly parse escape characters and spaces with shlex
        args_given = " ".join(map(shlex.quote, sys.argv[1:])).split()
        options = []
        found_parser = None

        # find the options
        if args_given[0].startswith('-'):
            p = 0
            for i, arg in list(enumerate(args_given)):
                # parser found - use standard syntax
                if arg.startswith('--'):
                    return
                # option found - populate option list
                elif arg.startswith('-'):
                    options.append(args_given.pop(i - p)[1:])
                    p = p + 1
                # command found if iterator didn't already stop - stop iterating
                else:
                    break

        # find the command and parser
        for parser in parser_info:
            if 'magic_commands' in parser:
                # first pass for two word commands: e.g. 'pip list'
                for magic_command in parser['magic_commands']:
                    try:
                        if ' '.join(args_given[0:2]) == magic_command:
                            found_parser = parser['argument']
                            break
                    # No command found - go to next loop (for cases like 'jc -a')
                    except Exception:
                        break

                # second pass for one word commands: e.g. 'ls'
                if not found_parser:
                    for magic_command in parser['magic_commands']:
                        try:
                            if args_given[0] == magic_command:
                                found_parser = parser['argument']
                                break
                        # No command found - use standard syntax (for cases like 'jc -a')
                        except Exception:
                            return

        # construct a new command line using the standard syntax: COMMAND | jc --PARSER -OPTIONS
        run_command = ' '.join(args_given)
        if found_parser:
            if options:
                cmd_options = '-' + ''.join(options)
            else:
                cmd_options = ''
            whole_command = ' '.join([run_command, '|', 'jc', found_parser, cmd_options])

            os.system(whole_command)
            exit()
        else:
            helptext(f'parser not found for "{run_command}"')
            sys.exit(1)


def main():
    # break on ctrl-c keyboard interrupt
    signal.signal(signal.SIGINT, ctrlc)

    # try magic syntax first: e.g. jc -p ls -al
    magic()

    options = []
    debug = False
    pretty = False
    quiet = False
    raw = False

    # options
    for opt in sys.argv:
        if opt.startswith('-') and not opt.startswith('--'):
            for flag in opt[1:]:
                options.append(flag)

    if 'd' in options:
        debug = True

    if 'p' in options:
        pretty = True

    if 'q' in options:
        quiet = True

    if 'r' in options:
        raw = True

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
                    jc.utils.error_message(f'{parser_name} parser could not parse the input data. Did you use the correct parser?\n         For details use the -d option.')
                    sys.exit(1)

    if not found:
        helptext('missing or incorrect arguments')
        sys.exit(1)

    json_out(result, pretty=pretty)


if __name__ == '__main__':
    main()
