[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.systemctl_ls"></a>

# jc.parsers.systemctl_ls

jc - JSON Convert `systemctl list-sockets` command output
parser

Usage (cli):

    $ systemctl list-sockets | jc --systemctl-ls

or

    $ jc systemctl list-sockets

Usage (module):

    import jc
    result = jc.parse('systemctl_ls', systemctl_ls_command_output)

Schema:

    [
      {
        "listen":       string,
        "unit":         string,
        "activates":    string
      }
    ]

Examples:

    $ systemctl list-sockets | jc --systemctl-ls -p
    [
      {
        "listen": "/dev/log",
        "unit": "systemd-journald.socket",
        "activates": "systemd-journald.service"
      },
      {
        "listen": "/run/dbus/system_bus_socket",
        "unit": "dbus.socket",
        "activates": "dbus.service"
      },
      {
        "listen": "/run/dmeventd-client",
        "unit": "dm-event.socket",
        "activates": "dm-event.service"
      },
      ...
    ]

<a id="jc.parsers.systemctl_ls.parse"></a>

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

    List of Dictionaries. Raw or processed structured data.

### Parser Information
Compatibility:  linux

Source: [`jc/parsers/systemctl_ls.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/systemctl_ls.py)

Version 1.5 by Kelly Brazil (kellyjonbrazil@gmail.com)
