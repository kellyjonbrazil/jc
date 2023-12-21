[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.gshadow"></a>

# jc.parsers.gshadow

jc - JSON Convert `/etc/gshadow` file parser

Usage (cli):

    $ cat /etc/gshadow | jc --gshadow

Usage (module):

    import jc
    result = jc.parse('gshadow', gshadow_file_output)

Schema:

    [
      {
        "group_name":       string,
        "password":         string,
        "administrators": [
                            string
        ],
        "members": [
                            string
        ]
      }
    ]

Examples:

    $ cat /etc/gshadow | jc --gshadow -p
    [
      {
        "group_name": "root",
        "password": "*",
        "administrators": [],
        "members": []
      },
      {
        "group_name": "adm",
        "password": "*",
        "administrators": [],
        "members": [
          "syslog",
          "joeuser"
        ]
      },
      ...
    ]

    $ cat /etc/gshadow | jc --gshadow -p -r
    [
      {
        "group_name": "root",
        "password": "*",
        "administrators": [
          ""
        ],
        "members": [
          ""
        ]
      },
      {
        "group_name": "adm",
        "password": "*",
        "administrators": [
          ""
        ],
        "members": [
          "syslog",
          "joeuser"
        ]
      },
      ...
    ]

<a id="jc.parsers.gshadow.parse"></a>

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
Compatibility:  linux, aix, freebsd

Source: [`jc/parsers/gshadow.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/gshadow.py)

Version 1.3 by Kelly Brazil (kellyjonbrazil@gmail.com)
