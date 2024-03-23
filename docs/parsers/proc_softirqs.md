[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.proc_softirqs"></a>

# jc.parsers.proc_softirqs

jc - JSON Convert `/proc/softirqs` file parser

Usage (cli):

    $ cat /proc/softirqs | jc --proc

or

    $ jc /proc/softirqs

or

    $ cat /proc/softirqs | jc --proc-softirqs

Usage (module):

    import jc
    result = jc.parse('proc', proc_softirqs_file)

or

    import jc
    result = jc.parse('proc_softirqs', proc_softirqs_file)

Schema:

    [
      {
        "counter":                    string,
        "CPU<number>":                integer,
      }
    ]

Examples:

    $ cat /proc/softirqs | jc --proc -p
    [
      {
        "counter": "HI",
        "CPU0": 1,
        "CPU1": 34056,
        "CPU2": 0,
        "CPU3": 0,
        "CPU4": 0
      },
      {
        "counter": "TIMER",
        "CPU0": 322970,
        "CPU1": 888166,
        "CPU2": 0,
        "CPU3": 0,
        "CPU4": 0
      },
      ...
    ]

<a id="jc.parsers.proc_softirqs.parse"></a>

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

Source: [`jc/parsers/proc_softirqs.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/proc_softirqs.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
