[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.toml"></a>

# jc.parsers.toml

jc - JSON Convert TOML file parser

Usage (cli):

    $ cat file.toml | jc --toml

Usage (module):

    import jc
    result = jc.parse('toml', toml_file_output)

Schema:

TOML Document converted to a Dictionary.
See https://toml.io/en/ for details.

    {
      "key1":     string/int/float/boolean/null/array/object,
      "key2":     string/int/float/boolean/null/array/object
    }

Examples:

    $ cat file.toml
    title = "TOML Example"

    [owner]
    name = "Tom Preston-Werner"
    dob = 1979-05-27T07:32:00-08:00

    [database]
    enabled = true
    ports = [ 8000, 8001, 8002 ]

    $ cat file.toml | jc --toml -p
    {
      "title": "TOML Example",
      "owner": {
        "name": "Tom Preston-Werner",
        "dob": 296667120,
        "dob_iso": "1979-05-27T07:32:00-08:00"
      },
      "database": {
        "enabled": true,
        "ports": [
          8000,
          8001,
          8002
        ]
      }
    }

<a id="jc.parsers.toml.parse"></a>

### parse

```python
def parse(data: str, raw: bool = False, quiet: bool = False) -> Dict[str, Any]
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) unprocessed output if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    Dictionary. Raw or processed structured data.

### Parser Information
Compatibility:  linux, darwin, cygwin, win32, aix, freebsd

Source: [`jc/parsers/toml.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/toml.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
