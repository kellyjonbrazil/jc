[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.semver"></a>

# jc.parsers.semver

jc - JSON Convert Semantic Version string parser

This parser conforms to the specification at https://semver.org/

See Also: `ver` parser.

Usage (cli):

    $ echo 1.2.3-rc.1+44837 | jc --semver

Usage (module):

    import jc
    result = jc.parse('semver', semver_string)

Schema:

Strings that do not strictly conform to the specification will return an
empty object.

    {
      "major":                  integer,
      "minor":                  integer,
      "patch":                  integer,
      "prerelease":             string/null,
      "build":                  string/null
    }

Examples:

    $ echo 1.2.3-rc.1+44837 | jc --semver -p
    {
      "major": 1,
      "minor": 2,
      "patch": 3,
      "prerelease": "rc.1",
      "build": "44837"
    }

    $ echo 1.2.3-rc.1+44837 | jc --semver -p -r
    {
      "major": "1",
      "minor": "2",
      "patch": "3",
      "prerelease": "rc.1",
      "build": "44837"
    }

<a id="jc.parsers.semver.parse"></a>

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

Source: [`jc/parsers/semver.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/semver.py)

This parser can be used with the `--slurp` command-line option.

Version 1.1 by Kelly Brazil (kellyjonbrazil@gmail.com)
