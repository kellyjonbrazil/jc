#!/usr/bin/env python3
"""jc - JSON CLI output utility
JC cli module
"""
import sys
import textwrap
import signal
import json
import jc.utils
import jc.parsers.arp
import jc.parsers.crontab
import jc.parsers.df
import jc.parsers.dig
import jc.parsers.du
import jc.parsers.env
import jc.parsers.free
import jc.parsers.fstab
import jc.parsers.history
import jc.parsers.hosts
import jc.parsers.ifconfig
import jc.parsers.iptables
import jc.parsers.jobs
import jc.parsers.ls
import jc.parsers.lsblk
import jc.parsers.lsmod
import jc.parsers.lsof
import jc.parsers.mount
import jc.parsers.netstat
import jc.parsers.pip_list
import jc.parsers.pip_show
import jc.parsers.ps
import jc.parsers.route
import jc.parsers.ss
import jc.parsers.stat
import jc.parsers.systemctl
import jc.parsers.systemctl_lj
import jc.parsers.systemctl_ls
import jc.parsers.systemctl_luf
import jc.parsers.uname
import jc.parsers.uptime
import jc.parsers.w

parser_map = {
    '--arp': jc.parsers.arp,
    '--crontab': jc.parsers.crontab,
    '--df': jc.parsers.df,
    '--dig': jc.parsers.dig,
    '--du': jc.parsers.du,
    '--env': jc.parsers.env,
    '--free': jc.parsers.free,
    '--fstab': jc.parsers.fstab,
    '--history': jc.parsers.history,
    '--hosts': jc.parsers.hosts,
    '--ifconfig': jc.parsers.ifconfig,
    '--iptables': jc.parsers.iptables,
    '--jobs': jc.parsers.jobs,
    '--ls': jc.parsers.ls,
    '--lsblk': jc.parsers.lsblk,
    '--lsmod': jc.parsers.lsmod,
    '--lsof': jc.parsers.lsof,
    '--mount': jc.parsers.mount,
    '--netstat': jc.parsers.netstat,
    '--pip-list': jc.parsers.pip_list,
    '--pip-show': jc.parsers.pip_show,
    '--ps': jc.parsers.ps,
    '--route': jc.parsers.route,
    '--ss': jc.parsers.ss,
    '--stat': jc.parsers.stat,
    '--systemctl': jc.parsers.systemctl,
    '--systemctl-lj': jc.parsers.systemctl_lj,
    '--systemctl-ls': jc.parsers.systemctl_ls,
    '--systemctl-luf': jc.parsers.systemctl_luf,
    '--uname': jc.parsers.uname,
    '--uptime': jc.parsers.uptime,
    '--w': jc.parsers.w
}


class info():
    version = '1.6.1'
    description = 'jc cli output JSON conversion tool'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'


def ctrlc(signum, frame):
    exit()


def parsers_text():
    ptext = ''
    for parser in parser_map:
        if hasattr(parser_map[parser], 'info'):
            padding = 16 - len(parser)
            padding_char = ' '
            padding_text = padding_char * padding
            ptext += '            ' + parser + padding_text + parser_map[parser].info.description + '\n'

    return ptext


def about_jc():
    parser_list = []
    for parser in parser_map:
        if hasattr(parser_map[parser], 'info'):
            info_dict = {}
            info_dict['name'] = parser_map[parser].__name__.split('.')[-1]
            info_dict['argument'] = parser
            parser_entry = vars(parser_map[parser].info)
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
    parsers_string = parsers_text()

    helptext_string = f'''
    jc:     {message}

    Usage:  jc PARSER [OPTIONS]

    Parsers:
{parsers_string}
    Options:
            -a              about jc
            -d              debug - show trace messages
            -p              pretty print output
            -q              quiet - suppress warnings
            -r              raw JSON output

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
        exit()

    data = sys.stdin.read()

    found = False

    if debug:
        for arg in sys.argv:
            if arg in parser_map:
                result = parser_map[arg].parse(data, raw=raw, quiet=quiet)
                found = True
                break
    else:
        for arg in sys.argv:
            if arg in parser_map:
                try:
                    result = parser_map[arg].parse(data, raw=raw, quiet=quiet)
                    found = True
                    break
                except:
                    parser_name = parser_map[arg].__name__.split('.')[-1]
                    jc.utils.error_message(f'{parser_name} parser could not parse the input data. Did you use the correct parser?\n         For details use the -d option.')
                    exit(1)

    if not found:
        helptext('missing or incorrect arguments')
        exit()

    json_out(result, pretty=pretty)


if __name__ == '__main__':
    main()
