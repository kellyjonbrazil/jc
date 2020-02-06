#!/usr/bin/env python3
"""jc - JSON CLI output utility
JC cli module
"""
import sys
import importlib
import textwrap
import signal
import json
import jc.utils

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
    """import the module just in time and present the module object"""
    importlib.import_module('jc.parsers.' + parser_mod_shortname(parser))
    return getattr(jc.parsers, parser_mod_shortname(parser))


class info():
    version = '1.7.1'
    description = 'jc cli output JSON conversion tool'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'


__version__ = info.version


def ctrlc(signum, frame):
    sys.exit(1)


def parsers_text(indent=0, pad=0):
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
    parsers_string = parsers_text(indent=12, pad=17)

    helptext_string = f'''
    jc:     {message}

    Usage:  jc PARSER [OPTIONS]

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
    '''
    print(textwrap.dedent(helptext_string), file=sys.stderr)


def json_out(data, pretty=False):
    if pretty:
        print(json.dumps(data, indent=2))
    else:
        print(json.dumps(data))


def main():
    signal.signal(signal.SIGINT, ctrlc)

    debug = False
    pretty = False
    quiet = False
    raw = False

    # options
    if '-d' in sys.argv:
        debug = True

    if '-p' in sys.argv:
        pretty = True

    if '-q' in sys.argv:
        quiet = True

    if '-r' in sys.argv:
        raw = True

    if '-a' in sys.argv:
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
                except:
                    jc.utils.error_message(f'{parser_name} parser could not parse the input data. Did you use the correct parser?\n         For details use the -d option.')
                    sys.exit(1)

    if not found:
        helptext('missing or incorrect arguments')
        sys.exit(1)

    json_out(result, pretty=pretty)


if __name__ == '__main__':
    main()
