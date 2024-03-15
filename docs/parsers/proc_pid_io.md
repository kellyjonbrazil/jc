[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.proc_pid_io"></a>

# jc.parsers.proc_pid_io

jc - JSON Convert `/proc/<pid>/io` file parser

Usage (cli):

    $ cat /proc/1/io | jc --proc

or

    $ jc /proc/1/io

or

    $ cat /proc/1/io | jc --proc-pid-io

Usage (module):

    import jc
    result = jc.parse('proc', proc_pid_io_file)

or

    import jc
    result = jc.parse('proc_pid_io', proc_pid_io_file)

Schema:

All values are integers.

    {
      <keyName>             integer
    }

Examples:

    $ cat /proc/1/io | jc --proc -p
    {
      "rchar": 4699288382,
      "wchar": 2931802997,
      "syscr": 661897,
      "syscw": 890910,
      "read_bytes": 168468480,
      "write_bytes": 27357184,
      "cancelled_write_bytes": 16883712
    }

<a id="jc.parsers.proc_pid_io.parse"></a>

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

Source: [`jc/parsers/proc_pid_io.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/proc_pid_io.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
