[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.uname"></a>

# jc.parsers.uname

jc - JSON Convert `uname -a` command output parser

> Note: Must use `uname -a`

Usage (cli):

    $ uname -a | jc --uname

or

    $ jc uname -a

Usage (module):

    import jc
    result = jc.parse('uname', uname_command_output)

Schema:

    {
        "kernel_name":        string,
        "node_name":          string,
        "kernel_release":     string,
        "operating_system":   string,
        "hardware_platform":  string,
        "processor":          string,
        "machine":            string,
        "kernel_version":     string
    }

Example:

    $ uname -a | jc --uname -p
    {
      "kernel_name": "Linux",
      "node_name": "user-ubuntu",
      "kernel_release": "4.15.0-65-generic",
      "operating_system": "GNU/Linux",
      "hardware_platform": "x86_64",
      "processor": "x86_64",
      "machine": "x86_64",
      "kernel_version": "#74-Ubuntu SMP Tue Sep 17 17:06:04 UTC 2019"
    }

<a id="jc.parsers.uname.parse"></a>

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

    Dictionary. Raw or processed structured data.

### Parser Information
Compatibility:  linux, darwin, freebsd

Source: [`jc/parsers/uname.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/uname.py)

This parser can be used with the `--slurp` command-line option.

Version 1.8 by Kelly Brazil (kellyjonbrazil@gmail.com)
