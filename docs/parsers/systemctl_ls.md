
# jc.parsers.systemctl_ls
jc - JSON CLI output utility `systemctl list-sockets` command output parser

Usage (cli):

    $ systemctl list-sockets | jc --systemctl-ls

    or

    $ jc systemctl list-sockets

Usage (module):

    import jc.parsers.systemctl_ls
    result = jc.parsers.systemctl_ls.parse(systemctl_ls_command_output)

Compatibility:

    'linux'

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


## process
```python
process(proc_data)
```

Final processing to conform to the schema.

Parameters:

    proc_data:   (List of Dictionaries) raw structured data to process

Returns:

    List of Dictionaries. Structured data with the following schema:

    [
      {
        "listen":       string,
        "unit":         string,
        "activates":    string
      }
    ]


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

