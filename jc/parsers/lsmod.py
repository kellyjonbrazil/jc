"""jc - JSON CLI output utility lsmod Parser

Usage:
    specify --lsmod as the first argument if the piped input is coming from lsmod

Example:

$ lsmod | jc --lsmod -p
[
 {
    "Module": "nf_nat_ipv4",
    "Size": "14115",
    "Used": "1",
    "By": [
      "iptable_nat"
    ]
  },
  {
    "Module": "nf_nat",
    "Size": "26583",
    "Used": "3",
    "By": [
      "nf_nat_ipv4",
      "nf_nat_ipv6",
      "nf_nat_masquerade_ipv4"
    ]
  },
  {
    "Module": "iptable_mangle",
    "Size": "12695",
    "Used": "1"
  },
  {
    "Module": "iptable_security",
    "Size": "12705",
    "Used": "1"
  },
  {
    "Module": "iptable_raw",
    "Size": "12678",
    "Used": "1"
  },
  {
    "Module": "nf_conntrack",
    "Size": "139224",
    "Used": "7",
    "By": [
      "nf_nat",
      "nf_nat_ipv4",
      "nf_nat_ipv6",
      "xt_conntrack",
      "nf_nat_masquerade_ipv4",
      "nf_conntrack_ipv4",
      "nf_conntrack_ipv6"
    ]
  },
  ...
]
"""


def parse(data):

    # code adapted from Conor Heine at:
    # https://gist.github.com/cahna/43a1a3ff4d075bcd71f9d7120037a501

    cleandata = data.splitlines()
    headers = [h for h in ' '.join(cleandata[0].strip().split()).split() if h]

    headers.pop(-1)
    headers.append('By')

    raw_data = map(lambda s: s.strip().split(None, len(headers) - 1), cleandata[1:])
    output = [dict(zip(headers, r)) for r in raw_data]

    for mod in output:
        if 'By' in mod:
            mod['By'] = mod['By'].split(',')

    return output
