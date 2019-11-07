"""jc - JSON CLI output utility ps Parser

Usage:
    specify --ps as the first argument if the piped input is coming from ps

    ps options supported:
    - ef
    - axu

Examples:

$ ps -ef | jc --ps -p
[
  {
    "uid": "root",
    "pid": 1,
    "ppid": 0,
    "c": 0,
    "stime": "Nov01",
    "tty": null,
    "time": "00:00:11",
    "cmd": "/usr/lib/systemd/systemd --switched-root --system --deserialize 22"
  },
  {
    "uid": "root",
    "pid": 2,
    "ppid": 0,
    "c": 0,
    "stime": "Nov01",
    "tty": null,
    "time": "00:00:00",
    "cmd": "[kthreadd]"
  },
  {
    "uid": "root",
    "pid": 4,
    "ppid": 2,
    "c": 0,
    "stime": "Nov01",
    "tty": null,
    "time": "00:00:00",
    "cmd": "[kworker/0:0H]"
  },
  ...
]

$ ps -ef | jc --ps -p -r
[
  {
    "uid": "root",
    "pid": "1",
    "ppid": "0",
    "c": "0",
    "stime": "Nov01",
    "tty": "?",
    "time": "00:00:11",
    "cmd": "/usr/lib/systemd/systemd --switched-root --system --deserialize 22"
  },
  {
    "uid": "root",
    "pid": "2",
    "ppid": "0",
    "c": "0",
    "stime": "Nov01",
    "tty": "?",
    "time": "00:00:00",
    "cmd": "[kthreadd]"
  },
  {
    "uid": "root",
    "pid": "4",
    "ppid": "2",
    "c": "0",
    "stime": "Nov01",
    "tty": "?",
    "time": "00:00:00",
    "cmd": "[kworker/0:0H]"
  },
  ...
]
"""
import jc.utils


def process(proc_data):
    '''schema:
    [
      {
        "uid":    string,
        "pid":    integer,
        "ppid":   integer,
        "c":      integer,
        "stime":  string,
        "tty":    string,    # ? = Null
        "time":   string,
        "cmd":    string
      }
    ]
    '''
    for entry in proc_data:
        int_list = ['pid', 'ppid', 'c']
        for key in int_list:
            if key in entry:
                try:
                    key_int = int(entry[key])
                    entry[key] = key_int
                except (ValueError):
                    entry[key] = None

        if 'tty' in entry:
            if entry['tty'] == '?':
                entry['tty'] = None

    return proc_data


def parse(data, raw=False, quiet=False):
    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'cygwin', 'aix', 'freebsd']

    if not quiet:
        jc.utils.compatibility(__name__, compatible)

    # code adapted from Conor Heine at:
    # https://gist.github.com/cahna/43a1a3ff4d075bcd71f9d7120037a501

    cleandata = data.splitlines()
    headers = [h for h in ' '.join(cleandata[0].lower().strip().split()).split() if h]

    # clean up '%cpu' and '%mem' headers
    # even though % in a key is valid json, it can make things difficult
    headers = ['cpu_percent' if x == '%cpu' else x for x in headers]
    headers = ['mem_percent' if x == '%mem' else x for x in headers]

    raw_data = map(lambda s: s.strip().split(None, len(headers) - 1), cleandata[1:])
    raw_output = [dict(zip(headers, r)) for r in raw_data]

    if raw:
        return raw_output
    else:
        return process(raw_output)
