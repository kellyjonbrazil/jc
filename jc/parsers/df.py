"""jc - JSON CLI output utility df Parser

Usage:
    specify --df as the first argument if the piped input is coming from df

Example:

$ df | jc --df -p
[
  {
    "filesystem": "udev",
    "1k-blocks": "977500",
    "used": "0",
    "available": "977500",
    "use_percent": "0%",
    "mounted": "/dev"
  },
  {
    "filesystem": "tmpfs",
    "1k-blocks": "201732",
    "used": "1204",
    "available": "200528",
    "use_percent": "1%",
    "mounted": "/run"
  },
  {
    "filesystem": "/dev/sda2",
    "1k-blocks": "20508240",
    "used": "5748312",
    "available": "13695124",
    "use_percent": "30%",
    "mounted": "/"
  },
  {
    "filesystem": "tmpfs",
    "1k-blocks": "1008648",
    "used": "0",
    "available": "1008648",
    "use_percent": "0%",
    "mounted": "/dev/shm"
  }
  ...
]
"""


def parse(data):

    # code adapted from Conor Heine at:
    # https://gist.github.com/cahna/43a1a3ff4d075bcd71f9d7120037a501

    cleandata = data.splitlines()
    headers = [h for h in ' '.join(cleandata[0].lower().strip().split()).split() if h]

    # clean up 'use%' header
    # even though % in a key is valid json, it can make things difficult
    headers = ['use_percent' if x == 'use%' else x for x in headers]

    raw_data = map(lambda s: s.strip().split(None, len(headers) - 1), cleandata[1:])
    return [dict(zip(headers, r)) for r in raw_data]
