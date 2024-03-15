[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.needrestart"></a>

# jc.parsers.needrestart

jc - JSON Convert `needrestart -b` command output parser

Usage (cli):

    $ needrestart -b | jc --needrestart

or

    $ jc needrestart -b

Usage (module):

    import jc
    result = jc.parse('needrestart', needrestart_command_output)

Schema:

    {
      "version":                        string,
      "running_kernel_version":         string,
      "expected_kernel_version":        string,
      "kernel_status":                  integer,
      "container":                      string,
      "session": [
                                        string
      ],
      "service": [
                                        string
      ],
      "pid": [
                                        string
      ]
    }

Examples:

    $ needrestart -b | jc --needrestart -p
    {
      "version": "2.1",
      "running_kernel_version": "3.19.3-tl1+",
      "expected_kernel_version": "3.19.3-tl1+",
      "kernel_status": 1,
      "container": "LXC web1",
      "session": [
        "metabase @ user manager service",
        "root @ session #28017"
      ],
      "service": [
        "systemd-journald.service",
        "systemd-machined.service"
      ]
    }

    $ needrestart -b | jc --needrestart -p -r
    {
      "needrestart_ver": "2.1",
      "needrestart_kcur": "3.19.3-tl1+",
      "needrestart_kexp": "3.19.3-tl1+",
      "needrestart_ksta": "1",
      "needrestart_cont": "LXC web1",
      "needrestart_sess": [
        "metabase @ user manager service",
        "root @ session #28017"
      ],
      "needrestart_svc": [
        "systemd-journald.service",
        "systemd-machined.service"
      ]
    }

<a id="jc.parsers.needrestart.parse"></a>

### parse

```python
def parse(data: str, raw: bool = False, quiet: bool = False) -> Dict[str, Any]
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

Source: [`jc/parsers/needrestart.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/needrestart.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
