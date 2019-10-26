"""jc - JSON CLI output utility w Parser

Usage:
    specify --w as the first argument if the piped input is coming from w

Example:

$ w | jc --w -p
[
  {
    "user": "root",
    "tty": "ttyS0",
    "from": "-",
    "login_at": "Mon20",
    "idle": "0.00s",
    "jcpu": "14.70s",
    "pcpu": "0.00s",
    "what": "bash"
  },
  {
    "user": "root",
    "tty": "pts/0",
    "from": "192.168.71.1",
    "login_at": "Thu22",
    "idle": "22:46m",
    "jcpu": "0.05s",
    "pcpu": "0.05s",
    "what": "-bash"
  }
]
"""


def parse(data):

    # code adapted from Conor Heine at:
    # https://gist.github.com/cahna/43a1a3ff4d075bcd71f9d7120037a501

    cleandata = data.splitlines()[1:]
    headers = [h for h in ' '.join(cleandata[0].lower().strip().split()).split() if h]

    # clean up 'login@' header
    # even though @ in a key is valid json, it can make things difficult
    headers = ['login_at' if x == 'login@' else x for x in headers]

    raw_data = map(lambda s: s.strip().split(None, len(headers) - 1), cleandata[1:])
    return [dict(zip(headers, r)) for r in raw_data]
