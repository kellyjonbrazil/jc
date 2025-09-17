[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.df"></a>

# jc.parsers.df

jc - JSON Convert `df` command output parser

Values are normalized to bytes when using `df -h`.

Usage (cli):

    $ df | jc --df

or

    $ jc df

Usage (module):

    import jc
    result = jc.parse('df', df_command_output)

Schema:

    [
      {
        "filesystem":        string,
        "size":              integer,
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

<a id="jc.parsers.df.parse"></a>

### parse

```python
def parse(data, raw=False, quiet=False)
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) unprocessed output if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    List of Dictionaries. Raw or processed structured data.

### Parser Information
Compatibility:  linux, darwin, freebsd

Source: [`jc/parsers/df.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/df.py)

Version 2.1 by Kelly Brazil (kellyjonbrazil@gmail.com)
