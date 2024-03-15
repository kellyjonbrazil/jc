[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.ver"></a>

# jc.parsers.ver

jc - JSON Convert Version string output parser

Best-effort attempt to parse various styles of version numbers. This parser
is based off of the version parser included in the CPython distutils
library.

If the version string conforms to some de facto-standard versioning rules
followed by many developers a `strict` key will be present in the output
with a value of `true` along with the named parsed components.

All other version strings will have a `strict` value of `false` and a
`components` key will contain a list of detected parts of the version
string.

See Also: `semver` parser.

Usage (cli):

    $ echo 1.2a1 | jc --ver

Usage (module):

    import jc
    result = jc.parse('ver', version_string_output)

Schema:

    {
      "major":                  integer,
      "minor":                  integer,
      "patch":                  integer,
      "prerelease":             string,
      "prerelease_num":         integer,
      "components": [
                                integer/string
      ],
      "strict":                 boolean
    }

Examples:

    $ echo 1.2a1 | jc --ver -p
    {
      "major": 1,
      "minor": 2,
      "patch": 0,
      "prerelease": "a",
      "prerelease_num": 1,
      "strict": true
    }

    $ echo 1.2a1 | jc --ver -p -r
    {
      "major": "1",
      "minor": "2",
      "patch": "0",
      "prerelease": "a",
      "prerelease_num": "1",
      "strict": true
    }

    $ echo 1.2beta3 | jc --ver -p
    {
      "components": [
        1,
        2,
        "beta",
        3
      ],
      "strict": false
    }

    $ echo 1.2beta3 | jc --ver -p -r
    {
      "components": [
        "1",
        "2",
        "beta",
        "3"
      ],
      "strict": false
    }

<a id="jc.parsers.ver.parse"></a>

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

    List of Dictionaries. Raw or processed structured data.

### Parser Information
Compatibility:  linux, darwin, cygwin, win32, aix, freebsd

Source: [`jc/parsers/ver.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/ver.py)

This parser can be used with the `--slurp` command-line option.

Version 1.2 by Kelly Brazil (kellyjonbrazil@gmail.com)
