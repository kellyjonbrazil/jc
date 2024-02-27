[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.rsync"></a>

# jc.parsers.rsync

jc - JSON Convert `rsync` command output parser

Supports the `-i` or `--itemize-changes` options with all levels of
verbosity. This parser will process the `STDOUT` output or a log file
generated with the `--log-file` option.

Usage (cli):

    $ rsync -i -a source/ dest | jc --rsync

or

    $ jc rsync -i -a source/ dest

or

    $ cat rsync-backup.log | jc --rsync

Usage (module):

    import jc
    result = jc.parse('rsync', rsync_command_output)

Schema:

    [
      {
        "summary": {
          "date":                             string,
          "time":                             string,
          "process":                          integer,
          "sent":                             integer,
          "received":                         integer,
          "total_size":                       integer,
          "matches":                          integer,
          "hash_hits":                        integer,
          "false_alarms":                     integer,
          "data":                             integer,
          "bytes_sec":                        float,
          "speedup":                          float
        },
        "files": [
          {
            "filename":                       string,
            "date":                           string,
            "time":                           string,
            "process":                        integer,
            "metadata":                       string,
            "update_type":                    string/null,  # [0]
            "file_type":                      string/null,  # [1]
            "checksum_or_value_different":    bool/null,
            "size_different":                 bool/null,
            "modification_time_different":    bool/null,
            "permissions_different":          bool/null,
            "owner_different":                bool/null,
            "group_different":                bool/null,
            "acl_different":                  bool/null,
            "extended_attribute_different":   bool/null,
            "epoch":                          integer,      # [2]
          }
        ]
      }
    ]

    [0] 'file sent', 'file received', 'local change or creation',
        'hard link', 'not updated', 'message'
    [1] 'file', 'directory', 'symlink', 'device', 'special file'
    [2] naive timestamp if time and date fields exist and can be converted.

Examples:

    $ rsync -i -a source/ dest | jc --rsync -p
    [
      {
        "summary": {
          "sent": 1708,
          "received": 8209,
          "bytes_sec": 19834.0,
          "total_size": 235,
          "speedup": 0.02
        },
        "files": [
          {
            "filename": "./",
            "metadata": ".d..t......",
            "update_type": "not updated",
            "file_type": "directory",
            "checksum_or_value_different": false,
            "size_different": false,
            "modification_time_different": true,
            "permissions_different": false,
            "owner_different": false,
            "group_different": false,
            "acl_different": false,
            "extended_attribute_different": false
          },
          ...
        ]
      }
    ]

    $ rsync | jc --rsync -p -r
    [
      {
        "summary": {
          "sent": "1,708",
          "received": "8,209",
          "bytes_sec": "19,834.00",
          "total_size": "235",
          "speedup": "0.02"
        },
        "files": [
          {
            "filename": "./",
            "metadata": ".d..t......",
            "update_type": "not updated",
            "file_type": "directory",
            "checksum_or_value_different": false,
            "size_different": false,
            "modification_time_different": true,
            "permissions_different": false,
            "owner_different": false,
            "group_different": false,
            "acl_different": false,
            "extended_attribute_different": false
          },
          ...
        ]
      }
    ]

<a id="jc.parsers.rsync.parse"></a>

### parse

```python
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[Dict]
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) unprocessed output if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    List of Dictionaries. Raw or processed structured data.

### Parser Information
Compatibility:  linux, darwin, freebsd

Source: [`jc/parsers/rsync.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/rsync.py)

Version 1.2 by Kelly Brazil (kellyjonbrazil@gmail.com)
