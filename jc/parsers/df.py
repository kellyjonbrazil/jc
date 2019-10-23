"""jc - JSON CLI output utility df Parser

Usage:
    specify --df as the first argument if the piped input is coming from df

Example:

$ df | jc --df -p
[
  {
    "Filesystem": "udev",
    "1K-blocks": "977500",
    "Used": "0",
    "Available": "977500",
    "Use%": "0%",
    "Mounted": "/dev"
  },
  {
    "Filesystem": "tmpfs",
    "1K-blocks": "201732",
    "Used": "1180",
    "Available": "200552",
    "Use%": "1%",
    "Mounted": "/run"
  },
  {
    "Filesystem": "/dev/sda2",
    "1K-blocks": "20508240",
    "Used": "5747284",
    "Available": "13696152",
    "Use%": "30%",
    "Mounted": "/"
  },
  {
    "Filesystem": "tmpfs",
    "1K-blocks": "1008648",
    "Used": "0",
    "Available": "1008648",
    "Use%": "0%",
    "Mounted": "/dev/shm"
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
