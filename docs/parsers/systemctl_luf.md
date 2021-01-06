
# jc.parsers.systemctl_luf
jc - JSON CLI output utility `systemctl list-unit-files` command output parser

Usage (cli):

    $ systemctl list-unit-files | jc --systemctl-luf

    or

    $ jc systemctl list-unit-files

Usage (module):

    import jc.parsers.systemctl_luf
    result = jc.parsers.systemctl_luf.parse(systemctl_luf_command_output)

Compatibility:

    'linux'

Examples:

    $ systemctl list-unit-files | jc --systemctl-luf -p
    [
      {
        "unit_file": "proc-sys-fs-binfmt_misc.automount",
        "state": "static"
      },
      {
        "unit_file": "dev-hugepages.mount",
        "state": "static"
      },
      {
        "unit_file": "dev-mqueue.mount",
        "state": "static"
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
        "unit_file":   string,
        "state":       string
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

