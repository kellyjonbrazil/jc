#!/usr/bin/env python3
"""jc - JSON CLI output utility

Main input module
"""

import sys
import signal
import json
from jc.utils import *
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


def main():
    signal.signal(signal.SIGINT, ctrlc)

    if sys.stdin.isatty():
        helptext('missing piped data')
        exit()

    data = sys.stdin.read()
    pretty = False
    quiet = False
    raw = False

    # options
    if '-p' in sys.argv:
        pretty = True

    if '-q' in sys.argv:
        quiet = True

    if '-r' in sys.argv:
        raw = True

    # parsers
    if '--arp' in sys.argv:
        result = jc.parsers.arp.parse(data, raw=raw, quiet=quiet)

    elif '--df' in sys.argv:
        result = jc.parsers.df.parse(data, raw=raw, quiet=quiet)

    elif '--dig' in sys.argv:
        result = jc.parsers.dig.parse(data, raw=raw, quiet=quiet)

    elif '--env' in sys.argv:
        result = jc.parsers.env.parse(data, raw=raw, quiet=quiet)

    elif '--free' in sys.argv:
        result = jc.parsers.free.parse(data, raw=raw, quiet=quiet)

    elif '--history' in sys.argv:
        result = jc.parsers.history.parse(data, raw=raw, quiet=quiet)

    elif '--ifconfig' in sys.argv:
        result = jc.parsers.ifconfig.parse(data, raw=raw, quiet=quiet)

    elif '--iptables' in sys.argv:
        result = jc.parsers.iptables.parse(data, raw=raw, quiet=quiet)

    elif '--jobs' in sys.argv:
        result = jc.parsers.jobs.parse(data, raw=raw, quiet=quiet)

    elif '--ls' in sys.argv:
        result = jc.parsers.ls.parse(data, raw=raw, quiet=quiet)

    elif '--lsblk' in sys.argv:
        result = jc.parsers.lsblk.parse(data, raw=raw, quiet=quiet)

    elif '--lsmod' in sys.argv:
        result = jc.parsers.lsmod.parse(data, raw=raw, quiet=quiet)

    elif '--lsof' in sys.argv:
        result = jc.parsers.lsof.parse(data, raw=raw, quiet=quiet)

    elif '--mount' in sys.argv:
        result = jc.parsers.mount.parse(data, raw=raw, quiet=quiet)

    elif '--netstat' in sys.argv:
        result = jc.parsers.netstat.parse(data, raw=raw, quiet=quiet)

    elif '--ps' in sys.argv:
        result = jc.parsers.ps.parse(data, raw=raw, quiet=quiet)

    elif '--route' in sys.argv:
        result = jc.parsers.route.parse(data, raw=raw, quiet=quiet)

    elif '--uname' in sys.argv:
        result = jc.parsers.uname.parse(data, raw=raw, quiet=quiet)

    elif '--uptime' in sys.argv:
        result = jc.parsers.uptime.parse(data, raw=raw, quiet=quiet)

    elif '--w' in sys.argv:
        result = jc.parsers.w.parse(data, raw=raw, quiet=quiet)

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
