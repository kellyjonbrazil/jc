[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.proc_loadavg"></a>

# jc.parsers.proc_loadavg

jc - JSON Convert `/proc/loadavg` file parser

Usage (cli):

    $ cat /proc/loadavg | jc --proc

or

    $ jc /proc/loadavg

or

    $ cat /proc/loadavg | jc --proc-loadavg

Usage (module):

    import jc
    result = jc.parse('proc', proc_loadavg_file)

or

    import jc
    result = jc.parse('proc_loadavg', proc_loadavg_file)

Schema:

All values are integers.

    {
      "load_1m":              float,
      "load_5m":              float,
      "load_15m":             float,
      "running":              integer,
      "available":            integer,
      "last_pid":             integer
    }

Examples:

    $ cat /proc/loadavg | jc --proc -p
    {
      "load_1m": 0.0,
      "load_5m": 0.01,
      "load_15m": 0.03,
      "running": 2,
      "available": 111,
      "last_pid": 2039
    }

    $ cat /proc/loadavg | jc --proc -p -r
    {
      "load_1m": "0.00",
      "load_5m": "0.01",
      "load_15m": "0.03",
      "running": "2",
      "available": "111",
      "last_pid": "2039"
    }

<a id="jc.parsers.proc_loadavg.parse"></a>

### parse

```python
def parse(data: str, raw: bool = False, quiet: bool = False) -> Dict
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) unprocessed output if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    Dictionary. Raw or processed structured data.

### Parser Information
Compatibility:  linux

Source: [`jc/parsers/proc_loadavg.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/proc_loadavg.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
