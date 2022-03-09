[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.pidstat"></a>

# jc.parsers.pidstat

jc - JSON Convert `pidstat` command output parser

Must use the `-h` option in `pidstat`. All other `pidstat` options are
supported in combination with `-h`.

Usage (cli):

    $ pidstat -h | jc --pidstat

    or

    $ jc pidstat -h

Usage (module):

    import jc
    result = jc.parse('pidstat', pidstat_command_output)

    or

    import jc.parsers.pidstat
    result = jc.parsers.pidstat.parse(pidstat_command_output)

Schema:

    [
      {
        "time":             integer,
        "uid":              integer,
        "pid":              integer,
        "percent_usr":      float,
        "percent_system":   float,
        "percent_guest":    float,
        "percent_cpu":      float,
        "cpu":              integer,
        "minflt_s":         float,
        "majflt_s":         float,
        "vsz":              integer,
        "rss":              integer,
        "percent_mem":      float,
        "stksize":          integer,
        "stkref":           integer,
        "kb_rd_s":          float,
        "kb_wr_s":          float,
        "kb_ccwr_s":        float,
        "cswch_s":          float,
        "nvcswch_s":        float,
        "command":          string
      }
    ]

Examples:

    $ pidstat -hl | jc --pidstat -p
    [
      {
        "time": 1646859134,
        "uid": 0,
        "pid": 1,
        "percent_usr": 0.0,
        "percent_system": 0.03,
        "percent_guest": 0.0,
        "percent_cpu": 0.03,
        "cpu": 0,
        "command": "/usr/lib/systemd/systemd --switched-root --system --deserialize 22"
      },
      {
        "time": 1646859134,
        "uid": 0,
        "pid": 6,
        "percent_usr": 0.0,
        "percent_system": 0.0,
        "percent_guest": 0.0,
        "percent_cpu": 0.0,
        "cpu": 0,
        "command": "ksoftirqd/0"
      },
      {
        "time": 1646859134,
        "uid": 0,
        "pid": 2263,
        "percent_usr": 0.0,
        "percent_system": 0.0,
        "percent_guest": 0.0,
        "percent_cpu": 0.0,
        "cpu": 0,
        "command": "kworker/0:0"
      }
    ]

    $ pidstat -hl | jc --pidstat -p -r
    [
      {
        "time": "1646859134",
        "uid": "0",
        "pid": "1",
        "percent_usr": "0.00",
        "percent_system": "0.03",
        "percent_guest": "0.00",
        "percent_cpu": "0.03",
        "cpu": "0",
        "command": "/usr/lib/systemd/systemd --switched-root --system --deserialize 22"
      },
      {
        "time": "1646859134",
        "uid": "0",
        "pid": "6",
        "percent_usr": "0.00",
        "percent_system": "0.00",
        "percent_guest": "0.00",
        "percent_cpu": "0.00",
        "cpu": "0",
        "command": "ksoftirqd/0"
      },
      {
        "time": "1646859134",
        "uid": "0",
        "pid": "2263",
        "percent_usr": "0.00",
        "percent_system": "0.00",
        "percent_guest": "0.00",
        "percent_cpu": "0.00",
        "cpu": "0",
        "command": "kworker/0:0"
      }
    ]

<a id="jc.parsers.pidstat.parse"></a>

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

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
