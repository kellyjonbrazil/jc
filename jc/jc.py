#!/usr/bin/env python3
"""jc - JSON CLI output utility

Main input module
"""

import sys
import signal
import json
import textwrap
import jc.parsers.arp
import jc.parsers.df
import jc.parsers.dig
import jc.parsers.env
import jc.parsers.free
import jc.parsers.history
import jc.parsers.ifconfig
import jc.parsers.iptables
import jc.parsers.jobs
import jc.parsers.ls
import jc.parsers.lsblk
import jc.parsers.lsmod
import jc.parsers.lsof
import jc.parsers.mount
import jc.parsers.netstat
import jc.parsers.ps
import jc.parsers.route
import jc.parsers.uname
import jc.parsers.uptime
import jc.parsers.w


def ctrlc(signum, frame):
    exit()


def helptext(message):
    helptext_string = f'''
    jc:     {message}

    Usage:  jc PARSER [OPTIONS]

    Parsers:
            --arp        arp parser
            --df         df parser
            --dig        dig parser
            --env        env parser
            --free       free parser
            --history    history parser
            --ifconfig   iconfig parser
            --iptables   iptables parser
            --jobs       jobs parser
            --ls         ls parser
            --lsblk      lsblk parser
            --lsmod      lsmod parser
            --lsof       lsof parser
            --mount      mount parser
            --netstat    netstat parser
            --ps         ps parser
            --route      route parser
            --uname      uname parser
            --uptime     uptime parser
            --w          w parser

    Options:
            -p           pretty print output
            -r           raw JSON output

    Example:
            ls -al | jc --ls -p
    '''

    print(textwrap.dedent(helptext_string), file=sys.stderr)


def errormessage(message):
    error_string = f'''
    jc:  {message}
    '''

    print(textwrap.dedent(error_string), file=sys.stderr)
    exit()


def compatibility(mod_name, compatible):
    if sys.platform not in compatible:
        mod = mod_name.split('.')[-1]
        compat_list = ', '.join(compatible)
        errormessage(f'{mod} parser not compatible with your OS ({sys.platform}).\n         Compatible platforms: {compat_list}')


def main():
    signal.signal(signal.SIGINT, ctrlc)

    if sys.stdin.isatty():
        helptext('missing piped data')
        exit()

    data = sys.stdin.read()
    pretty = False
    raw = False

    # options
    if '-p' in sys.argv:
        pretty = True

    if '-r' in sys.argv:
        raw = True

    # parsers
    if '--arp' in sys.argv:
        result = jc.parsers.arp.parse(data, raw=raw)

    elif '--df' in sys.argv:
        result = jc.parsers.df.parse(data, raw=raw)

    elif '--dig' in sys.argv:
        result = jc.parsers.dig.parse(data, raw=raw)

    elif '--env' in sys.argv:
        result = jc.parsers.env.parse(data, raw=raw)

    elif '--free' in sys.argv:
        result = jc.parsers.free.parse(data, raw=raw)

    elif '--history' in sys.argv:
        result = jc.parsers.history.parse(data, raw=raw)

    elif '--ifconfig' in sys.argv:
        result = jc.parsers.ifconfig.parse(data, raw=raw)

    elif '--iptables' in sys.argv:
        result = jc.parsers.iptables.parse(data, raw=raw)

    elif '--jobs' in sys.argv:
        result = jc.parsers.jobs.parse(data, raw=raw)

    elif '--ls' in sys.argv:
        result = jc.parsers.ls.parse(data, raw=raw)

    elif '--lsblk' in sys.argv:
        result = jc.parsers.lsblk.parse(data, raw=raw)

    elif '--lsmod' in sys.argv:
        result = jc.parsers.lsmod.parse(data, raw=raw)

    elif '--lsof' in sys.argv:
        result = jc.parsers.lsof.parse(data, raw=raw)

    elif '--mount' in sys.argv:
        result = jc.parsers.mount.parse(data, raw=raw)

    elif '--netstat' in sys.argv:
        result = jc.parsers.netstat.parse(data, raw=raw)

    elif '--ps' in sys.argv:
        result = jc.parsers.ps.parse(data, raw=raw)

    elif '--route' in sys.argv:
        result = jc.parsers.route.parse(data, raw=raw)

    elif '--uname' in sys.argv:
        result = jc.parsers.uname.parse(data, raw=raw)

    elif '--uptime' in sys.argv:
        result = jc.parsers.uptime.parse(data, raw=raw)

    elif '--w' in sys.argv:
        result = jc.parsers.w.parse(data, raw=raw)

    else:
        helptext('missing or incorrect arguments')
        exit()

    # output resulting dictionary as json
    if pretty:
        print(json.dumps(result, indent=2))
    else:
        print(json.dumps(result))


if __name__ == '__main__':
    main()
