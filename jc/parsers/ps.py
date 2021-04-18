"""jc - JSON CLI output utility `ps` command output parser

`ps` options supported:
- `ef`
- `axu`

Usage (cli):

    $ ps | jc --ps

    or

    $ jc ps

Usage (module):

    import jc.parsers.ps
    result = jc.parsers.ps.parse(ps_command_output)

Schema:

    [
      {
        "uid":           string,
        "pid":           integer,
        "ppid":          integer,
        "c":             integer,
        "stime":         string,
        "tty":           string,    # ? or ?? = Null
        "tt":            string,    # ?? = Null
        "time":          string,
        "cmd":           string,
        "user":          string,
        "cpu_percent":   float,
        "mem_percent":   float,
        "vsz":           integer,
        "rss":           integer,
        "stat":          string,
        "start":         string,
        "command":       string
      }
    ]

Examples:

    $ ps -ef | jc --ps -p
    [
      {
        "uid": "root",
        "pid": 1,
        "ppid": 0,
        "c": 0,
        "stime": "Nov01",
        "tty": null,
        "time": "00:00:11",
        "cmd": "/usr/lib/systemd/systemd --switched-root --system --deserialize 22"
      },
      {
        "uid": "root",
        "pid": 2,
        "ppid": 0,
        "c": 0,
        "stime": "Nov01",
        "tty": null,
        "time": "00:00:00",
        "cmd": "[kthreadd]"
      },
      {
        "uid": "root",
        "pid": 4,
        "ppid": 2,
        "c": 0,
        "stime": "Nov01",
        "tty": null,
        "time": "00:00:00",
        "cmd": "[kworker/0:0H]"
      },
      ...
    ]

    $ ps -ef | jc --ps -p -r
    [
      {
        "uid": "root",
        "pid": "1",
        "ppid": "0",
        "c": "0",
        "stime": "Nov01",
        "tty": "?",
        "time": "00:00:11",
        "cmd": "/usr/lib/systemd/systemd --switched-root --system --deserialize 22"
      },
      {
        "uid": "root",
        "pid": "2",
        "ppid": "0",
        "c": "0",
        "stime": "Nov01",
        "tty": "?",
        "time": "00:00:00",
        "cmd": "[kthreadd]"
      },
      {
        "uid": "root",
        "pid": "4",
        "ppid": "2",
        "c": "0",
        "stime": "Nov01",
        "tty": "?",
        "time": "00:00:00",
        "cmd": "[kworker/0:0H]"
      },
      ...
    ]

    $ ps axu | jc --ps -p
    [
      {
        "user": "root",
        "pid": 1,
        "cpu_percent": 0.0,
        "mem_percent": 0.1,
        "vsz": 128072,
        "rss": 6784,
        "tty": null,
        "stat": "Ss",
        "start": "Nov09",
        "time": "0:08",
        "command": "/usr/lib/systemd/systemd --switched-root --system --deserialize 22"
      },
      {
        "user": "root",
        "pid": 2,
        "cpu_percent": 0.0,
        "mem_percent": 0.0,
        "vsz": 0,
        "rss": 0,
        "tty": null,
        "stat": "S",
        "start": "Nov09",
        "time": "0:00",
        "command": "[kthreadd]"
      },
      {
        "user": "root",
        "pid": 4,
        "cpu_percent": 0.0,
        "mem_percent": 0.0,
        "vsz": 0,
        "rss": 0,
        "tty": null,
        "stat": "S<",
        "start": "Nov09",
        "time": "0:00",
        "command": "[kworker/0:0H]"
      },
      ...
    ]

    $ ps axu | jc --ps -p -r
    [
      {
        "user": "root",
        "pid": "1",
        "cpu_percent": "0.0",
        "mem_percent": "0.1",
        "vsz": "128072",
        "rss": "6784",
        "tty": "?",
        "stat": "Ss",
        "start": "Nov09",
        "time": "0:08",
        "command": "/usr/lib/systemd/systemd --switched-root --system --deserialize 22"
      },
      {
        "user": "root",
        "pid": "2",
        "cpu_percent": "0.0",
        "mem_percent": "0.0",
        "vsz": "0",
        "rss": "0",
        "tty": "?",
        "stat": "S",
        "start": "Nov09",
        "time": "0:00",
        "command": "[kthreadd]"
      },
      {
        "user": "root",
        "pid": "4",
        "cpu_percent": "0.0",
        "mem_percent": "0.0",
        "vsz": "0",
        "rss": "0",
        "tty": "?",
        "stat": "S<",
        "start": "Nov09",
        "time": "0:00",
        "command": "[kworker/0:0H]"
      },
      ...
    ]
"""
import jc.utils
import jc.parsers.universal


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.5'
    description = '`ps` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'cygwin', 'aix', 'freebsd']
    magic_commands = ['ps']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured data to conform to the schema.
    """
    for entry in proc_data:
        # change key name '%cpu' to 'cpu_percent'
        if '%cpu' in entry:
            entry['cpu_percent'] = entry.pop('%cpu')

        # change key name '%mem' to 'mem_percent'
        if '%mem' in entry:
            entry['mem_percent'] = entry.pop('%mem')

        # convert ints and floats
        int_list = ['pid', 'ppid', 'c', 'vsz', 'rss']
        float_list = ['cpu_percent', 'mem_percent']
        for key in entry:
            if key in int_list:
                entry[key] = jc.utils.convert_to_int(entry[key])
            if key in float_list:
                entry[key] = jc.utils.convert_to_float(entry[key])

        # clean up other fields
        if 'tty' in entry:
            if entry['tty'] == '?' or entry['tty'] == '??':
                entry['tty'] = None

        if 'tt' in entry:
            if entry['tt'] == '??':
                entry['tt'] = None

    return proc_data


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of Dictionaries. Raw or processed structured data.
    """
    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

    cleandata = data.splitlines()
    raw_output = []

    if jc.utils.has_data(data):

        cleandata[0] = cleandata[0].lower()
        raw_output = jc.parsers.universal.simple_table_parse(cleandata)

    if raw:
        return raw_output
    else:
        return _process(raw_output)
