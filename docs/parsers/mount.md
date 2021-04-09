[Home](https://kellyjonbrazil.github.io/jc/)

# jc.parsers.mount
jc - JSON CLI output utility `mount` command output parser

Usage (cli):

    $ mount | jc --mount

    or

    $ jc mount

Usage (module):

    import jc.parsers.mount
    result = jc.parsers.mount.parse(mount_command_output)

Schema:

    [
      {
        "filesystem":       string,
        "mount_point":      string,
        "type":             string,
        "access": [
                            string
        ]
      }
    ]

Example:

    $ mount | jc --mount -p
    [
      {
        "filesystem": "sysfs",
        "mount_point": "/sys",
        "type": "sysfs",
        "access": [
          "rw",
          "nosuid",
          "nodev",
          "noexec",
          "relatime"
        ]
      },
      {
        "filesystem": "proc",
        "mount_point": "/proc",
        "type": "proc",
        "access": [
          "rw",
          "nosuid",
          "nodev",
          "noexec",
          "relatime"
        ]
      },
      {
        "filesystem": "udev",
        "mount_point": "/dev",
        "type": "devtmpfs",
        "access": [
          "rw",
          "nosuid",
          "relatime",
          "size=977500k",
          "nr_inodes=244375",
          "mode=755"
        ]
      },
      ...
    ]


## info
```python
info()
```
Provides parser metadata (version, author, etc.)

## parse
```python
parse(data, raw=False, quiet=False)
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) output preprocessed JSON if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    List of Dictionaries. Raw or processed structured data.

## Parser Information
Compatibility:  linux, darwin, freebsd

Version 1.6 by Kelly Brazil (kellyjonbrazil@gmail.com)
