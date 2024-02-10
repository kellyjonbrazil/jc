[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.group"></a>

# jc.parsers.group

jc - JSON Convert `/etc/group` file parser

Usage (cli):

    $ cat /etc/group | jc --group

Usage (module):

    import jc
    result = jc.parse('group', group_file_output)

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

<a id="jc.parsers.group.parse"></a>

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
Compatibility:  linux, darwin, aix, freebsd

Source: [`jc/parsers/group.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/group.py)

Version 1.5 by Kelly Brazil (kellyjonbrazil@gmail.com)
