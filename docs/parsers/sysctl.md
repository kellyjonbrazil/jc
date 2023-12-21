[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.sysctl"></a>

# jc.parsers.sysctl

jc - JSON Convert `sysctl -a` command output parser

> Note: Since `sysctl` output is not easily parsable only a very simple
> key/value object will be output. An attempt is made to convert obvious
> integers and floats. If no conversion is desired, use the `-r`
> command-line argument or the `raw=True` argument in `parse()`.

Usage (cli):

    $ sysctl -a | jc --sysctl

or

    $ jc sysctl -a

Usage (module):

    import jc
    result = jc.parse('sysctl', sysctl_command_output)

Schema:

    {
      "key1":     string/integer/float,     # best guess based on value
      "key2":     string/integer/float,
      "key3":     string/integer/float
    }

Examples:

    $ sysctl -a | jc --sysctl -p
    {
      "user.cs_path": "/usr/bin:/bin:/usr/sbin:/sbin",
      "user.bc_base_max": 99,
      "user.bc_dim_max": 2048,
      "user.bc_scale_max": 99,
      "user.bc_string_max": 1000,
      "user.coll_weights_max": 2,
      "user.expr_nest_max": 32
      ...
    }

    $ sysctl -a | jc --sysctl -p -r
    {
      "user.cs_path": "/usr/bin:/bin:/usr/sbin:/sbin",
      "user.bc_base_max": "99",
      "user.bc_dim_max": "2048",
      "user.bc_scale_max": "99",
      "user.bc_string_max": "1000",
      "user.coll_weights_max": "2",
      "user.expr_nest_max": "32",
      ...
    }

<a id="jc.parsers.sysctl.parse"></a>

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

Source: [`jc/parsers/sysctl.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/sysctl.py)

Version 1.2 by Kelly Brazil (kellyjonbrazil@gmail.com)
