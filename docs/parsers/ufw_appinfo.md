[Home](https://kellyjonbrazil.github.io/jc/)

# jc.parsers.ufw_appinfo
jc - JSON CLI output utility `ufw app info [application]` command output parser

Because `ufw` application definitions allow overlapping ports and port ranges, this parser preserves that behavior, but also provides `normalized` lists and ranges that remove duplicate ports and merge overlapping ranges.

Usage (cli):

    $ ufw app info OpenSSH | jc --ufw-appinfo

    or

    $ jc ufw app info OpenSSH

Usage (module):

    import jc.parsers.ufw_appinfo
    result = jc.parsers.ufw_appinfo.parse(ufw_appinfo_command_output)

Schema:

    {
      "profile":                  string,
      "title":                    string,
      "description":              string,
      "tcp_list": [
                                  integer
      ],
      "tcp_ranges": [
        {
          "start":                integer,      # 'any' is converted to start/end: 0/65535
          "end":                  integer
        }
      ],
      "udp_list": [
                                  integer
      ],
      "udp_ranges": [
        {
          "start":                integer,      # 'any' is converted to start/end: 0/65535
          "end":                  integer
        }
      ],
      "normalized_tcp_list": [
                                  integers      # duplicates and overlapping are removed
      ],
      "normalized_tcp_ranges": [
        {
          "start":                integer,      # 'any' is converted to start/end: 0/65535
          "end":                  integers      # overlapping are merged
        }
      ],
      "normalized_udp_list": [
                                  integers      # duplicates and overlapping are removed
      ],
      "normalized_udp_ranges": [
        {
          "start":                integer,      # 'any' is converted to start/end: 0/65535
          "end":                  integers      # overlapping are merged
        }
      ]
    }

Examples:

    $ ufw app info OpenSSH | jc --ufw-appinfo -p
    []

    $ ufw app info OpenSSH | jc --ufw-appinfo -p -r
    []


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

    Dictionary. Raw or processed structured data.

## Parser Information
Compatibility:  linux

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
