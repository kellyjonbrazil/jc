[Home](https://kellyjonbrazil.github.io/jc/)

# jc.parsers.systemctl_ls
jc - JSON CLI output utility `systemctl list-sockets` command output parser

Usage (cli):

    $ systemctl list-sockets | jc --systemctl-ls

    or

    $ jc systemctl list-sockets

Usage (module):

    import jc.parsers.systemctl_ls
    result = jc.parsers.systemctl_ls.parse(systemctl_ls_command_output)

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


## info
```python
info()
```
Provides parser metadata (version, author, etc.)

## parse
```python
parse(data, raw=False, quiet=False)
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) output preprocessed JSON if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    List of Dictionaries. Raw or processed structured data.

## Parser Information
Compatibility:  linux

Version 1.4 by Kelly Brazil (kellyjonbrazil@gmail.com)
