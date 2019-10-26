"""jc - JSON CLI output utility ps Parser

Usage:
    specify --ps as the first argument if the piped input is coming from ps

    ps options supported:
    - ef
    - axu

Example:

$ ps -ef | jc --ps -p
[
  ...
  {
    "uid": "root",
    "pid": "545",
    "ppid": "1",
    "c": "0",
    "stime": "Oct21",
    "tty": "?",
    "time": "00:00:03",
    "cmd": "/usr/lib/systemd/systemd-journald"
  },
  {
    "uid": "root",
    "pid": "566",
    "ppid": "1",
    "c": "0",
    "stime": "Oct21",
    "tty": "?",
    "time": "00:00:00",
    "cmd": "/usr/sbin/lvmetad -f"
  },
  {
    "uid": "root",
    "pid": "580",
    "ppid": "1",
    "c": "0",
    "stime": "Oct21",
    "tty": "?",
    "time": "00:00:00",
    "cmd": "/usr/lib/systemd/systemd-udevd"
  },
  {
    "uid": "root",
    "pid": "659",
    "ppid": "2",
    "c": "0",
    "stime": "Oct21",
    "tty": "?",
    "time": "00:00:00",
    "cmd": "[kworker/u257:0]"
  },
  {
    "uid": "root",
    "pid": "666",
    "ppid": "2",
    "c": "0",
    "stime": "Oct21",
    "tty": "?",
    "time": "00:00:00",
    "cmd": "[hci0]"
  },
  ...
]
"""


def parse(data):

    # code adapted from Conor Heine at:
    # https://gist.github.com/cahna/43a1a3ff4d075bcd71f9d7120037a501

    cleandata = data.splitlines()
    headers = [h for h in ' '.join(cleandata[0].lower().strip().split()).split() if h]

    # clean up '%cpu' and '%mem' headers
    # even though % in a key is valid json, it can make things difficult
    headers = ['cpu_percent' if x == '%cpu' else x for x in headers]
    headers = ['mem_percent' if x == '%mem' else x for x in headers]

    raw_data = map(lambda s: s.strip().split(None, len(headers) - 1), cleandata[1:])
    return [dict(zip(headers, r)) for r in raw_data]
