"""jc - JSON CLI output utility free Parser

Usage:
    specify --free as the first argument if the piped input is coming from free

Example:

$ free | jc --free -p
[
  {
    "type": "Mem",
    "total": "2017300",
    "used": "213104",
    "free": "1148452",
    "shared": "1176",
    "buff_cache": "655744",
    "available": "1622204"
  },
  {
    "type": "Swap",
    "total": "2097148",
    "used": "0",
    "free": "2097148"
  }
]
"""


def parse(data):

    # code adapted from Conor Heine at:
    # https://gist.github.com/cahna/43a1a3ff4d075bcd71f9d7120037a501

    cleandata = data.splitlines()
    headers = [h for h in ' '.join(cleandata[0].lower().strip().split()).split() if h]
    headers.insert(0, "type")

    # clean up 'buff/cache' header
    # even though forward slash in a key is valid json, it can make things difficult
    headers = ['buff_cache' if x == 'buff/cache' else x for x in headers]

    raw_data = map(lambda s: s.strip().split(None, len(headers) - 1), cleandata[1:])
    output = [dict(zip(headers, r)) for r in raw_data]

    for entry in output:
        entry['type'] = entry['type'].rstrip(':')

    return output
