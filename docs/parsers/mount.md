[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.mount"></a>

# jc.parsers.mount

jc - JSON Convert `mount` command output parser

Usage (cli):

    $ mount | jc --mount

or

    $ jc mount

Usage (module):

    import jc
    result = jc.parse('mount', mount_command_output)

Schema:

    [
      {
        "filesystem":       string,
        "mount_point":      string,
        "type":             string,
        "options": [
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
        "options": [
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
        "options": [
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
        "options": [
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

<a id="jc.parsers.mount.parse"></a>

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
Compatibility:  linux, darwin, freebsd, aix

Source: [`jc/parsers/mount.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/mount.py)

Version 1.11 by Kelly Brazil (kellyjonbrazil@gmail.com)
