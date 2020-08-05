"""jc - JSON CLI output utility
JC cli module
"""

import sys
import os
import os.path
import re
import shlex
import importlib
import textwrap
import signal
import json
import pygments
from pygments import highlight
from pygments.style import Style
from pygments.token import (Name, Number, String, Keyword)
from pygments.lexers import JsonLexer
from pygments.formatters import Terminal256Formatter
import jc.appdirs as appdirs


class info():
    version = '1.13.3'
    description = 'JSON CLI output utility'
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
    'date',
    'df',
    'dig',
    'dmidecode',
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
    'kv',
    'last',
    'ls',
    'lsblk',
    'lsmod',
    'lsof',
    'mount',
    'netstat',
    'ntpq',
    'passwd',
    'ping',
    'pip-list',
    'pip-show',
    'ps',
    'route',
    'shadow',
    'ss',
    'stat',
    'sysctl',
    'systemctl',
    'systemctl-lj',
    'systemctl-ls',
    'systemctl-luf',
    'timedatectl',
    'tracepath',
    'traceroute',
    'uname',
    'uptime',
    'w',
    'who',
    'xml',
    'yaml'
]

# List of custom or override parsers.
# Allow any <user_data_dir>/jc/jcparsers/*.py
local_parsers = []
data_dir = appdirs.user_data_dir('jc', 'jc')
local_parsers_dir = os.path.join(data_dir, 'jcparsers')
if os.path.isdir(local_parsers_dir):
    sys.path.append(data_dir)
    for name in os.listdir(local_parsers_dir):
        if re.match(r'\w+\.py', name) and os.path.isfile(os.path.join(local_parsers_dir, name)):
            plugin_name = name[0:-3]
            local_parsers.append(plugin_name)
            if plugin_name not in parsers:
                parsers.append(plugin_name)


