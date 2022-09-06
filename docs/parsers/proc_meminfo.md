[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.proc_meminfo"></a>

# jc.parsers.proc\_meminfo

jc - JSON Convert `/proc/meminfo` file parser

Usage (cli):

    $ cat /proc/meminfo | jc --proc

Usage (module):

    import jc
    result = jc.parse('proc_meminfo', proc_meminfo_file)

Schema:

    [
      {
        "foo":     string,
        "bar":     boolean,
        "baz":     integer
      }
    ]

Examples:

    $ foo | jc --foo -p
    []

    $ foo | jc --foo -p -r
    []

<a id="jc.parsers.proc_meminfo.parse"></a>

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

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
