[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.du"></a>

# jc.parsers.du

jc - JSON Convert `du` command output parser

Usage (cli):

    $ du | jc --du

or

    $ jc du

Usage (module):

    import jc
    result = jc.parse('du', du_command_output)

Schema:

    [
      {
        "size":     integer,
        "name":     string
      }
    ]

Examples:

    $ du /usr | jc --du -p
    [
      {
        "size": 104608,
        "name": "/usr/bin"
      },
      {
        "size": 56,
        "name": "/usr/standalone/firmware/iBridge1_1Customer.bundle/..."
      },
      {
        "size": 0,
        "name": "/usr/standalone/firmware/iBridge1_1Customer.bundle/..."
      },
      {
        "size": 0,
        "name": "/usr/standalone/firmware/iBridge1_1Customer.bundle/..."
      },
      {
        "size": 0,
        "name": "/usr/standalone/firmware/iBridge1_1Customer.bundle/..."
      },
      {
        "size": 1008,
        "name": "/usr/standalone/firmware/iBridge1_1Customer.bundle/..."
      },
      ...
    ]

    $ du /usr | jc --du -p -r
    [
      {
        "size": "104608",
        "name": "/usr/bin"
      },
      {
        "size": "56",
        "name": "/usr/standalone/firmware/iBridge1_1Customer.bundle/..."
      },
      {
        "size": "0",
        "name": "/usr/standalone/firmware/iBridge1_1Customer.bundle/..."
      },
      {
        "size": "0",
        "name": "/usr/standalone/firmware/iBridge1_1Customer.bundle/..."
      },
      {
        "size": "0",
        "name": "/usr/standalone/firmware/iBridge1_1Customer.bundle/..."
      },
      {
        "size": "1008",
        "name": "/usr/standalone/firmware/iBridge1_1Customer.bundle/..."
      },
      ...
    ]

<a id="jc.parsers.du.parse"></a>

### parse

```python
def parse(data, raw=False, quiet=False)
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) unprocessed output if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    List of Dictionaries. Raw or processed structured data.

### Parser Information
Compatibility:  linux, darwin, aix, freebsd

Version 1.6 by Kelly Brazil (kellyjonbrazil@gmail.com)
