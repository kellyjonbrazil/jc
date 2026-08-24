[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.net_localgroup"></a>

# jc.parsers.net_localgroup

jc - JSON Convert `net localgroup` command output parser

Usage (cli):

    $ net localgroup | jc --net-localgroup
    $ net localgroup /domain | jc --net-localgroup
    $ net localgroup Administrators | jc --net-localgroup
    $ net localgroup Administrators /domain | jc --net-localgroup

Usage (module):

    import jc
    result = jc.parse('net_localgroup', net_localgroup_command_output)

Schema:

    {
        "account_origin":     string,
        "domain":             string,
        "comment":            string,
        "groups": [
            {
                "name":       string
                "members": [
                              string
                ]
            }
        ],
    }

Examples:

    $ net localgroup | jc --net-localgroup -p
    {
        "account_origin": null,
        "comment": null,
        "domain": null,
        "groups": [
            {
                "name": "Administrators",
                "members": [
                    "Administrator",
                    "Operator",
                    "ansible",
                    "user1"
                ]
            }
        ]
    }

<a id="jc.parsers.net_localgroup.parse"></a>

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

    Parsed dictionary. The raw and processed data structures are the same.

### Parser Information
Compatibility:  win32

Source: [`jc/parsers/net_localgroup.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/net_localgroup.py)

Version 1.0 by joehacksalot (joehacksalot@gmail.com)
