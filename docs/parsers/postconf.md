[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.postconf"></a>

# jc.parsers.postconf

jc - JSON Convert `postconf -M` command output parser

Usage (cli):

    $ postconf -M | jc --postconf

or

    $ jc postconf -M

Usage (module):

    import jc
    result = jc.parse('postconf', postconf_command_output)

Schema:

    [
      {
        "service_name":                     string,
        "service_type":                     string,
        "private":                          boolean/null,  # [0]
        "unprivileged":                     boolean/null,  # [0]
        "chroot":                           boolean/null,  # [0]
        "wake_up_time":                     integer/null,  # [0]
        "no_wake_up_before_first_use":      boolean/null,  # [1]
        "process_limit":                    integer/null,  # [0]
        "command":                          string
      }
    ]

    [0] '-' converted to null/None
    [1] null/None if `wake_up_time` is null/None

Examples:

    $ postconf -M | jc --postconf -p
    [
      {
        "service_name": "smtp",
        "service_type": "inet",
        "private": false,
        "unprivileged": null,
        "chroot": true,
        "wake_up_time": null,
        "process_limit": null,
        "command": "smtpd",
        "no_wake_up_before_first_use": null
      },
      {
        "service_name": "pickup",
        "service_type": "unix",
        "private": false,
        "unprivileged": null,
        "chroot": true,
        "wake_up_time": 60,
        "process_limit": 1,
        "command": "pickup",
        "no_wake_up_before_first_use": false
      }
    ]

    $ postconf -M | jc --postconf -p -r
    [
      {
        "service_name": "smtp",
        "service_type": "inet",
        "private": "n",
        "unprivileged": "-",
        "chroot": "y",
        "wake_up_time": "-",
        "process_limit": "-",
        "command": "smtpd"
      },
      {
        "service_name": "pickup",
        "service_type": "unix",
        "private": "n",
        "unprivileged": "-",
        "chroot": "y",
        "wake_up_time": "60",
        "process_limit": "1",
        "command": "pickup"
      }
    ]

<a id="jc.parsers.postconf.parse"></a>

### parse

```python
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[Dict]
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) unprocessed output if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    List of Dictionaries. Raw or processed structured data.

### Parser Information
Compatibility:  linux

Source: [`jc/parsers/postconf.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/postconf.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
