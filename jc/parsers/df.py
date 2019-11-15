"""jc - JSON CLI output utility df Parser

Usage:
    specify --df as the first argument if the piped input is coming from df

Examples:

    $ df | jc --df -p
    [
      {
        "filesystem": "devtmpfs",
        "1k-blocks": 1918820,
        "used": 0,
        "available": 1918820,
        "use_percent": 0,
        "mounted_on": "/dev"
      },
      {
        "filesystem": "tmpfs",
        "1k-blocks": 1930668,
        "used": 0,
        "available": 1930668,
        "use_percent": 0,
        "mounted_on": "/dev/shm"
      },
      {
        "filesystem": "tmpfs",
        "1k-blocks": 1930668,
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
        "1k-blocks": "1918820",
        "used": "0",
        "available": "1918820",
        "use_percent": "0%",
        "mounted_on": "/dev"
      },
      {
        "filesystem": "tmpfs",
        "1k-blocks": "1930668",
        "used": "0",
        "available": "1930668",
        "use_percent": "0%",
        "mounted_on": "/dev/shm"
      },
      {
        "filesystem": "tmpfs",
        "1k-blocks": "1930668",
        "used": "11800",
        "available": "1918868",
        "use_percent": "1%",
        "mounted_on": "/run"
      },
      ...
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
            "filesystem":   string,
            "size":         string,
            "1k-blocks":    integer,
            "used":         integer,
            "available":    integer,
            "use_percent":  integer,
            "mounted_on":   string
          }
        ]
    """
    for entry in proc_data:
        # change any entry for key with '-blocks' in the name to int
        for k in entry:
            if str(k).find('-blocks') != -1:
                try:
                    blocks_int = int(entry[k])
                    entry[k] = blocks_int
                except (ValueError):
                    entry[k] = None

        # remove percent sign from 'use_percent'
        if 'use_percent' in entry:
            entry['use_percent'] = entry['use_percent'].rstrip('%')

        # change used, available, and use_percent to int
        int_list = ['used', 'available', 'use_percent']
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
    compatible = ['linux']

    if not quiet:
        jc.utils.compatibility(__name__, compatible)

    cleandata = data.splitlines()
    fix_headers = cleandata[0].lower().replace('avail ', 'available ')
    fix_headers = fix_headers.replace('use%', 'use_percent')
    fix_headers = fix_headers.replace('mounted on', 'mounted_on')
    headers = [h for h in ' '.join(fix_headers.strip().split()).split() if h]

    raw_data = map(lambda s: s.strip().split(None, len(headers) - 1), cleandata[1:])
    raw_output = [dict(zip(headers, r)) for r in raw_data]

    if raw:
        return raw_output
    else:
        return process(raw_output)
