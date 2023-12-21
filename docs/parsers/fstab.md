[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.fstab"></a>

# jc.parsers.fstab

jc - JSON Convert `fstab` file parser

Usage (cli):

    $ cat /etc/fstab | jc --fstab

Usage (module):

    import jc
    result = jc.parse('fstab', fstab_command_output)

Schema:

    [
      {
        "fs_spec":      string,
        "fs_file":      string,
        "fs_vfstype":   string,
        "fs_mntops":    string,
        "fs_freq":      integer,
        "fs_passno":    integer
      }
    ]

Examples:

    $ cat /etc/fstab | jc --fstab -p
    [
      {
        "fs_spec": "/dev/mapper/centos-root",
        "fs_file": "/",
        "fs_vfstype": "xfs",
        "fs_mntops": "defaults",
        "fs_freq": 0,
        "fs_passno": 0
      },
      {
        "fs_spec": "UUID=05d927bb-5875-49e3-ada1-7f46cb31c932",
        "fs_file": "/boot",
        "fs_vfstype": "xfs",
        "fs_mntops": "defaults",
        "fs_freq": 0,
        "fs_passno": 0
      },
      {
        "fs_spec": "/dev/mapper/centos-swap",
        "fs_file": "swap",
        "fs_vfstype": "swap",
        "fs_mntops": "defaults",
        "fs_freq": 0,
        "fs_passno": 0
      }
    ]

    $ cat /etc/fstab | jc --fstab -p -r
    [
      {
        "fs_spec": "/dev/mapper/centos-root",
        "fs_file": "/",
        "fs_vfstype": "xfs",
        "fs_mntops": "defaults",
        "fs_freq": "0",
        "fs_passno": "0"
      },
      {
        "fs_spec": "UUID=05d927bb-5875-49e3-ada1-7f46cb31c932",
        "fs_file": "/boot",
        "fs_vfstype": "xfs",
        "fs_mntops": "defaults",
        "fs_freq": "0",
        "fs_passno": "0"
      },
      {
        "fs_spec": "/dev/mapper/centos-swap",
        "fs_file": "swap",
        "fs_vfstype": "swap",
        "fs_mntops": "defaults",
        "fs_freq": "0",
        "fs_passno": "0"
      }
    ]

<a id="jc.parsers.fstab.parse"></a>

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
Compatibility:  linux, freebsd

Source: [`jc/parsers/fstab.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/fstab.py)

Version 1.7 by Kelly Brazil (kellyjonbrazil@gmail.com)
