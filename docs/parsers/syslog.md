[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.syslog"></a>

# jc.parsers.syslog

jc - JSON Convert Syslog RFC 5424 string parser

The `timestamp_epoch` calculated timestamp field is naive. (i.e. based on
the local time of the system the parser is run on)

The `timestamp_epoch_utc` calculated timestamp field is timezone-aware and
is only available if the timezone field is UTC.

Usage (cli):

    $ syslogstring | jc --syslog

    or

    $ jc syslog-5424

Usage (module):

    import jc
    result = jc.parse('syslog', syslog_command_output)

Schema:
Blank values converted to `null`/`None`

    [
      {
        "priority":                   integer,
        "version":                    integer,
        "timestamp":                  string,
        "timestamp_epoch":            integer,  # [0]
        "timestamp_epoch_utc":        integer,  # [1]
        "hostname":                   string,
        "appname":                    string,
        "proc_id":                    integer,
        "msg_id":                     string,
        "structured_data": [
          {
            "identity":               string,
            "values": {
              "<key>":                string
            }
          }
        ],
        "message":                    string
      }
    ]

    [0] naive timestamp if "timestamp" field is parsable, else null
    [1] timezone aware timestamp availabe for UTC, else null

Examples:

    $ cat syslog.txt| jc --syslog -p
    [
      {
        "priority": 35,
        "version": 1,
        "timestamp": "2003-10-11T22:14:15.003Z",
        "hostname": "mymachine.example.com",
        "appname": "evntslog",
        "proc_id": null,
        "msg_id": "ID47",
        "structured_data": [
          {
            "identity": "exampleSDID@32473",
            "values": {
              "iut": "3",
              "eventSource": "Application",
              "eventID": "1011"
            }
          },
          {
            "identity": "examplePriority@32473",
            "values": {
              "class": "high"
            }
          }
        ],
        "message": "unauthorized attempt",
        "timestamp_epoch": 1065935655,
        "timestamp_epoch_utc": 1065910455
      }
    ]

    $ cat syslog.txt| jc --syslog -p -r
    [
      {
        "priority": "35",
        "version": "1",
        "timestamp": "2003-10-11T22:14:15.003Z",
        "hostname": "mymachine.example.com",
        "appname": "evntslog",
        "proc_id": null,
        "msg_id": "ID47",
        "structured_data": "[exampleSDID@32473 iut=\"3\" eventSource=\...",
        "message": "unauthorized attempt"
      }
    ]

<a id="jc.parsers.syslog.parse"></a>

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
Compatibility:  linux, darwin, cygwin, win32, aix, freebsd

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
