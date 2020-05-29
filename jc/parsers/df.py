"""jc - JSON CLI output utility df Parser

Usage:

    specify --df as the first argument if the piped input is coming from df

Compatibility:

    'linux', 'darwin', 'freebsd'

Examples:

    $ df | jc --df -p
    [
      {
        "filesystem": "devtmpfs",
        "1k_blocks": 1918820,
        "used": 0,
        "available": 1918820,
        "use_percent": 0,
        "mounted_on": "/dev"
      },
      {
        "filesystem": "tmpfs",
        "1k_blocks": 1930668,
        "used": 0,
        "available": 1930668,
        "use_percent": 0,
        "mounted_on": "/dev/shm"
      },
      {
        "filesystem": "tmpfs",
        "1k_blocks": 1930668,
        "used": 11800,
        "available": 1918868,
        "use_percent": 1,
        "mounted_on": "/run"
      },
      ...
    ]

    $ df | jc --df -p -r
    [
      {
        "filesystem": "devtmpfs",
        "1k_blocks": "1918820",
        "used": "0",
        "available": "1918820",
        "use_percent": "0%",
        "mounted_on": "/dev"
      },
      {
        "filesystem": "tmpfs",
        "1k_blocks": "1930668",
        "used": "0",
        "available": "1930668",
        "use_percent": "0%",
        "mounted_on": "/dev/shm"
      },
      {
        "filesystem": "tmpfs",
        "1k_blocks": "1930668",
        "used": "11800",
        "available": "1918868",
        "use_percent": "1%",
        "mounted_on": "/run"
      },
      ...
    ]
"""
import jc.utils
import jc.parsers.universal


class info():
    version = '1.3'
    description = 'df command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'freebsd']
    magic_commands = ['df']


__version__ = info.version


def process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (dictionary) raw structured data to process

    Returns:

        List of dictionaries. Structured data with the following schema:

        [
          {
            "filesystem":        string,
            "size":              string,
            "1k_blocks":         integer,
            "512_blocks":        integer,
            "used":              integer,
            "available":         integer,
            "capacity_percent":  integer,
            "ifree":             integer,
            "iused":             integer,
            "use_percent":       integer,
            "iused_percent":     integer,
            "mounted_on":        string
          }
        ]
    """

    for entry in proc_data:
        # change 'avail' to 'available'
        if 'avail' in entry:
            entry['available'] = entry.pop('avail')

        # change 'use%' to 'use_percent'
        if 'use%' in entry:
            entry['use_percent'] = entry.pop('use%')

        # change 'capacity' to 'capacity_percent'
        if 'capacity' in entry:
            entry['capacity_percent'] = entry.pop('capacity')

        # change '%iused' to 'iused_percent'
        if '%iused' in entry:
            entry['iused_percent'] = entry.pop('%iused')

        # change any entry for key with '_blocks' in the name to int
        for k in entry:
            if '_blocks' in str(k):
                try:
                    blocks_int = int(entry[k])
                    entry[k] = blocks_int
                except (ValueError):
                    entry[k] = None

        # remove percent sign from 'use_percent', 'capacity_percent', and 'iused_percent'
        if 'use_percent' in entry:
            entry['use_percent'] = entry['use_percent'].rstrip('%')

        if 'capacity_percent' in entry:
            entry['capacity_percent'] = entry['capacity_percent'].rstrip('%')

        if 'iused_percent' in entry:
            entry['iused_percent'] = entry['iused_percent'].rstrip('%')

        # change used, available, use_percent, capacity_percent, ifree, iused, iused_percent to int
        int_list = ['used', 'available', 'use_percent', 'capacity_percent', 'ifree', 'iused', 'iused_percent']
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

        List of dictionaries. Raw or processed structured data.
    """

    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

    cleandata = data.splitlines()

    # fix headers
    cleandata[0] = cleandata[0].lower()
    cleandata[0] = cleandata[0].replace('-', '_')
    cleandata[0] = cleandata[0].replace('mounted on', 'mounted_on')

    # parse the data
    raw_output = jc.parsers.universal.sparse_table_parse(cleandata)

    if raw:
        return raw_output
    else:
        return process(raw_output)
