"""jc - JSON CLI output utility route Parser

Usage:
    specify --route as the first argument if the piped input is coming from route

Examples:

    $ route -ee | jc --route -p
    [
      {
        "destination": "default",
        "gateway": "gateway",
        "genmask": "0.0.0.0",
        "flags": "UG",
        "metric": 100,
        "ref": 0,
        "use": 0,
        "iface": "ens33",
        "mss": 0,
        "window": 0,
        "irtt": 0
      },
      {
        "destination": "172.17.0.0",
        "gateway": "0.0.0.0",
        "genmask": "255.255.0.0",
        "flags": "U",
        "metric": 0,
        "ref": 0,
        "use": 0,
        "iface": "docker",
        "mss": 0,
        "window": 0,
        "irtt": 0
      },
      {
        "destination": "192.168.71.0",
        "gateway": "0.0.0.0",
        "genmask": "255.255.255.0",
        "flags": "U",
        "metric": 100,
        "ref": 0,
        "use": 0,
        "iface": "ens33",
        "mss": 0,
        "window": 0,
        "irtt": 0
      }
    ]

    $ route -ee | jc --route -p -r
    [
      {
        "destination": "default",
        "gateway": "gateway",
        "genmask": "0.0.0.0",
        "flags": "UG",
        "metric": "100",
        "ref": "0",
        "use": "0",
        "iface": "ens33",
        "mss": "0",
        "window": "0",
        "irtt": "0"
      },
      {
        "destination": "172.17.0.0",
        "gateway": "0.0.0.0",
        "genmask": "255.255.0.0",
        "flags": "U",
        "metric": "0",
        "ref": "0",
        "use": "0",
        "iface": "docker",
        "mss": "0",
        "window": "0",
        "irtt": "0"
      },
      {
        "destination": "192.168.71.0",
        "gateway": "0.0.0.0",
        "genmask": "255.255.255.0",
        "flags": "U",
        "metric": "100",
        "ref": "0",
        "use": "0",
        "iface": "ens33",
        "mss": "0",
        "window": "0",
        "irtt": "0"
      }
    ]
"""
import jc.utils


def process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (dictionary) raw structured data to process

    Returns:

        dictionary   structured data with the following schema:

        [
          {
            "destination":  string,
            "gateway":      string,
            "genmask":      string,
            "flags":        string,
            "metric":       integer,
            "ref":          integer,
            "use":          integer,
            "mss":          integer,
            "window":       integer,
            "irtt":         integer,
            "iface":        string
          }
        ]
    """
    for entry in proc_data:
        int_list = ['metric', 'ref', 'use', 'mss', 'window', 'irtt']
        for key in int_list:
            if key in entry:
                try:
                    key_int = int(entry[key])
                    entry[key] = key_int
                except (ValueError):
                    entry[key] = None

    return proc_data


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        dictionary   raw or processed structured data
    """

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'aix', 'freebsd']

    if not quiet:
        jc.utils.compatibility(__name__, compatible)

    # code adapted from Conor Heine at:
    # https://gist.github.com/cahna/43a1a3ff4d075bcd71f9d7120037a501

    cleandata = data.splitlines()[1:]
    headers = [h for h in ' '.join(cleandata[0].lower().strip().split()).split() if h]
    raw_data = map(lambda s: s.strip().split(None, len(headers) - 1), cleandata[1:])
    raw_output = [dict(zip(headers, r)) for r in raw_data]

    if raw:
        return raw_output
    else:
        return process(raw_output)
