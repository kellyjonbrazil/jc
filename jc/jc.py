#!/usr/bin/env python3
"""jc - JSON CLI output utility

Main input module
"""

import sys
import json
import jc.parsers.ifconfig
import jc.parsers.ls
import jc.parsers.netstat
import jc.parsers.ps
import jc.parsers.route


def main():
    data = sys.stdin.read()
    pretty = False

    if '-p' in sys.argv:
        pretty = True

    if '--ifconfig' in sys.argv:
        result = jc.parsers.ifconfig.parse(data)

    elif '--ls' in sys.argv:
        result = jc.parsers.ls.parse(data)

    elif '--netstat' in sys.argv:
        result = jc.parsers.netstat.parse(data)

    elif '--ps' in sys.argv:
        result = jc.parsers.ps.parse(data)

    elif '--route' in sys.argv:
        result = jc.parsers.route.parse(data)

    else:
        print('jc:     missing arguments', file=sys.stderr)
        print('Usage:  jc [parser] [options]\n', file=sys.stderr)
        print('Parsers:', file=sys.stderr)
        print('        --ifconfig   iconfig parser', file=sys.stderr)
        print('        --ls         ls parser', file=sys.stderr)
        print('        --netstat    netstat parser', file=sys.stderr)
        print('        --ps         ps parser', file=sys.stderr)
        print('        --route      route parser\n', file=sys.stderr)
        print('Options:', file=sys.stderr)
        print('        -p           pretty print output\n', file=sys.stderr)
        print('Example:', file=sys.stderr)
        print('        ls -al | jc --ls -p\n', file=sys.stderr)
        exit()

    # output resulting dictionary as json
    if pretty:
        print(json.dumps(result, indent=2))
    else:
        print(json.dumps(result))


if __name__ == '__main__':
    main()
