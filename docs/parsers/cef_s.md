[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.cef_s"></a>

# jc.parsers.cef_s

jc - JSON Convert CEF string output streaming parser

> This streaming parser outputs JSON Lines (cli) or returns an Iterable of
> Dictionaries (module)

This parser conforms to the Microfocus Arcsight CEF specification.

This parser will accept a single CEF string or multiple CEF string lines.
Any text before "CEF" will be ignored. Syslog and CEF escaped characters
(`\\`, `\\"`, `\\]`, `\\|`, `\\=`, `\\%`, `\\#`, `\\n`, and `\\r`) are
unescaped.

Extended fields, as defined in the CEF specification, are relabeled
and the values are converted to their respective types. Extra naive and
UTC epoch timestamps are added where appropriate per the CEF specification.

A warning message to `STDERR` will be printed if an unparsable line is found
unless `--quiet` or `quiet=True` is used.

To preserve escaping and original keynames and to prevent type conversions
use the `--raw` CLI option or `raw=True` param in the `parse()` function.

Usage (cli):

    $ echo 'CEF:0|Vendor|Product|3.2.0|1|SYSTEM|1|... | jc --cef-s

Usage (module):

    import jc

    result = jc.parse('cef_s', cef_command_output.splitlines())
    for item in result:
        # do something

Schema:

See: https://www.microfocus.com/documentation/arcsight/arcsight-smartconnectors-8.3/cef-implementation-standard/Content/CEF/Chapter%201%20What%20is%20CEF.htm

> Note: Special characters in key names will be converted to underscores.

    {
      "deviceVendor":                   string,
      "deviceProduct":                  string,
      "deviceVersion":                  string,
      "deviceEventClassId":             string,
      "deviceEventClassIdNum":          integer/null,
      "name":                           string,
      "agentSeverity":                  string/integer,
      "agentSeverityString":            string,
      "agentSeverityNum":               integer/null,
      "CEFVersion":                     integer,
      <extended fields>                 string/integer/float,  # [0]
      <extended fields>"_epoch":        integer/null,  # [1]
      <extended fields>"_epoch_utc":    integer/null,  # [2]
      <custom fields>                   string,
      "unparsable":                     string  # [3]

      # below object only exists if using -qq or ignore_exceptions=True
      "_jc_meta": {
        "success":      boolean,     # false if error parsing
        "error":        string,      # exists if "success" is false
        "line":         string       # exists if "success" is false
      }
    }

    [0] Will attempt to convert extended fields to the type specified in the
        CEF specification. If conversion fails, then the field will remain
        a string.
    [1] Naive calculated epoch timestamp
    [2] Timezone-aware calculated epoch timestamp. (UTC only) This value
        will be null if a UTC timezone cannot be extracted from the original
        timestamp string value.
    [3] This field exists if the CEF line is not parsable. The value
        is the original syslog line.

Examples:

    $ cat cef.log | jc --cef-s
    {"deviceVendor":"Fortinet","deviceProduct":"FortiDeceptor","deviceV...}
    {"deviceVendor":"Trend Micro","deviceProduct":"Deep Security Agent"...}
    ...

    $ cat cef.log | jc --cef-s -r
    {"deviceVendor":"Fortinet","deviceProduct":"FortiDeceptor","deviceV...}
    {"deviceVendor":"Trend Micro","deviceProduct":"Deep Security Agent"...}
    ...

<a id="jc.parsers.cef_s.parse"></a>

### parse

```python
def parse(data: Iterable[str],
          raw: bool = False,
          quiet: bool = False,
          ignore_exceptions: bool = False) -> Union[Iterable[Dict], tuple]
```

Main text parsing generator function. Returns an iterable object.

Parameters:

    data:              (iterable)  line-based text data to parse
                                   (e.g. sys.stdin or str.splitlines())

    raw:               (boolean)   unprocessed output if True
    quiet:             (boolean)   suppress warning messages if True
    ignore_exceptions: (boolean)   ignore parsing exceptions if True


Returns:

    Iterable of Dictionaries

### Parser Information
Compatibility:  linux, darwin, cygwin, win32, aix, freebsd

Source: [`jc/parsers/cef_s.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/cef_s.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
