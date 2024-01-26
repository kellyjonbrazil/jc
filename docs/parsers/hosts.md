[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.hosts"></a>

# jc.parsers.hosts

jc - JSON Convert `/etc/hosts` file parser

Usage (cli):

    $ cat /etc/hosts | jc --hosts

Usage (module):

    import jc
    result = jc.parse('hosts', hosts_file_output)

Schema:

    [
      {
        "ip":           string,
        "hostname": [
                        string
        ]
      }
    ]

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

<a id="jc.parsers.hosts.parse"></a>

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
Compatibility:  linux, darwin, cygwin, win32, aix, freebsd

Source: [`jc/parsers/hosts.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/hosts.py)

Version 1.4 by Kelly Brazil (kellyjonbrazil@gmail.com)
