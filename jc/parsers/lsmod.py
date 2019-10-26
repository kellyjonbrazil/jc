"""jc - JSON CLI output utility lsmod Parser

Usage:
    specify --lsmod as the first argument if the piped input is coming from lsmod

Example:

$ lsmod | jc --lsmod -p
[
  ...
  {
    "module": "nf_conntrack",
    "size": "139224",
    "used": "7",
    "by": [
      "nf_nat",
      "nf_nat_ipv4",
      "nf_nat_ipv6",
      "xt_conntrack",
      "nf_nat_masquerade_ipv4",
      "nf_conntrack_ipv4",
      "nf_conntrack_ipv6"
    ]
  },
  {
    "module": "ip_set",
    "size": "45799",
    "used": "0"
  },
  {
    "module": "nfnetlink",
    "size": "14519",
    "used": "1",
    "by": [
      "ip_set"
    ]
  },
  {
    "module": "ebtable_filter",
    "size": "12827",
    "used": "1"
  },
  {
    "module": "ebtables",
    "size": "35009",
    "used": "2",
    "by": [
      "ebtable_nat",
      "ebtable_filter"
    ]
  },
  ...
]
"""


def parse(data):

    # code adapted from Conor Heine at:
    # https://gist.github.com/cahna/43a1a3ff4d075bcd71f9d7120037a501

    cleandata = data.splitlines()
    headers = [h for h in ' '.join(cleandata[0].lower().strip().split()).split() if h]

    raw_data = map(lambda s: s.strip().split(None, len(headers) - 1), cleandata[1:])
    output = [dict(zip(headers, r)) for r in raw_data]

    for mod in output:
        if 'by' in mod:
            mod['by'] = mod['by'].split(',')

    return output
