[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.resolve_conf"></a>

# jc.parsers.resolve\_conf

jc - JSON Convert `/etc/resolve.conf` file parser

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
def parse(data: str, raw: bool = False, quiet: bool = False) -> JSONDictType
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

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
