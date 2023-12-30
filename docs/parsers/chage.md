[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.chage"></a>

# jc.parsers.chage

jc - JSON Convert `chage --list` command output parser

Supports `chage -l <username>` or `chage --list <username>`

Usage (cli):

    $ chage -l johndoe | jc --chage

or

    $ jc chage -l johndoe

Usage (module):

    import jc
    result = jc.parse('chage', chage_command_output)

Schema:

    {
      "password_last_changed":                      string,
      "password_expires":                           string,
      "password_inactive":                          string,
      "account_expires":                            string,
      "min_days_between_password_change":           integer,
      "max_days_between_password_change":           integer,
      "warning_days_before_password_expires":       integer
    }

Examples:

    $ chage --list joeuser | jc --chage -p
    {
      "password_last_changed": "never",
      "password_expires": "never",
      "password_inactive": "never",
      "account_expires": "never",
      "min_days_between_password_change": 0,
      "max_days_between_password_change": 99999,
      "warning_days_before_password_expires": 7
    }

    $ chage --list joeuser | jc --chage -p -r
    {
      "password_last_changed": "never",
      "password_expires": "never",
      "password_inactive": "never",
      "account_expires": "never",
      "min_days_between_password_change": "0",
      "max_days_between_password_change": "99999",
      "warning_days_before_password_expires": "7"
    }

<a id="jc.parsers.chage.parse"></a>

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

Source: [`jc/parsers/chage.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/chage.py)

Version 1.1 by Kelly Brazil (kellyjonbrazil@gmail.com)
