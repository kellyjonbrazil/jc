"""jc - JSON CLI output utility w Parser

Usage:
    specify --w as the first argument if the piped input is coming from w


Example:

$ w | jc --w -p
[
  {
    "USER": "root",
    "TTY": "ttyS0",
    "FROM": "-",
    "LOGIN@": "Mon20",
    "IDLE": "2:27",
    "JCPU": "10.61s",
    "PCPU": "10.53s",
    "WHAT": "-bash"
  },
  {
    "USER": "root",
    "TTY": "pts/0",
    "FROM": "192.168.71.1",
    "LOGIN@": "22:58",
    "IDLE": "2.00s",
    "JCPU": "0.04s",
    "PCPU": "0.00s",
    "WHAT": "w"
  }
]
"""


def parse(data):

    # code adapted from Conor Heine at:
    # https://gist.github.com/cahna/43a1a3ff4d075bcd71f9d7120037a501

    cleandata = data.splitlines()[1:]
    headers = [h for h in ' '.join(cleandata[0].strip().split()).split() if h]
    raw_data = map(lambda s: s.strip().split(None, len(headers) - 1), cleandata[1:])
    return [dict(zip(headers, r)) for r in raw_data]
