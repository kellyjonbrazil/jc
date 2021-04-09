[Home](https://kellyjonbrazil.github.io/jc/)

# jc.parsers.group
jc - JSON CLI output utility `/etc/group` file parser

Usage (cli):

    $ cat /etc/group | jc --group

Usage (module):

    import jc.parsers.group
    result = jc.parsers.group.parse(group_file_output)

Schema:

    [
      {
        "group_name":    string,
        "password":      string,
        "gid":           integer,
        "members": [
                         string
        ]
      }
    ]

Examples:

    $ cat /etc/group | jc --group -p
    [
      {
        "group_name": "nobody",
        "password": "*",
        "gid": -2,
        "members": []
      },
      {
        "group_name": "nogroup",
        "password": "*",
        "gid": -1,
        "members": []
      },
      {
        "group_name": "wheel",
        "password": "*",
        "gid": 0,
        "members": [
          "root"
        ]
      },
      {
        "group_name": "certusers",
        "password": "*",
        "gid": 29,
        "members": [
          "root",
          "_jabber",
          "_postfix",
          "_cyrus",
          "_calendar",
          "_dovecot"
        ]
      },
      ...
    ]

    $ cat /etc/group | jc --group -p -r
    [
      {
        "group_name": "nobody",
        "password": "*",
        "gid": "-2",
        "members": [
          ""
        ]
      },
      {
        "group_name": "nogroup",
        "password": "*",
        "gid": "-1",
        "members": [
          ""
        ]
      },
      {
        "group_name": "wheel",
        "password": "*",
        "gid": "0",
        "members": [
          "root"
        ]
      },
      {
        "group_name": "certusers",
        "password": "*",
        "gid": "29",
        "members": [
          "root",
          "_jabber",
          "_postfix",
          "_cyrus",
          "_calendar",
          "_dovecot"
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
Compatibility:  linux, darwin, aix, freebsd

Version 1.2 by Kelly Brazil (kellyjonbrazil@gmail.com)
