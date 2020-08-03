
# jc.parsers.shadow
jc - JSON CLI output utility /etc/shadow file Parser

Usage:

    specify --shadow as the first argument if the piped input is coming from /etc/shadow

Compatibility:

    'linux', 'darwin', 'aix', 'freebsd'

Examples:

    $ sudo cat /etc/shadow | jc --shadow -p
    [
      {
        "username": "root",
        "password": "*",
        "last_changed": 18113,
        "minimum": 0,
        "maximum": 99999,
        "warn": 7,
        "inactive": null,
        "expire": null
      },
      {
        "username": "daemon",
        "password": "*",
        "last_changed": 18113,
        "minimum": 0,
        "maximum": 99999,
        "warn": 7,
        "inactive": null,
        "expire": null
      },
      {
        "username": "bin",
        "password": "*",
        "last_changed": 18113,
        "minimum": 0,
        "maximum": 99999,
        "warn": 7,
        "inactive": null,
        "expire": null
      },
      ...
    ]

    $ sudo cat /etc/shadow | jc --shadow -p -r
    [
      {
        "username": "root",
        "password": "*",
        "last_changed": "18113",
        "minimum": "0",
        "maximum": "99999",
        "warn": "7",
        "inactive": "",
        "expire": ""
      },
      {
        "username": "daemon",
        "password": "*",
        "last_changed": "18113",
        "minimum": "0",
        "maximum": "99999",
        "warn": "7",
        "inactive": "",
        "expire": ""
      },
      {
        "username": "bin",
        "password": "*",
        "last_changed": "18113",
        "minimum": "0",
        "maximum": "99999",
        "warn": "7",
        "inactive": "",
        "expire": ""
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

    proc_data:   (dictionary) raw structured data to process

Returns:

    List of dictionaries. Structured data with the following schema:

    [
      {
        "username":       string,
        "password":       string,
        "last_changed":   integer,
        "minimum":        integer,
        "maximum":        integer,
        "warn":           integer,
        "inactive":       integer,
        "expire":         integer
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

    List of dictionaries. Raw or processed structured data.

