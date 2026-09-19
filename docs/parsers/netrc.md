[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.netrc"></a>

# jc.parsers.netrc

jc - JSON Convert `.netrc` file parser

This parser will work with `.netrc` and `_netrc` files used by `curl`,
`ftp`, and other tools to store login credentials for remote machines.

`machine`/`default` blocks and `macdef` (macro) blocks are both returned
as items in the same list. Since the two block types don't share fields,
unused fields are set to `null`.

Usage (cli):

    $ cat ~/.netrc | jc --netrc

Usage (module):

    import jc
    result = jc.parse('netrc', netrc_file_output)

Schema:

    [
      {
        "machine":                   string,
        "login":                     string,
        "password":                  string,
        "account":                   string,
        "macdef":                    string,
        "definition": [
                                     string
        ]
      }
    ]

Examples:

    $ cat ~/.netrc | jc --netrc -p
    [
      {
        "machine": "mail.example.com",
        "login": "jdoe",
        "password": "secret123",
        "account": null,
        "macdef": null,
        "definition": null
      },
      {
        "machine": "default",
        "login": "anonymous",
        "password": "user@example.com",
        "account": null,
        "macdef": null,
        "definition": null
      },
      {
        "machine": null,
        "login": null,
        "password": null,
        "account": null,
        "macdef": "init",
        "definition": [
          "cd /pub",
          "mget *"
        ]
      }
    ]

<a id="jc.parsers.netrc.parse"></a>

### parse

```python
def parse(data: str,
          raw: bool = False,
          quiet: bool = False) -> List[Dict[str, Any]]
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

Source: [`jc/parsers/netrc.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/netrc.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
