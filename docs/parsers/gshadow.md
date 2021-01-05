
# jc.parsers.gshadow
jc - JSON CLI output utility `/etc/gshadow` file parser

Usage (cli):

    $ cat /etc/gshadow | jc --gshadow

Usage (module):

    import jc.parsers.gshadow
    result = jc.parsers.gshadow.parse(gshadow_file_output)

Compatibility:

    'linux', 'aix', 'freebsd'

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


## info
```python
info()
```


## process
```python
process(proc_data)
```

Final processing to conform to the schema.

Parameters:

    proc_data:   (List of Dictionaries) raw structured data to process

Returns:

    List of Dictionaries. Structured data with the following schema:

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

