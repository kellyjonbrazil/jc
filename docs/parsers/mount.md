# jc.parsers.mount
jc - JSON CLI output utility mount Parser

Usage:
    specify --mount as the first argument if the piped input is coming from mount

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

## process
```python
process(proc_data)
```

schema:

    [
      {
        "filesystem":   string,
        "mount_point":  string,
        "type":         string,
        "access": [
                        string
        ]
      }
    ]

    nothing to process

## parse
```python
parse(data, raw=False, quiet=False)
```

Main parsing function

Arguments:

    raw:    (boolean) output preprocessed JSON if True
    quiet:  (boolean) suppress warning messages if True

