[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.upsc"></a>

# jc.parsers.upsc

jc - JSON Convert `upsc` command output parser

Parses the output of the `upsc` command from Network UPS Tools (NUT),
which reports UPS status as simple `key: value` pairs.

An attempt is made to convert values that are obviously numeric (integers
and floats) while leaving identifier-like values (such as serial numbers
or vendor/product IDs that have significant leading zeros) as strings. If
no conversion is desired, use the `-r` command-line argument or the
`raw=True` argument in `parse()`.

Usage (cli):

    $ upsc ups@localhost | jc --upsc

or

    $ jc upsc ups@localhost

Usage (module):

    import jc
    result = jc.parse('upsc', upsc_command_output)

Schema:

    {
      "key1":     string/integer/float,     # best guess based on value
      "key2":     string/integer/float,
      "key3":     string/integer/float
    }

Examples:

    $ upsc ups@localhost | jc --upsc -p
    {
      "battery_charge": 100,
      "battery_voltage": 24.0,
      "device_serial": "000000000000",
      "ups_status": "OL",
      "ups_vendorid": "0764"
      ...
    }

    $ upsc ups@localhost | jc --upsc -p -r
    {
      "battery_charge": "100",
      "battery_voltage": "24.0",
      "device_serial": "000000000000",
      "ups_status": "OL",
      "ups_vendorid": "0764"
      ...
    }

<a id="jc.parsers.upsc.parse"></a>

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

Source: [`jc/parsers/upsc.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/upsc.py)

Version 1.0 by Mayoka (j.mayoka@mayokajohn.com)
