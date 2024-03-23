[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.proc_version"></a>

# jc.parsers.proc_version

jc - JSON Convert `/proc/version` file parser

> Note: This parser will parse `/proc/version` files that follow the
> common format used by most popular linux distributions.

Usage (cli):

    $ cat /proc/version | jc --proc

or

    $ jc /proc/version

or

    $ cat /proc/version | jc --proc-version

Usage (module):

    import jc
    result = jc.parse('proc', proc_version_file)

or

    import jc
    result = jc.parse('proc_version', proc_version_file)

Schema:

    {
      "version":                  string,
      "email":                    string,
      "gcc":                      string,
      "build":                    string,
      "flags":                    string/null,
      "date":                     string
    }

Examples:

    $ cat /proc/version | jc --proc -p
    {
      "version": "5.8.0-63-generic",
      "email": "buildd@lcy01-amd64-028",
      "gcc": "gcc (Ubuntu 10.3.0-1ubuntu1~20.10) 10.3.0, GNU ld (GNU Binutils for Ubuntu) 2.35.1",
      "build": "#71-Ubuntu",
      "flags": "SMP",
      "date": "Tue Jul 13 15:59:12 UTC 2021"
    }

<a id="jc.parsers.proc_version.parse"></a>

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

Source: [`jc/parsers/proc_version.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/proc_version.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
