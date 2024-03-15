[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.email_address"></a>

# jc.parsers.email_address

jc - JSON Convert Email Address string parser

Usage (cli):

    $ echo "username@example.com" | jc --email-address

Usage (module):

    import jc
    result = jc.parse('email_address', email_address_string)

Schema:

    {
      "username":             string,
      "domain":               string,
      "local":                string,
      "local_plus_suffix":    string or null
    }

Examples:

    $ echo 'joe.user@gmail.com' | jc --email-address -p
    {
      "username": "joe.user",
      "domain": "gmail.com",
      "local": "joe.user",
      "local_plus_suffix": null
    }

    $ echo 'joe.user+spam@gmail.com' | jc --email-address -p
    {
      "username": "joe.user",
      "domain": "gmail.com",
      "local": "joe.user+spam",
      "local_plus_suffix": "spam"
    }

<a id="jc.parsers.email_address.parse"></a>

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
Compatibility:  linux, darwin, cygwin, win32, aix, freebsd

Source: [`jc/parsers/email_address.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/email_address.py)

This parser can be used with the `--slurp` command-line option.

Version 1.1 by Kelly Brazil (kellyjonbrazil@gmail.com)
