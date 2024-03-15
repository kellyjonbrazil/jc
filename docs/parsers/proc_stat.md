[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.proc_stat"></a>

# jc.parsers.proc_stat

jc - JSON Convert `/proc/stat` file parser

Usage (cli):

    $ cat /proc/stat | jc --proc

or

    $ jc /proc/stat

or

    $ cat /proc/stat | jc --proc-stat

Usage (module):

    import jc
    result = jc.parse('proc', proc_stat_file)

or

    import jc
    result = jc.parse('proc_stat', proc_stat_file)

Schema:

    {
      "cpu": {
        "user":                         integer,
        "nice":                         integer,
        "system":                       integer,
        "idle":                         integer,
        "iowait":                       integer,
        "irq":                          integer,
        "softirq":                      integer,
        "steal":                        integer,
        "guest":                        integer,
        "guest_nice":                   integer
      },
      "cpu<number>": {
        "user":                         integer,
        "nice":                         integer,
        "system":                       integer,
        "idle":                         integer,
        "iowait":                       integer,
        "irq":                          integer,
        "softirq":                      integer,
        "steal":                        integer,
        "guest":                        integer,
        "guest_nice":                   integer
      },
      "interrupts": [
                                        integer
      ],
      "context_switches":               integer,
      "boot_time":                      integer,
      "processes":                      integer,
      "processes_running":              integer,
      "processes_blocked":              integer,
      "softirq": [
                                        integer
      ]
    }

Examples:

    $ cat /proc/stat | jc --proc -p
    {
      "cpu": {
        "user": 6002,
        "nice": 152,
        "system": 8398,
        "idle": 3444436,
        "iowait": 448,
        "irq": 0,
        "softirq": 1174,
        "steal": 0,
        "guest": 0,
        "guest_nice": 0
      },
      "cpu0": {
        "user": 2784,
        "nice": 137,
        "system": 4367,
        "idle": 1732802,
        "iowait": 225,
        "irq": 0,
        "softirq": 221,
        "steal": 0,
        "guest": 0,
        "guest_nice": 0
      },
      "cpu1": {
        "user": 3218,
        "nice": 15,
        "system": 4031,
        "idle": 1711634,
        "iowait": 223,
        "irq": 0,
        "softirq": 953,
        "steal": 0,
        "guest": 0,
        "guest_nice": 0
      },
      "interrupts": [
        2496709,
        18,
        73,
        0,
        0,
        ...
      ],
      "context_switches": 4622716,
      "boot_time": 1662154781,
      "processes": 9831,
      "processes_running": 1,
      "processes_blocked": 0,
      "softirq": [
        3478985,
        35230,
        1252057,
        3467,
        128583,
        51014,
        0,
        171199,
        1241297,
        0,
        596138
      ]
    }

<a id="jc.parsers.proc_stat.parse"></a>

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

Source: [`jc/parsers/proc_stat.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/proc_stat.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
