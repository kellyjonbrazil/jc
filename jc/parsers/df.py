"""jc - JSON CLI output utility df Parser

Usage:
    specify --df as the first argument if the piped input is coming from df

Example:

$ df | jc --df -p
[
  {
    "Filesystem": "/dev/disk1s1",
    "512-blocks": "976490576",
    "Used": "268326664",
    "Available": "702568152",
    "Capacity": "28%",
    "iused": "1395740",
    "ifree": "9223372036853380067",
    "%iused": "0%",
    "Mounted": "/"
  },
  {
    "Filesystem": "devfs",
    "512-blocks": "680",
    "Used": "680",
    "Available": "0",
    "Capacity": "100%",
    "iused": "1178",
    "ifree": "0",
    "%iused": "100%",
    "Mounted": "/dev"
  },
  {
    "Filesystem": "map",
    "512-blocks": "auto_home",
    "Used": "0",
    "Available": "0",
    "Capacity": "0",
    "iused": "100%",
    "ifree": "0",
    "%iused": "0",
    "Mounted": "100%",
    "on": "/home"
  }
]
"""


def parse(data):

    # code adapted from Conor Heine at:
    # https://gist.github.com/cahna/43a1a3ff4d075bcd71f9d7120037a501

    cleandata = data.splitlines()
    headers = [h for h in ' '.join(cleandata[0].strip().split()).split() if h]
    raw_data = map(lambda s: s.strip().split(None, len(headers) - 1), cleandata[1:])
    return [dict(zip(headers, r)) for r in raw_data]
