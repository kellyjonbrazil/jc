[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.proc_locks"></a>

# jc.parsers.proc_locks

jc - JSON Convert `/proc/locks` file parser

Usage (cli):

    $ cat /proc/locks | jc --proc

or

    $ jc /proc/locks

or

    $ cat /proc/locks | jc --proc-locks

Usage (module):

    import jc
    result = jc.parse('proc', proc_locks_file)

or

    import jc
    result = jc.parse('proc_locks', proc_locks_file)

Schema:

    [
      {
        "id":                   integer,
        "class":                string,
        "type":                 string,
        "access":               string,
        "pid":                  integer,
        "maj":                  string,
        "min":                  string,
        "inode":                integer,
        "start":                string,
        "end":                  string
      }
    ]

Examples:

    $ cat /proc/locks | jc --proc -p
    [
      {
        "id": 1,
        "class": "POSIX",
        "type": "ADVISORY",
        "access": "WRITE",
        "pid": 877,
        "maj": "00",
        "min": "19",
        "inode": 812,
        "start": "0",
        "end": "EOF"
      },
      {
        "id": 2,
        "class": "FLOCK",
        "type": "ADVISORY",
        "access": "WRITE",
        "pid": 854,
        "maj": "00",
        "min": "19",
        "inode": 805,
        "start": "0",
        "end": "EOF"
      },
      ...
    ]

    $ cat /proc/locks | jc --proc-locks -p -r
    [
      {
        "id": "1",
        "class": "POSIX",
        "type": "ADVISORY",
        "access": "WRITE",
        "pid": "877",
        "maj": "00",
        "min": "19",
        "inode": "812",
        "start": "0",
        "end": "EOF"
      },
      {
        "id": "2",
        "class": "FLOCK",
        "type": "ADVISORY",
        "access": "WRITE",
        "pid": "854",
        "maj": "00",
        "min": "19",
        "inode": "805",
        "start": "0",
        "end": "EOF"
      },
      ...
    ]

<a id="jc.parsers.proc_locks.parse"></a>

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

Source: [`jc/parsers/proc_locks.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/proc_locks.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
