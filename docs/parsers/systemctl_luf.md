[Home](https://kellyjonbrazil.github.io/jc/)
# Table of Contents

* [jc.parsers.systemctl\_luf](#jc.parsers.systemctl_luf)
  * [parse](#jc.parsers.systemctl_luf.parse)

<a id="jc.parsers.systemctl_luf"></a>

# jc.parsers.systemctl\_luf

jc - JSON CLI output utility `systemctl list-unit-files` command output
parser

Usage (cli):

    $ systemctl list-unit-files | jc --systemctl-luf

    or

    $ jc systemctl list-unit-files

Usage (module):

    import jc
    result = jc.parse('systemctl_luf', systemctl_luf_command_output)

    or

    import jc.parsers.systemctl_luf
    result = jc.parsers.systemctl_luf.parse(systemctl_luf_command_output)

Schema:

    [
      {
        "unit_file":   string,
        "state":       string
      }
    ]

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

<a id="jc.parsers.systemctl_luf.parse"></a>

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

Version 1.5 by Kelly Brazil (kellyjonbrazil@gmail.com)
