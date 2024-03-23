[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.resolve_conf"></a>

# jc.parsers.resolve_conf

jc - JSON Convert `/etc/resolve.conf` file parser

This parser may be more forgiving than the system parser. For example, if
multiple `search` lists are defined, this parser will append all entries to
the `search` field, while the system parser may only use the list from the
last defined instance.

Usage (cli):

    $ cat /etc/resolve.conf | jc --resolve-conf

Usage (module):

    import jc
    result = jc.parse('resolve_conf', resolve_conf_output)

Schema:

    {
      "domain":             string,
      "search": [
                            string
      ],
      "nameservers": [
                            string
      ],
      "options": [
                            string
      ],
      "sortlist": [
                            string
      ]
    }


Examples:

    $ cat /etc/resolve.conf | jc --resolve-conf -p
    {
      "search": [
        "eng.myprime.com",
        "dev.eng.myprime.com",
        "labs.myprime.com",
        "qa.myprime.com"
      ],
      "nameservers": [
        "10.136.17.15"
      ],
      "options": [
        "rotate",
        "ndots:1"
      ]
    }

<a id="jc.parsers.resolve_conf.parse"></a>

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

Source: [`jc/parsers/resolve_conf.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/resolve_conf.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
