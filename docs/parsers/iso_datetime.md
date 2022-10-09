[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.iso_datetime"></a>

# jc.parsers.iso\_datetime

jc - JSON Convert ISO 8601 Datetime string parser

This parser has been renamed to datetime-iso (cli) or datetime_iso (module).

This parser will be removed in a future version, so please start using
the new parser name.

<a id="jc.parsers.iso_datetime.parse"></a>

### parse

```python
def parse(data, raw=False, quiet=False)
```

This parser is deprecated and calls datetime_iso. Please use datetime_iso
directly. This parser will be removed in the future.

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) unprocessed output if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    Dictionary. Raw or processed structured data.

### Parser Information
Compatibility:  linux, aix, freebsd, darwin, win32, cygwin

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
