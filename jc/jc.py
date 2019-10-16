#!/usr/bin/env python3
"""jc - JSON CLI output utility

Main input module
"""

import sys
import json
import parsers.ifconfig
import parsers.ls
import parsers.netstat

pretty = False
data = sys.stdin.read()

if len(sys.argv) < 2:
    print(f'\nError: {sys.argv[0]}\n  Must specify parser. (e.g. --ls, --netstat, --ifconfig, etc.)')
    print('  Use -p to pretty print')
    print(f'\nExample: ls -al | {sys.argv[0]} --ls -p\n')
    exit()

arg = sys.argv[1]

if len(sys.argv) > 2:
    if sys.argv[2] == '-p':
        pretty = True

if arg == '--ifconfig':
    result = parsers.ifconfig.parse(data)
elif arg == '--ls':
    result = parsers.ls.parse(data)
elif arg == '--netstat':
    result = parsers.netstat.parse(data)

# output resulting dictionary as json
if pretty:
    print(json.dumps(result, indent=2))
else:
    print(json.dumps(result))
