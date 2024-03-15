[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.findmnt"></a>

# jc.parsers.findmnt

jc - JSON Convert `findmnt` command output parser

Supports `-a`, `-l`, or no `findmnt` options.

> Note: Newer versions of `findmnt` have a JSON output option.

Usage (cli):

    $ findmnt | jc --findmnt

or

    $ jc findmnt

Usage (module):

    import jc
    result = jc.parse('findmnt', findmnt_command_output)

Schema:

    [
      {
        "target":                   string,
        "source":                   string,
        "fstype":                   string,
        "options": [
                                    string
        ],
        "kv_options": {
          "<key_name>":             string
        }
    ]

Examples:

    $ findmnt | jc --findmnt -p
    [
      {
        "target": "/",
        "source": "/dev/mapper/centos-root",
        "fstype": "xfs",
        "options": [
          "rw",
          "relatime",
          "seclabel",
          "attr2",
          "inode64",
          "noquota"
        ]
      },
      {
        "target": "/sys/fs/cgroup",
        "source": "tmpfs",
        "fstype": "tmpfs",
        "options": [
          "ro",
          "nosuid",
          "nodev",
          "noexec",
          "seclabel"
        ],
        "kv_options": {
          "mode": "755"
        }
      },
      ...
    ]

    $ findmnt | jc --findmnt -p -r
    [
      {
        "target": "/",
        "source": "/dev/mapper/centos-root",
        "fstype": "xfs",
        "options": "rw,relatime,seclabel,attr2,inode64,noquota"
      },
      {
        "target": "/sys/fs/cgroup",
        "source": "tmpfs",
        "fstype": "tmpfs",
        "options": "ro,nosuid,nodev,noexec,seclabel,mode=755"
      },
      ...
    ]

<a id="jc.parsers.findmnt.parse"></a>

### parse

```python
def parse(data: str,
          raw: bool = False,
          quiet: bool = False) -> List[Dict[str, Any]]
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) unprocessed output if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    List of Dictionaries. Raw or processed structured data.

### Parser Information
Compatibility:  linux

Source: [`jc/parsers/findmnt.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/findmnt.py)

Version 1.1 by Kelly Brazil (kellyjonbrazil@gmail.com)
