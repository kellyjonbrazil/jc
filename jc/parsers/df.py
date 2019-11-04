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
    "mounted": "/dev"
  },
  {
    "filesystem": "tmpfs",
    "1k-blocks": 1930668,
    "used": 0,
    "available": 1930668,
    "use_percent": 0,
    "mounted": "/dev/shm"
  },
  {
    "filesystem": "tmpfs",
    "1k-blocks": 1930668,
    "used": 11800,
    "available": 1918868,
    "use_percent": 1,
    "mounted": "/run"
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
    "mounted": "/dev"
  },
  {
    "filesystem": "tmpfs",
    "1k-blocks": "1930668",
    "used": "0",
    "available": "1930668",
    "use_percent": "0%",
    "mounted": "/dev/shm"
  },
  {
    "filesystem": "tmpfs",
    "1k-blocks": "1930668",
    "used": "11800",
    "available": "1918868",
    "use_percent": "1%",
    "mounted": "/run"
  },
  ...
]
"""


def process(proc_data):
    for entry in proc_data:
        # change any entry for key with '-blocks' in the name to int
        for k in entry:
            if str(k).find('-blocks') != -1:
                try:
                    blocks_int = int(entry[k])
                    entry[k] = blocks_int
                except (ValueError, TypeError):
                    entry[k] = None

        # change 'used' to int
        if 'used' in entry:
            try:
                used_int = int(entry['used'])
                entry['used'] = used_int
            except (ValueError, TypeError):
                entry['used'] = None

        # change 'available' to int
        if 'available' in entry:
            try:
                available_int = int(entry['available'])
                entry['available'] = available_int
            except (ValueError, TypeError):
                entry['available'] = None
        else:
            entry['available'] = None

        # remove percent sign from 'use_percent' and change to int
        if 'use_percent' in entry:
            try:
                use_percent_int = entry['use_percent'].rstrip('%')
                use_percent_int = int(use_percent_int)
                entry['use_percent'] = use_percent_int
            except (ValueError, TypeError):
                entry['use_percent'] = None

    return proc_data


def parse(data, raw=False):

    # code adapted from Conor Heine at:
    # https://gist.github.com/cahna/43a1a3ff4d075bcd71f9d7120037a501

    cleandata = data.splitlines()
    headers = [h for h in ' '.join(cleandata[0].lower().strip().split()).split() if h]

    # clean up 'use%' header
    # even though % in a key is valid json, it can make things difficult
    headers = ['use_percent' if x == 'use%' else x for x in headers]

    raw_data = map(lambda s: s.strip().split(None, len(headers) - 1), cleandata[1:])
    raw_output = [dict(zip(headers, r)) for r in raw_data]

    if raw:
        return raw_output
    else:
        return process(raw_output)