# We only support 2.3.0+, pygments changed color names in 2.4.0.
# startswith is sufficient and avoids potential exceptions from split and int.
if pygments.__version__.startswith('2.3.'):
    PYGMENT_COLOR = {
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
else:
    PYGMENT_COLOR = {
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


def set_env_colors(env_colors=None):
    """
    Return a dictionary to be used in Pygments custom style class.

    Grab custom colors from JC_COLORS environment variable. JC_COLORS env variable takes 4 comma
    separated string values and should be in the format of:

    JC_COLORS=<keyname_color>,<keyword_color>,<number_color>,<string_color>

    Where colors are: black, red, green, yellow, blue, magenta, cyan, gray, brightblack, brightred,
                      brightgreen, brightyellow, brightblue, brightmagenta, brightcyan, white, default

    Default colors:

    JC_COLORS=blue,brightblack,magenta,green
    or
    JC_COLORS=default,default,default,default

    """
    input_error = False

    if env_colors:
        color_list = env_colors.split(',')
    else:
        color_list = ['default', 'default', 'default', 'default']

    if len(color_list) != 4:
        input_error = True

    for color in color_list:
        if color != 'default' and color not in PYGMENT_COLOR:
            input_error = True

    # if there is an issue with the env variable, just set all colors to default and move on
    if input_error:
        print('jc:   Warning: could not parse JC_COLORS environment variable\n', file=sys.stderr)
        color_list = ['default', 'default', 'default', 'default']

    # Try the color set in the JC_COLORS env variable first. If it is set to default, then fall back to default colors
    return {
        Name.Tag: f'bold {PYGMENT_COLOR[color_list[0]]}' if not color_list[0] == 'default' else f"bold {PYGMENT_COLOR['blue']}",   # key names
        Keyword: PYGMENT_COLOR[color_list[1]] if not color_list[1] == 'default' else PYGMENT_COLOR['brightblack'],                 # true, false, null
        Number: PYGMENT_COLOR[color_list[2]] if not color_list[2] == 'default' else PYGMENT_COLOR['magenta'],                      # numbers
        String: PYGMENT_COLOR[color_list[3]] if not color_list[3] == 'default' else PYGMENT_COLOR['green']                         # strings
    }


def piped_output():
    """Return False if stdout is a TTY. True if output is being piped to another program"""
    if sys.stdout.isatty():
        return False
    else:
        return True


def ctrlc(signum, frame):
    """Exit with error on SIGINT"""
    sys.exit(1)


def parser_shortname(parser_argument):
    """Return short name of the parser with dashes and no -- prefix"""
    return parser_argument[2:]


def parser_argument(parser):
    """Return short name of the parser with dashes and with -- prefix"""
    return f'--{parser}'


def parser_mod_shortname(parser):
    """Return short name of the parser's module name (no -- prefix and dashes converted to underscores)"""
    return parser.replace('--', '').replace('-', '_')


def parser_module(parser):
    """Import the module just in time and return the module object"""
    shortname = parser_mod_shortname(parser)
    path = ('jcparsers.' if shortname in local_parsers else 'jc.parsers.')
    return importlib.import_module(path + shortname)


def parsers_text(indent=0, pad=0):
    """Return the argument and description information from each parser"""
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
    """Return jc info and the contents of each parser.info as a dictionary"""
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
    """Return the help text with the list of parsers"""
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
            -d               debug - show traceback (-dd for verbose traceback)
            -m               monochrome output
            -p               pretty print output
            -q               quiet - suppress warnings
            -r               raw JSON output

    Example:
            ls -al | jc --ls -p

            or using the magic syntax:

            jc -p ls -al
    '''
    return textwrap.dedent(helptext_string)


def json_out(data, pretty=False, env_colors=None, mono=False, piped_out=False):
    """Return a JSON formatted string. String may include color codes or be pretty printed."""
    if not mono and not piped_out:
        # set colors
        class JcStyle(Style):
            styles = set_env_colors(env_colors)

        if pretty:
            return str(highlight(json.dumps(data, indent=2), JsonLexer(), Terminal256Formatter(style=JcStyle))[0:-1])
        else:
            return str(highlight(json.dumps(data), JsonLexer(), Terminal256Formatter(style=JcStyle))[0:-1])
    else:
        if pretty:
            return json.dumps(data, indent=2)
        else:
            return json.dumps(data)


def generate_magic_command(args):
    """
    Return a tuple with a boolean and a command, where the boolean signifies that
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

    # create a dictionary of magic_commands to their respective parsers.
    for entry in parser_info:
        # Update the dict with all of the magic commands for this parser, if they exist.
        magic_dict.update({mc: entry['argument'] for mc in entry.get('magic_commands', [])})

    # find the command and parser
    one_word_command = args_given[0]
    two_word_command = ' '.join(args_given[0:2])

    # try to get a parser for two_word_command, otherwise get one for one_word_command
    found_parser = magic_dict.get(two_word_command, magic_dict.get(one_word_command))

    # construct a new command line using the standard syntax: COMMAND | jc --PARSER -OPTIONS
    run_command = ' '.join(args_given)
    if found_parser:
        cmd_options = ('-' + ''.join(options)) if options else ''
        return True, ' '.join([run_command, '|', 'jc', found_parser, cmd_options])
    else:
        return False, run_command


def magic():
    """Runs the command generated by generate_magic_command() to support magic syntax"""
    valid_command, run_command = generate_magic_command(sys.argv)
    if valid_command:
        os.system(run_command)
        sys.exit(0)
    elif run_command is None:
        return
    else:
        print(helptext(f'parser not found for "{run_command}"'), file=sys.stderr)
        sys.exit(1)


def main():
    # break on ctrl-c keyboard interrupt
    signal.signal(signal.SIGINT, ctrlc)

    # break on pipe error. need try/except for windows compatibility
    try:
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except AttributeError:
        pass

    jc_colors = os.getenv('JC_COLORS')

    # try magic syntax first: e.g. jc -p ls -al
    magic()

    options = []

    # options
    for opt in sys.argv:
        if opt.startswith('-') and not opt.startswith('--'):
            options.extend(opt[1:])

    debug = 'd' in options
    verbose_debug = True if options.count('d') > 1 else False
    mono = 'm' in options
    pretty = 'p' in options
    quiet = 'q' in options
    raw = 'r' in options

    if verbose_debug:
        import jc.tracebackplus
        jc.tracebackplus.enable(context=11)

    if 'a' in options:
        print(json_out(about_jc(), pretty=pretty, env_colors=jc_colors, mono=mono, piped_out=piped_output()))
        sys.exit(0)

    if sys.stdin.isatty():
        print(helptext('missing piped data'), file=sys.stderr)
        sys.exit(1)

    data = sys.stdin.read()

    found = False

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
                if debug:
                    raise
                else:
                    import jc.utils
                    jc.utils.error_message(
                        f'{parser_name} parser could not parse the input data. Did you use the correct parser?\n'
                        '                 For details use the -d or -dd option.')
                    sys.exit(1)

    if not found:
        print(helptext('missing or incorrect arguments'), file=sys.stderr)
        sys.exit(1)

    print(json_out(result, pretty=pretty, env_colors=jc_colors, mono=mono, piped_out=piped_output()))


if __name__ == '__main__':
    main()
