[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.proc_diskstats"></a>

# jc.parsers.proc_diskstats

jc - JSON Convert `/proc/diskstats` file parser

Usage (cli):

    $ cat /proc/diskstats | jc --proc

or

    $ jc /proc/diskstats

or

    $ cat /proc/diskstats | jc --proc-diskstats

Usage (module):

    import jc
    result = jc.parse('proc', proc_diskstats_file)

or

    import jc
    result = jc.parse('proc_diskstats', proc_diskstats_file)

Schema:

    [
      {
        "maj":                                          integer,
        "min":                                          integer,
        "device":                                       string,
        "reads_completed":                              integer,
        "reads_merged":                                 integer,
        "sectors_read":                                 integer,
        "read_time_ms":                                 integer,
        "writes_completed":                             integer,
        "writes_merged":                                integer,
        "sectors_written":                              integer,
        "write_time_ms":                                integer,
        "io_in_progress":                               integer,
        "io_time_ms":                                   integer,
        "weighted_io_time_ms":                          integer,
        "discards_completed_successfully":              integer,
        "discards_merged":                              integer,
        "sectors_discarded":                            integer,
        "discarding_time_ms":                           integer,
        "flush_requests_completed_successfully":        integer,
        "flushing_time_ms":                             integer
      }
    ]

Examples:

    $ cat /proc/diskstats | jc --proc -p
    [
      {
        "maj": 7,
        "min": 0,
        "device": "loop0",
        "reads_completed": 48,
        "reads_merged": 0,
        "sectors_read": 718,
        "read_time_ms": 19,
        "writes_completed": 0,
        "writes_merged": 0,
        "sectors_written": 0,
        "write_time_ms": 0,
        "io_in_progress": 0,
        "io_time_ms": 36,
        "weighted_io_time_ms": 19,
        "discards_completed_successfully": 0,
        "discards_merged": 0,
        "sectors_discarded": 0,
        "discarding_time_ms": 0,
        "flush_requests_completed_successfully": 0,
        "flushing_time_ms": 0
      },
      {
        "maj": 7,
        "min": 1,
        "device": "loop1",
        "reads_completed": 41,
        "reads_merged": 0,
        "sectors_read": 688,
        "read_time_ms": 17,
        "writes_completed": 0,
        "writes_merged": 0,
        "sectors_written": 0,
        "write_time_ms": 0,
        "io_in_progress": 0,
        "io_time_ms": 28,
        "weighted_io_time_ms": 17,
        "discards_completed_successfully": 0,
        "discards_merged": 0,
        "sectors_discarded": 0,
        "discarding_time_ms": 0,
        "flush_requests_completed_successfully": 0,
        "flushing_time_ms": 0
      },
      ...
    ]

    $ cat /proc/diskstats | jc --proc_diskstats -p -r
    [
      {
        "maj": "7",
        "min": "0",
        "device": "loop0",
        "reads_completed": "48",
        "reads_merged": "0",
        "sectors_read": "718",
        "read_time_ms": "19",
        "writes_completed": "0",
        "writes_merged": "0",
        "sectors_written": "0",
        "write_time_ms": "0",
        "io_in_progress": "0",
        "io_time_ms": "36",
        "weighted_io_time_ms": "19",
        "discards_completed_successfully": "0",
        "discards_merged": "0",
        "sectors_discarded": "0",
        "discarding_time_ms": "0",
        "flush_requests_completed_successfully": "0",
        "flushing_time_ms": "0"
      },
      {
        "maj": "7",
        "min": "1",
        "device": "loop1",
        "reads_completed": "41",
        "reads_merged": "0",
        "sectors_read": "688",
        "read_time_ms": "17",
        "writes_completed": "0",
        "writes_merged": "0",
        "sectors_written": "0",
        "write_time_ms": "0",
        "io_in_progress": "0",
        "io_time_ms": "28",
        "weighted_io_time_ms": "17",
        "discards_completed_successfully": "0",
        "discards_merged": "0",
        "sectors_discarded": "0",
        "discarding_time_ms": "0",
        "flush_requests_completed_successfully": "0",
        "flushing_time_ms": "0"
      },
      {
        "maj": "7",
        "min": "2",
        "device": "loop2",
        "reads_completed": "119",
        "reads_merged": "0",
        "sectors_read": "2956",
        "read_time_ms": "18",
        "writes_completed": "0",
        "writes_merged": "0",
        "sectors_written": "0",
        "write_time_ms": "0",
        "io_in_progress": "0",
        "io_time_ms": "56",
        "weighted_io_time_ms": "18",
        "discards_completed_successfully": "0",
        "discards_merged": "0",
        "sectors_discarded": "0",
        "discarding_time_ms": "0",
        "flush_requests_completed_successfully": "0",
        "flushing_time_ms": "0"
      },
      ...
    ]

<a id="jc.parsers.proc_diskstats.parse"></a>

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
Compatibility:  linux

Source: [`jc/parsers/proc_diskstats.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/proc_diskstats.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
