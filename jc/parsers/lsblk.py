"""jc - JSON CLI output utility lsblk Parser

Usage:
    specify --lsblk as the first argument if the piped input is coming from lsblk

Example:

$ lsblk | jc --lsblk -p
[
  {
    "NAME": "loop0",
    "MAJ_MIN": "7:0",
    "RM": "0",
    "SIZE": "54.5M",
    "RO": "1",
    "TYPE": "loop",
    "MOUNTPOINT": "/snap/core18/1223"
  },
  {
    "NAME": "sda",
    "MAJ_MIN": "8:0",
    "RM": "0",
    "SIZE": "20G",
    "RO": "0",
    "TYPE": "disk"
  },
  {
    "NAME": "sda1",
    "MAJ_MIN": "8:1",
    "RM": "0",
    "SIZE": "1M",
    "RO": "0",
    "TYPE": "part"
  },
  {
    "NAME": "sda2",
    "MAJ_MIN": "8:2",
    "RM": "0",
    "SIZE": "20G",
    "RO": "0",
    "TYPE": "part",
    "MOUNTPOINT": "/"
  },
  {
    "NAME": "sr0",
    "MAJ_MIN": "11:0",
    "RM": "1",
    "SIZE": "64.8M",
    "RO": "0",
    "TYPE": "rom"
  }
]
"""


def parse(data):

    # code adapted from Conor Heine at:
    # https://gist.github.com/cahna/43a1a3ff4d075bcd71f9d7120037a501

    cleandata = data.splitlines()
    headers = [h for h in ' '.join(cleandata[0].lower().strip().split()).split() if h]

    # clean up 'maj:min' header
    # even though colon in a key is valid json, it can make things difficult
    headers = ['maj_min' if x == 'maj:min' else x for x in headers]

    raw_data = map(lambda s: s.strip().split(None, len(headers) - 1), cleandata[1:])
    output = [dict(zip(headers, r)) for r in raw_data]

    for entry in output:
        entry['name'] = entry['name'].encode('ascii', errors='ignore').decode()

    return output
