[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.dir"></a>

# jc.parsers.dir

jc - JSON Convert `dir` command output parser

Options supported:
- `/T timefield`
- `/O sortorder`
- `/C, /-C`
- `/S`

The "Magic" syntax is not supported since the `dir` command is a shell
builtin.

The `epoch` calculated timestamp field is naive. (i.e. based on the local
time of the system the parser is run on)

Usage (cli):

    C:\> dir | jc --dir

Usage (module):

    import jc
    result = jc.parse('dir', dir_command_output)

Schema:

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

Examples:

    C:\> dir | jc --dir -p
    [
      {
        "date": "03/24/2021",
        "time": "03:15 PM",
        "dir": true,
        "size": null,
        "filename": ".",
        "parent": "C:\\Program Files\\Internet Explorer",
        "epoch": 1616624100
      },
      {
        "date": "03/24/2021",
        "time": "03:15 PM",
        "dir": true,
        "size": null,
        "filename": "..",
        "parent": "C:\\Program Files\\Internet Explorer",
        "epoch": 1616624100
      },
      {
        "date": "12/07/2019",
        "time": "02:49 AM",
        "dir": true,
        "size": null,
        "filename": "en-US",
        "parent": "C:\\Program Files\\Internet Explorer",
        "epoch": 1575715740
      },
      {
        "date": "12/07/2019",
        "time": "02:09 AM",
        "dir": false,
        "size": 54784,
        "filename": "ExtExport.exe",
        "parent": "C:\\Program Files\\Internet Explorer",
        "epoch": 1575713340
      },
      ...
    ]

    C:\> dir | jc --dir -p -r
    [
      {
        "date": "03/24/2021",
        "time": "03:15 PM",
        "dir": true,
        "size": null,
        "filename": ".",
        "parent": "C:\\Program Files\\Internet Explorer"
      },
      {
        "date": "03/24/2021",
        "time": "03:15 PM",
        "dir": true,
        "size": null,
        "filename": "..",
        "parent": "C:\\Program Files\\Internet Explorer"
      },
      {
        "date": "12/07/2019",
        "time": "02:49 AM",
        "dir": true,
        "size": null,
        "filename": "en-US",
        "parent": "C:\\Program Files\\Internet Explorer"
      },
      {
        "date": "12/07/2019",
        "time": "02:09 AM",
        "dir": false,
        "size": "54,784",
        "filename": "ExtExport.exe",
        "parent": "C:\\Program Files\\Internet Explorer"
      },
      ...
    ]

<a id="jc.parsers.dir.parse"></a>

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
Compatibility:  win32

Source: [`jc/parsers/dir.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/dir.py)

Version 1.6 by Rasheed Elsaleh (rasheed@rebelliondefense.com)
