[Home](https://kellyjonbrazil.github.io/jc/)

# jc.parsers.hosts
jc - JSON CLI output utility `/etc/hosts` file parser

Usage (cli):

    $ cat /etc/hosts | jc --hosts

Usage (module):

    import jc.parsers.hosts
    result = jc.parsers.hosts.parse(hosts_file_output)

Schema:

    [
      {
        "ip":           string,
        "hostname": [
                        string
        ]
      }
    ]

Compatibility:

    'linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd'

Examples:

    $ cat /etc/hosts | jc --hosts -p
    [
      {
        "ip": "127.0.0.1",
        "hostname": [
          "localhost"
        ]
      },
      {
        "ip": "127.0.1.1",
        "hostname": [
          "root-ubuntu"
        ]
      },
      {
        "ip": "::1",
        "hostname": [
          "ip6-localhost",
          "ip6-loopback"
        ]
      },
      {
        "ip": "fe00::0",
        "hostname": [
          "ip6-localnet"
        ]
      },
      {
        "ip": "ff00::0",
        "hostname": [
          "ip6-mcastprefix"
        ]
      },
      {
        "ip": "ff02::1",
        "hostname": [
          "ip6-allnodes"
        ]
      },
      {
        "ip": "ff02::2",
        "hostname": [
          "ip6-allrouters"
        ]
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
Compatibility:  linux, darwin, cygwin, win32, aix, freebsd

Version 1.3 by Kelly Brazil (kellyjonbrazil@gmail.com)
