"""jc - JSON CLI output utility route Parser

Usage:
    specify --route as the first argument if the piped input is coming from route


Example:

$ route | jc --route -p
[
  {
    "destination": "default",
    "gateway": "gateway",
    "genmask": "0.0.0.0",
    "flags": "UG",
    "metric": "100",
    "ref": "0",
    "use": "0",
    "iface": "ens33"
  },
  {
    "destination": "172.17.0.0",
    "gateway": "0.0.0.0",
    "genmask": "255.255.0.0",
    "flags": "U",
    "metric": "0",
    "ref": "0",
    "use": "0",
    "iface": "docker0"
  },
  {
    "destination": "192.168.71.0",
    "gateway": "0.0.0.0",
    "genmask": "255.255.255.0",
    "flags": "U",
    "metric": "100",
    "ref": "0",
    "use": "0",
    "iface": "ens33"
  }
]
"""


def parse(data):

    # code adapted from Conor Heine at:
    # https://gist.github.com/cahna/43a1a3ff4d075bcd71f9d7120037a501

    cleandata = data.splitlines()[1:]
    headers = [h for h in ' '.join(cleandata[0].lower().strip().split()).split() if h]
    raw_data = map(lambda s: s.strip().split(None, len(headers) - 1), cleandata[1:])
    return [dict(zip(headers, r)) for r in raw_data]
