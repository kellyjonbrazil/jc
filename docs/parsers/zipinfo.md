[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.zipinfo"></a>

# jc.parsers.zipinfo

jc - JSON Convert `zipinfo` command output parser

> Note: No `zipinfo` options are supported.

Usage (cli):

    $ zipinfo <archive> | jc --zipinfo

or

    $ jc zipinfo

Usage (module):

    import jc
    result = jc.parse('zipinfo', zipinfo_command_output)

Schema:

    [
      {
        "archive":              string,
        "size":                 integer,
        "size_unit":            string,
        "number_entries":       integer,
        "number_files":         integer,
        "bytes_uncompressed":   integer,
        "bytes_compressed":     integer,
        "percent_compressed":   float,
        "files": [
          {
            "flags":            string,
            "zipversion":       string,
            "zipunder":         string,
            "filesize":         integer,
            "type":             string,
            "method":           string,
            "date":             string,
            "time":             string,
            "filename":         string
          }
        ]
      }
    ]

Examples:

    $ zipinfo log4j-core-2.16.0.jar | jc --zipinfo -p

    [
      {
        "archive": "log4j-core-2.16.0.jar",
        "size": 1789565,
        "size_unit": "bytes",
        "number_entries": 1218,
        "number_files": 1218,
        "bytes_uncompressed": 3974141,
        "bytes_compressed": 1515455,
        "percent_compressed": 61.9,
        "files": [
          {
            "flags": "-rw-r--r--",
            "zipversion": "2.0",
            "zipunder": "unx",
            "filesize": 19810,
            "type": "bl",
            "method": "defN",
            "date": "21-Dec-12",
            "time": "23:35",
            "filename": "META-INF/MANIFEST.MF"
          },
    ...

<a id="jc.parsers.zipinfo.parse"></a>

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
Compatibility:  linux, darwin

Source: [`jc/parsers/zipinfo.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/zipinfo.py)

Version 1.2 by Matt J (https://github.com/listuser)
