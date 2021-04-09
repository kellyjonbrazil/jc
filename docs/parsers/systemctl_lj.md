[Home](https://kellyjonbrazil.github.io/jc/)

# jc.parsers.systemctl_lj
jc - JSON CLI output utility `systemctl list-jobs` command output parser

Usage (cli):

    $ systemctl list-jobs | jc --systemctl-lj

    or

    $ jc systemctl list-jobs

Usage (module):

    import jc.parsers.systemctl_lj
    result = jc.parsers.systemctl_lj.parse(systemctl_lj_command_output)

Schema:

    [
      {
        "job":      integer,
        "unit":     string,
        "type":     string,
        "state":    string
      }
    ]

Compatibility:

    'linux'

Examples:

    $ systemctl list-jobs| jc --systemctl-lj -p
    [
      {
        "job": 3543,
        "unit": "nginxAfterGlusterfs.service",
        "type": "start",
        "state": "waiting"
      },
      {
        "job": 3545,
        "unit": "glusterReadyForLocalhostMount.service",
        "type": "start",
        "state": "running"
      },
      {
        "job": 3506,
        "unit": "nginx.service",
        "type": "start",
        "state": "waiting"
      }
    ]

    $ systemctl list-jobs| jc --systemctl-lj -p -r
    [
      {
        "job": "3543",
        "unit": "nginxAfterGlusterfs.service",
        "type": "start",
        "state": "waiting"
      },
      {
        "job": "3545",
        "unit": "glusterReadyForLocalhostMount.service",
        "type": "start",
        "state": "running"
      },
      {
        "job": "3506",
        "unit": "nginx.service",
        "type": "start",
        "state": "waiting"
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
Compatibility:  linux

Version 1.4 by Kelly Brazil (kellyjonbrazil@gmail.com)
