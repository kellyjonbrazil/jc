[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.cksum"></a>

# jc.parsers.cksum

jc - JSON Convert `cksum` command output parser

This parser works with the following checksum calculation utilities:
- `sum`
- `cksum`

Usage (cli):

    $ cksum file.txt | jc --cksum

or

    $ jc cksum file.txt

Usage (module):

    import jc
    result = jc.parse('cksum', cksum_command_output)

Schema:

    [
      {
        "filename":     string,
        "checksum":     integer,
        "blocks":       integer
      }
    ]

Examples:

    $ cksum * | jc --cksum -p
    [
      {
        "filename": "__init__.py",
        "checksum": 4294967295,
        "blocks": 0
      },
      {
        "filename": "airport.py",
        "checksum": 2208551092,
        "blocks": 3745
      },
      {
        "filename": "airport_s.py",
        "checksum": 1113817598,
        "blocks": 4572
      },
      ...
    ]

<a id="jc.parsers.cksum.parse"></a>

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
Compatibility:  linux, darwin, cygwin, aix, freebsd

Source: [`jc/parsers/cksum.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/cksum.py)

Version 1.4 by Kelly Brazil (kellyjonbrazil@gmail.com)
