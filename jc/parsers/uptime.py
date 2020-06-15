"""jc - JSON CLI output utility uptime Parser

Usage:

    specify --uptime as the first argument if the piped input is coming from uptime

Compatibility:

    'linux', 'darwin', 'cygwin', 'aix', 'freebsd'

Example:

    $ uptime | jc --uptime -p
    {
      "time": "11:30:44",
      "uptime": "1 day, 21:17",
      "users": 1,
      "load_1m": 0.01,
      "load_5m": 0.04,
      "load_15m": 0.05
    }

    $ uptime | jc --uptime -p -r
    {
      "time": "11:31:09",
      "uptime": "1 day, 21:17",
      "users": "1",
      "load_1m": "0.00",
      "load_5m": "0.04",
      "load_15m": "0.05"
    }
"""
import jc.utils


class info():
    version = '1.2'
    description = 'uptime command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'cygwin', 'aix', 'freebsd']
    magic_commands = ['uptime']


__version__ = info.version


def process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (dictionary) raw structured data to process

    Returns:

        Dictionary. Structured data with the following schema:

        {
          "time":     string,
          "uptime":   string,
          "users":    integer,
          "load_1m":  float,
          "load_5m":  float,
          "load_15m": float
        }
    """
    int_list = ['users']
    for key in int_list:
        if key in proc_data:
            try:
                key_int = int(proc_data[key])
                proc_data[key] = key_int
            except (ValueError):
                proc_data[key] = None

    float_list = ['load_1m', 'load_5m', 'load_15m']
    for key in float_list:
        if key in proc_data:
            try:
                key_float = float(proc_data[key])
                proc_data[key] = key_float
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

        Dictionary. Raw or processed structured data
    """
    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

    raw_output = {}
    cleandata = data.splitlines()

    if jc.utils.has_data(data):

        parsed_line = cleandata[0].split()

        # allow space for odd times
        while len(parsed_line) < 20:
            parsed_line.insert(2, ' ')

        # find first part of time
        for i, word in enumerate(parsed_line[2:]):
            if word != ' ':
                marker = i + 2
                break

        raw_output['time'] = parsed_line[0]
        raw_output['uptime'] = ' '.join(parsed_line[marker:13]).lstrip().rstrip(',')
        raw_output['users'] = parsed_line[13]
        raw_output['load_1m'] = parsed_line[17].rstrip(',')
        raw_output['load_5m'] = parsed_line[18].rstrip(',')
        raw_output['load_15m'] = parsed_line[19]

    if raw:
        return raw_output
    else:
        return process(raw_output)
