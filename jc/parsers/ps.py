"""jc - JSON CLI output utility ps Parser

Usage:
    specify --ps as the first argument if the piped input is coming from ps

    ps options supported:
    - ef
    - axu

Example:

$ ps -ef | jc --ps -p
[
  {
    "UID": "root",
    "PID": "1",
    "PPID": "0",
    "C": "0",
    "STIME": "13:58",
    "TTY": "?",
    "TIME": "00:00:05",
    "CMD": "/lib/systemd/systemd --system --deserialize 35"
  },
  {
    "UID": "root",
    "PID": "2",
    "PPID": "0",
    "C": "0",
    "STIME": "13:58",
    "TTY": "?",
    "TIME": "00:00:00",
    "CMD": "[kthreadd]"
  },
  {
    "UID": "root",
    "PID": "4",
    "PPID": "2",
    "C": "0",
    "STIME": "13:58",
    "TTY": "?",
    "TIME": "00:00:00",
    "CMD": "[kworker/0:0H]"
  },
  {
    "UID": "root",
    "PID": "6",
    "PPID": "2",
    "C": "0",
    "STIME": "13:58",
    "TTY": "?",
    "TIME": "00:00:00",
    "CMD": "[mm_percpu_wq]"
  },
  ...
]
"""


def parse(data):

    # code adapted from Conor Heine at:
    # https://gist.github.com/cahna/43a1a3ff4d075bcd71f9d7120037a501

    cleandata = data.splitlines()
    headers = [h for h in ' '.join(cleandata[0].strip().split()).split() if h]
    raw_data = map(lambda s: s.strip().split(None, len(headers) - 1), cleandata[1:])
    return [dict(zip(headers, r)) for r in raw_data]
