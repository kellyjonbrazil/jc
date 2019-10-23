"""jc - JSON CLI output utility env Parser

Usage:
    specify --env as the first argument if the piped input is coming from env

Example:
$ env | jc --env -p
[
  {
    "TERM": "xterm-256color"
  },
  {
    "SHELL": "/bin/bash"
  },
  {
    "USER": "root"
  },
  {
    "PATH": "/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
  },
  {
    "PWD": "/bin"
  },
  {
    "LANG": "en_US.UTF-8"
  },
  {
    "HOME": "/root"
  },
  {
    "_": "/usr/bin/env"
  }
]
"""


def parse(data):
    output = []

    linedata = data.splitlines()

    # Clear any blank lines
    cleandata = list(filter(None, linedata))

    if cleandata:

        for entry in cleandata:
            output_line = {}
            parsed_line = entry.split('=', maxsplit=1)
            output_line[parsed_line[0]] = parsed_line[1]
            output.append(output_line)

    return output
