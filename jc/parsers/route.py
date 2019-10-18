"""jc - JSON CLI output utility route Parser

Usage:
    specify --route as the first argument if the piped input is coming from route


Example:

$ route -n | jc --route -p
[
  {
    "Destination": "0.0.0.0",
    "Gateway": "192.168.71.2",
    "Genmask": "0.0.0.0",
    "Flags": "UG",
    "Metric": "100",
    "Ref": "0",
    "Use": "0",
    "Iface": "ens33"
  },
  {
    "Destination": "172.17.0.0",
    "Gateway": "0.0.0.0",
    "Genmask": "255.255.0.0",
    "Flags": "U",
    "Metric": "0",
    "Ref": "0",
    "Use": "0",
    "Iface": "docker0"
  },
  {
    "Destination": "192.168.71.0",
    "Gateway": "0.0.0.0",
    "Genmask": "255.255.255.0",
    "Flags": "U",
    "Metric": "0",
    "Ref": "0",
    "Use": "0",
    "Iface": "ens33"
  },
  {
    "Destination": "192.168.71.2",
    "Gateway": "0.0.0.0",
    "Genmask": "255.255.255.255",
    "Flags": "UH",
    "Metric": "100",
    "Ref": "0",
    "Use": "0",
    "Iface": "ens33"
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
