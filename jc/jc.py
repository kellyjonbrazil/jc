#!/usr/bin/env python3
"""jc - JSON CLI output utility

Main input module
"""

import sys
import json
import jc.parsers.df
import jc.parsers.env
import jc.parsers.free
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


def helptext():
    print('Usage:  jc [parser] [options]\n', file=sys.stderr)
    print('Parsers:', file=sys.stderr)
    print('        --df         df parser', file=sys.stderr)
    print('        --env        env parser', file=sys.stderr)
    print('        --free       free parser', file=sys.stderr)
    print('        --ifconfig   iconfig parser', file=sys.stderr)
    print('        --iptables   iptables parser', file=sys.stderr)
    print('        --jobs       jobs parser', file=sys.stderr)
    print('        --ls         ls parser', file=sys.stderr)
    print('        --lsblk      lsblk parser', file=sys.stderr)
    print('        --lsmod      lsmod parser', file=sys.stderr)
    print('        --lsof       lsof parser', file=sys.stderr)
    print('        --mount      mount parser', file=sys.stderr)
    print('        --netstat    netstat parser', file=sys.stderr)
    print('        --ps         ps parser', file=sys.stderr)
    print('        --route      route parser', file=sys.stderr)
    print('        --uname      uname parser\n', file=sys.stderr)
    print('Options:', file=sys.stderr)
    print('        -p           pretty print output\n', file=sys.stderr)
    print('Example:', file=sys.stderr)
    print('        ls -al | jc --ls -p\n', file=sys.stderr)


def main():
    if sys.stdin.isatty():
        print('jc:     missing piped data\n', file=sys.stderr)
        helptext()
        exit()

    data = sys.stdin.read()
    pretty = False

    # options
    if '-p' in sys.argv:
        pretty = True

    # parsers
    if '--df' in sys.argv:
        result = jc.parsers.df.parse(data)

    elif '--env' in sys.argv:
        result = jc.parsers.env.parse(data)

    elif '--free' in sys.argv:
        result = jc.parsers.free.parse(data)

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

    else:
        print('jc:     missing or incorrect arguments\n', file=sys.stderr)
        helptext()
        exit()

    # output resulting dictionary as json
    if pretty:
        print(json.dumps(result, indent=2))
    else:
        print(json.dumps(result))


if __name__ == '__main__':
    main()
