#!/usr/bin/env python3
"""jc - JSON CLI output utility

Main input module
"""

import sys
import json
import jc.parsers.ifconfig
import jc.parsers.ls
import jc.parsers.netstat

def main():
    pretty = False
    data = sys.stdin.read()

    if len(sys.argv) < 2:
        print(f'\nError: jc\n  Must specify parser. (e.g. --ls, --netstat, --ifconfig, etc.)')
        print('  Use -p to pretty print')
        print(f'\nExample: ls -al | jc --ls -p\n')
        exit()

    arg = sys.argv[1]

    if len(sys.argv) > 2:
        if sys.argv[2] == '-p':
            pretty = True

    if arg == '--ifconfig':
        result = jc.parsers.ifconfig.parse(data)
    elif arg == '--ls':
        result = jc.parsers.ls.parse(data)
    elif arg == '--netstat':
        result = jc.parsers.netstat.parse(data)

    # output resulting dictionary as json
    if pretty:
        print(json.dumps(result, indent=2))
    else:
        print(json.dumps(result))

if __name__ == '__main__':
    main()
