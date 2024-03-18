[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.proc_pid_statm"></a>

# jc.parsers.proc_pid_statm

jc - JSON Convert `/proc/<pid>/statm` file parser

Usage (cli):

    $ cat /proc/1/statm | jc --proc

or

    $ jc /proc/1/statm

or

    $ cat /proc/1/statm | jc --proc-pid-statm

Usage (module):

    import jc
    result = jc.parse('proc', proc_pid_statm_file)

or

    import jc
    result = jc.parse('proc_pid_statm', proc_pid_statm_file)

Schema:

    {
      "size":                   integer,
      "resident":               integer,
      "shared":                 integer,
      "text":                   integer,
      "lib":                    integer,
      "data":                   integer,
      "dt":                     integer
    }

Examples:

    $ cat /proc/1/statm | jc --proc -p
    {
      "size": 42496,
      "resident": 3313,
      "shared": 2169,
      "text": 202,
      "lib": 0,
      "data": 5180,
      "dt": 0
    }

<a id="jc.parsers.proc_pid_statm.parse"></a>

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

Source: [`jc/parsers/proc_pid_statm.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/proc_pid_statm.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
