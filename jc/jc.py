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


def main():
    helptext = '''

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

    Example:
            ls -al | jc --ls -p

    '''

    signal.signal(signal.SIGINT, ctrlc)

    if sys.stdin.isatty():
        print('jc:     missing piped data' + textwrap.dedent(helptext), file=sys.stderr)
        exit()

    data = sys.stdin.read()
    pretty = False

    # options
    if '-p' in sys.argv:
        pretty = True

    # parsers
    if '--arp' in sys.argv:
        result = jc.parsers.arp.parse(data)

    elif '--df' in sys.argv:
        result = jc.parsers.df.parse(data)

    elif '--dig' in sys.argv:
        result = jc.parsers.dig.parse(data)

    elif '--env' in sys.argv:
        result = jc.parsers.env.parse(data)

    elif '--free' in sys.argv:
        result = jc.parsers.free.parse(data)

    elif '--history' in sys.argv:
        result = jc.parsers.history.parse(data)

    elif '--ifconfig' in sys.argv:
        result = jc.parsers.ifconfig.parse(data)

    elif '--iptables' in sys.argv:
        result = jc.parsers.iptables.parse(data)

    elif '--jobs' in sys.argv:
        result = jc.parsers.jobs.parse(data)

    elif '--ls' in sys.argv:
        result = jc.parsers.ls.parse(data)

    elif '--lsblk' in sys.argv:
        result = jc.parsers.lsblk.parse(data)

    elif '--lsmod' in sys.argv:
        result = jc.parsers.lsmod.parse(data)

    elif '--lsof' in sys.argv:
        result = jc.parsers.lsof.parse(data)

    elif '--mount' in sys.argv:
        result = jc.parsers.mount.parse(data)

    elif '--netstat' in sys.argv:
        result = jc.parsers.netstat.parse(data)

    elif '--ps' in sys.argv:
        result = jc.parsers.ps.parse(data)

    elif '--route' in sys.argv:
        result = jc.parsers.route.parse(data)

    elif '--uname' in sys.argv:
        result = jc.parsers.uname.parse(data)

    elif '--uptime' in sys.argv:
        result = jc.parsers.uptime.parse(data)

    elif '--w' in sys.argv:
        result = jc.parsers.w.parse(data)

    else:
        print('jc:     missing or incorrect arguments' + textwrap.dedent(helptext), file=sys.stderr)
        exit()

    # output resulting dictionary as json
    if pretty:
        print(json.dumps(result, indent=2))
    else:
        print(json.dumps(result))


if __name__ == '__main__':
    main()
