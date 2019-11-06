"""jc - JSON CLI output utility env Parser

Usage:
    specify --env as the first argument if the piped input is coming from env

Examples:

$ env | jc --env -p
[
  {
    "name": "XDG_SESSION_ID",
    "value": "1"
  },
  {
    "name": "HOSTNAME",
    "value": "localhost.localdomain"
  },
  {
    "name": "TERM",
    "value": "vt220"
  },
  {
    "name": "SHELL",
    "value": "/bin/bash"
  },
  {
    "name": "HISTSIZE",
    "value": "1000"
  },
  ...
]

$ env | jc --env -p -r
{
  "TERM": "xterm-256color",
  "SHELL": "/bin/bash",
  "USER": "root",
  "PATH": "/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin",
  "PWD": "/root",
  "LANG": "en_US.UTF-8",
  "HOME": "/root",
  "LOGNAME": "root",
  "_": "/usr/bin/env"
}
"""
import jc


def process(proc_data):
    '''schema:
    [
      {
        "name":     string,
        "value":    string
      }
    ]
    '''

    # rebuild output for added semantic information
    processed = []
    for k, v in proc_data.items():
        proc_line = {}
        proc_line['name'] = k
        proc_line['value'] = v
        processed.append(proc_line)

    return processed


def parse(data, raw=False):
    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    jc.jc.compatibility(__name__,
                        ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd'])

    raw_output = {}

    linedata = data.splitlines()

    # Clear any blank lines
    cleandata = list(filter(None, linedata))

    if cleandata:

        for entry in cleandata:
            parsed_line = entry.split('=', maxsplit=1)
            raw_output[parsed_line[0]] = parsed_line[1]

    if raw:
        return raw_output
    else:
        return process(raw_output)
