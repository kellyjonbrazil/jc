"""jc - JSON CLI output utility lsblk Parser

Usage:
    specify --lsblk as the first argument if the piped input is coming from lsblk

Example:

$ lsblk | jc --lsblk -p
[
  {
    "name": "sda",
    "maj_min": "8:0",
    "rm": "0",
    "size": "20G",
    "ro": "0",
    "type": "disk"
  },
  {
    "name": "sda1",
    "maj_min": "8:1",
    "rm": "0",
    "size": "1G",
    "ro": "0",
    "type": "part",
    "mountpoint": "/boot"
  },
  {
    "name": "sda2",
    "maj_min": "8:2",
    "rm": "0",
    "size": "19G",
    "ro": "0",
    "type": "part"
  },
  {
    "name": "centos-root",
    "maj_min": "253:0",
    "rm": "0",
    "size": "17G",
    "ro": "0",
    "type": "lvm",
    "mountpoint": "/"
  },
  {
    "name": "centos-swap",
    "maj_min": "253:1",
    "rm": "0",
    "size": "2G",
    "ro": "0",
    "type": "lvm",
    "mountpoint": "[SWAP]"
  },
  {
    "name": "sr0",
    "maj_min": "11:0",
    "rm": "1",
    "size": "1024M",
    "ro": "0",
    "type": "rom"
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
