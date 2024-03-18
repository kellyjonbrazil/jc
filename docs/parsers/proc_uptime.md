[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.proc_uptime"></a>

# jc.parsers.proc_uptime

jc - JSON Convert `/proc/uptime` file parser

Usage (cli):

    $ cat /proc/uptime | jc --proc

or

    $ jc /proc/uptime

or

    $ cat /proc/uptime | jc --proc-uptime

Usage (module):

    import jc
    result = jc.parse('proc', proc_uptime_file)

or

    import jc
    result = jc.parse('proc_uptime', proc_uptime_file)

Schema:

    {
      "up_time":                    float,
      "idle_time":                  float
    }

Examples:

    $ cat /proc/uptime | jc --proc -p
    {
      "up_time": 46901.13,
      "idle_time": 46856.66
    }

<a id="jc.parsers.proc_uptime.parse"></a>

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

Source: [`jc/parsers/proc_uptime.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/proc_uptime.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
