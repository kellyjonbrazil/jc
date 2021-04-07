
# jc.parsers.dir
jc - JSON CLI output utility `dir` command output parser

Options supported:
- `/T timefield`
- `/O sortorder`
- `/C, /-C`
- `/S`

The `epoch` calculated timestamp field is naive (i.e. based on the local time of the system the parser is run on)

Usage (cli):

    C:> dir | jc --dir

    or

    C:> jc dir

Usage (module):

    import jc.parsers.dir
    result = jc.parsers.dir.parse(dir_command_output)

Compatibility:

    'win32'

Examples:

    C:> dir | jc --dir -p
    [
      {
        "date": "03/24/2021",
        "time": "03:15 PM",
        "dir": true,
        "size": null,
        "filename": ".",
        "parent": "C:\Program Files\Internet Explorer",
        "epoch": 1616624100
      },
      {
        "date": "03/24/2021",
        "time": "03:15 PM",
        "dir": true,
        "size": null,
        "filename": "..",
        "parent": "C:\Program Files\Internet Explorer",
        "epoch": 1616624100
      },
      {
        "date": "12/07/2019",
        "time": "02:49 AM",
        "dir": true,
        "size": null,
        "filename": "en-US",
        "parent": "C:\Program Files\Internet Explorer",
        "epoch": 1575715740
      },
      {
        "date": "12/07/2019",
        "time": "02:09 AM",
        "dir": false,
        "size": 54784,
        "filename": "ExtExport.exe",
        "parent": "C:\Program Files\Internet Explorer",
        "epoch": 1575713340
      },
      ...
    ]

    C:> dir | jc --dir -p -r
    [
      {
        "date": "03/24/2021",
        "time": "03:15 PM",
        "dir": true,
        "size": null,
        "filename": ".",
        "parent": "C:\Program Files\Internet Explorer"
      },
      {
        "date": "03/24/2021",
        "time": "03:15 PM",
        "dir": true,
        "size": null,
        "filename": "..",
        "parent": "C:\Program Files\Internet Explorer"
      },
      {
        "date": "12/07/2019",
        "time": "02:49 AM",
        "dir": true,
        "size": null,
        "filename": "en-US",
        "parent": "C:\Program Files\Internet Explorer"
      },
      {
        "date": "12/07/2019",
        "time": "02:09 AM",
        "dir": false,
        "size": "54,784",
        "filename": "ExtExport.exe",
        "parent": "C:\Program Files\Internet Explorer"
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

    proc_data:   (Dictionary of Lists) raw structured data to process

Returns:

    List of Dictionaries. Structured data with the following schema:

    [
      {
        "date":         string,
        "time":         string,
        "epoch":        integer,    # naive timestamp
        "dir":          boolean,
        "size":         integer,
        "filename:      string,
        "parent":       string
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

