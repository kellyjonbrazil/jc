"""jc - JSON CLI output utility airport -I Parser

Usage:

    specify --airport as the first argument if the piped input is coming from airport -I (OSX)

    This program can be found at:
    /System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport

Compatibility:

    'darwin'

Examples:

    $ airport -I | jc --airport -p
    {
      "agrctlrssi": -66,
      "agrextrssi": 0,
      "agrctlnoise": -90,
      "agrextnoise": 0,
      "state": "running",
      "op_mode": "station",
      "lasttxrate": 195,
      "maxrate": 867,
      "lastassocstatus": 0,
      "802_11_auth": "open",
      "link_auth": "wpa2-psk",
      "bssid": "3c:37:86:15:ad:f9",
      "ssid": "SnazzleDazzle",
      "mcs": 0,
      "channel": "48,80"
    }

    $ airport -I | jc --airport -p -r
    {
      "agrctlrssi": "-66",
      "agrextrssi": "0",
      "agrctlnoise": "-90",
      "agrextnoise": "0",
      "state": "running",
      "op_mode": "station",
      "lasttxrate": "195",
      "maxrate": "867",
      "lastassocstatus": "0",
      "802_11_auth": "open",
      "link_auth": "wpa2-psk",
      "bssid": "3c:37:86:15:ad:f9",
      "ssid": "SnazzleDazzle",
      "mcs": "0",
      "channel": "48,80"
    }
"""
import jc.utils


class info():
    version = '1.1'
    description = 'airport -I command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    # details = 'enter any other details here'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['darwin']
    magic_commands = ['airport -I']


__version__ = info.version


def process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (dictionary) raw structured data to process

    Returns:

        Dictionary. Structured data with the following schema:

        {
          "agrctlrssi":        integer,
          "agrextrssi":        integer,
          "agrctlnoise":       integer,
          "agrextnoise":       integer,
          "state":             string,
          "op_mode":           string,
          "lasttxrate":        integer,
          "maxrate":           integer,
          "lastassocstatus":   integer,
          "802_11_auth":       string,
          "link_auth":         string,
          "bssid":             string,
          "ssid":              string,
          "mcs":               integer,
          "channel":           string
        }
    """
    # integer changes
    int_list = ['agrctlrssi', 'agrextrssi', 'agrctlnoise', 'agrextnoise',
                'lasttxrate', 'maxrate', 'lastassocstatus', 'mcs']
    for key in proc_data:
        if key in int_list:
            try:
                proc_data[key] = int(proc_data[key])
            except (ValueError):
                proc_data[key] = None

    return proc_data


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data.
    """
    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

    raw_output = {}

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):
            linedata = line.split(':', maxsplit=1)
            raw_output[linedata[0].strip().lower().replace(' ', '_').replace('.', '_')] = linedata[1].strip()

    if raw:
        return raw_output
    else:
        return process(raw_output)
