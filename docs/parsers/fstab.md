[Home](https://kellyjonbrazil.github.io/jc/)

# jc.parsers.fstab
jc - JSON CLI output utility `fstab` file parser

Usage (cli):

    $ cat /etc/fstab | jc --fstab

Usage (module):

    import jc.parsers.fstab
    result = jc.parsers.fstab.parse(fstab_command_output)

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
Compatibility:  linux, freebsd

Version 1.6 by Kelly Brazil (kellyjonbrazil@gmail.com)
