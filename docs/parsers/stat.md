[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.stat"></a>

# jc.parsers.stat

jc - JSON Convert `stat` command output parser

The `xxx_epoch` calculated timestamp fields are naive. (i.e. based on the
local time of the system the parser is run on)

The `xxx_epoch_utc` calculated timestamp fields are timezone-aware and are
only available if the timezone field is UTC.

Usage (cli):

    $ stat * | jc --stat

or

    $ jc stat *

Usage (module):

    import jc
    result = jc.parse('stat', stat_command_output)

Schema:

    [
      {
        "file":                     string,
        "link_to"                   string,
        "size":                     integer,
        "blocks":                   integer,
        "io_blocks":                integer,
        "type":                     string,
        "device":                   string,
        "inode":                    integer,
        "links":                    integer,
        "access":                   string,
        "flags":                    string,
        "uid":                      integer,
        "user":                     string,
        "gid":                      integer,
        "group":                    string,
        "access_time":              string,    # - = null
        "access_time_epoch":        integer,   # naive timestamp
        "access_time_epoch_utc":    integer,   # timezone-aware timestamp
        "modify_time":              string,    # - = null
        "modify_time_epoch":        integer,   # naive timestamp
        "modify_time_epoch_utc":    integer,   # timezone-aware timestamp
        "change_time":              string,    # - = null
        "change_time_epoch":        integer,   # naive timestamp
        "change_time_epoch_utc":    integer,   # timezone-aware timestamp
        "birth_time":               string,    # - = null
        "birth_time_epoch":         integer,   # naive timestamp
        "birth_time_epoch_utc":     integer,   # timezone-aware timestamp
        "unix_device":              integer,
        "rdev":                     integer,
        "block_size":               integer,
        "unix_flags":               string
      }
    ]

Examples:

    $ stat /bin/* | jc --stat -p
    [
      {
        "file": "/bin/bash",
        "size": 1113504,
        "blocks": 2176,
        "io_blocks": 4096,
        "type": "regular file",
        "device": "802h/2050d",
        "inode": 131099,
        "links": 1,
        "access": "0755",
        "flags": "-rwxr-xr-x",
        "uid": 0,
        "user": "root",
        "gid": 0,
        "group": "root",
        "access_time": "2019-11-14 08:18:03.509681766 +0000",
        "modify_time": "2019-06-06 22:28:15.000000000 +0000",
        "change_time": "2019-08-12 17:21:29.521945390 +0000",
        "birth_time": null,
        "access_time_epoch": 1573748283,
        "access_time_epoch_utc": 1573719483,
        "modify_time_epoch": 1559885295,
        "modify_time_epoch_utc": 1559860095,
        "change_time_epoch": 1565655689,
        "change_time_epoch_utc": 1565630489,
        "birth_time_epoch": null,
        "birth_time_epoch_utc": null
      },
      {
        "file": "/bin/btrfs",
        "size": 716464,
        "blocks": 1400,
        "io_blocks": 4096,
        "type": "regular file",
        "device": "802h/2050d",
        "inode": 131100,
        "links": 1,
        "access": "0755",
        "flags": "-rwxr-xr-x",
        "uid": 0,
        "user": "root",
        "gid": 0,
        "group": "root",
        "access_time": "2019-11-14 08:18:28.990834276 +0000",
        "modify_time": "2018-03-12 23:04:27.000000000 +0000",
        "change_time": "2019-08-12 17:21:29.545944399 +0000",
        "birth_time": null,
        "access_time_epoch": 1573748308,
        "access_time_epoch_utc": 1573719508,
        "modify_time_epoch": 1520921067,
        "modify_time_epoch_utc": 1520895867,
        "change_time_epoch": 1565655689,
        "change_time_epoch_utc": 1565630489,
        "birth_time_epoch": null,
        "birth_time_epoch_utc": null
      },
      ...
    ]

    $ stat /bin/* | jc --stat -p -r
    [
      {
        "file": "/bin/bash",
        "size": "1113504",
        "blocks": "2176",
        "io_blocks": "4096",
        "type": "regular file",
        "device": "802h/2050d",
        "inode": "131099",
        "links": "1",
        "access": "0755",
        "flags": "-rwxr-xr-x",
        "uid": "0",
        "user": "root",
        "gid": "0",
        "group": "root",
        "access_time": "2019-11-14 08:18:03.509681766 +0000",
        "modify_time": "2019-06-06 22:28:15.000000000 +0000",
        "change_time": "2019-08-12 17:21:29.521945390 +0000",
        "birth_time": null
      },
      {
        "file": "/bin/btrfs",
        "size": "716464",
        "blocks": "1400",
        "io_blocks": "4096",
        "type": "regular file",
        "device": "802h/2050d",
        "inode": "131100",
        "links": "1",
        "access": "0755",
        "flags": "-rwxr-xr-x",
        "uid": "0",
        "user": "root",
        "gid": "0",
        "group": "root",
        "access_time": "2019-11-14 08:18:28.990834276 +0000",
        "modify_time": "2018-03-12 23:04:27.000000000 +0000",
        "change_time": "2019-08-12 17:21:29.545944399 +0000",
        "birth_time": null
      },
      ...
    ]

<a id="jc.parsers.stat.parse"></a>

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

Source: [`jc/parsers/stat.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/stat.py)

Version 1.13 by Kelly Brazil (kellyjonbrazil@gmail.com)
