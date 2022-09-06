[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.proc"></a>

# jc.parsers.proc

jc - JSON Convert Proc file output parser

<<Short procfile description and caveats>>

Usage (cli):

    $ cat /proc/<file> | jc --procfile

Usage (module):

    import jc
    result = jc.parse('procfile', proc_file)

Schema:

    [
      {
        "procfile":     string,
        "bar":     boolean,
        "baz":     integer
      }
    ]

Examples:

    $ procfile | jc --procfile -p
    []

    $ procfile | jc --procfile -p -r
    []

<a id="jc.parsers.proc.parse"></a>

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
