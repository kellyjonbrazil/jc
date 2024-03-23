[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.pidstat_s"></a>

# jc.parsers.pidstat_s

jc - JSON Convert `pidstat -H` command output streaming parser

> This streaming parser outputs JSON Lines (cli) or returns an Iterable of
> Dictionaries (module)

Must use the `-H` (or `-h`, if `-H` is not available) option in `pidstat`.
All other `pidstat` options are supported in combination with this option.

Usage (cli):

    $ pidstat -H | jc --pidstat-s

> Note: When piping `jc` converted `pidstat` output to other processes it
> may appear the output is hanging due to the OS pipe buffers. This is
> because `pidstat` output is too small to quickly fill up the buffer. Use
> the `-u` option to unbuffer the `jc` output if you would like immediate
> output. See the [readme](https://github.com/kellyjonbrazil/jc/tree/master#unbuffering-output)
> for more information.

Usage (module):

    import jc

    result = jc.parse('pidstat_s', pidstat_command_output.splitlines())
    for item in result:
        # do something

Schema:

    {
      "time":             integer,
      "uid":              integer,
      "pid":              integer,
      "percent_usr":      float,
      "percent_system":   float,
      "percent_guest":    float,
      "percent_wait":     float,
      "percent_cpu":      float,
      "cpu":              integer,
      "minflt_s":         float,
      "majflt_s":         float,
      "vsz":              integer,
      "rss":              integer,
      "percent_mem":      float,
      "stksize":          integer,
      "stkref":           integer,
      "kb_rd_s":          float,
      "kb_wr_s":          float,
      "kb_ccwr_s":        float,
      "cswch_s":          float,
      "nvcswch_s":        float,
      "usr_ms":           integer,
      "system_ms":        integer,
      "guest_ms":         integer,
      "command":          string,

      # below object only exists if using -qq or ignore_exceptions=True
      "_jc_meta": {
        "success":        boolean,     # false if error parsing
        "error":          string,      # exists if "success" is false
        "line":           string       # exists if "success" is false
      }
    }

Examples:

    $ pidstat -Hl | jc --pidstat-s
    {"time":1646859134,"uid":0,"pid":1,"percent_usr":0.0,"percent_syste...}
    {"time":1646859134,"uid":0,"pid":6,"percent_usr":0.0,"percent_syste...}
    {"time":1646859134,"uid":0,"pid":9,"percent_usr":0.0,"percent_syste...}
    ...

    $ pidstat -Hl | jc --pidstat-s -r
    {"time":"1646859134","uid":"0","pid":"1","percent_usr":"0.00","perc...}
    {"time":"1646859134","uid":"0","pid":"6","percent_usr":"0.00","perc...}
    {"time":"1646859134","uid":"0","pid":"9","percent_usr":"0.00","perc...}
    ...

<a id="jc.parsers.pidstat_s.parse"></a>

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
Compatibility:  linux

Source: [`jc/parsers/pidstat_s.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/pidstat_s.py)

Version 1.2 by Kelly Brazil (kellyjonbrazil@gmail.com)
