[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.iostat_s"></a>

# jc.parsers.iostat_s

jc - JSON Convert `iostat` command output streaming parser

> This streaming parser outputs JSON Lines (cli) or returns an Iterable of
> Dictionaries (module)

> Note: `iostat` version 11 and higher include a JSON output option

Usage (cli):

    $ iostat | jc --iostat-s

> Note: When piping `jc` converted `iostat` output to other processes it may
> appear the output is hanging due to the OS pipe buffers. This is because
> `iostat` output is too small to quickly fill up the buffer. Use the `-u`
> option to unbuffer the `jc` output if you would like immediate output. See
> the [readme](https://github.com/kellyjonbrazil/jc/tree/master#unbuffering-output)
> for more information.

Usage (module):

    import jc

    result = jc.parse('iostat_s', iostat_command_output.splitlines())
    for item in result:
        # do something

Schema:

    {
      "type":             string,
      "percent_user":     float,
      "percent_nice":     float,
      "percent_system":   float,
      "percent_iowait":   float,
      "percent_steal":    float,
      "percent_idle":     float,
      "device":           string,
      "tps":              float,
      "kb_read_s":        float,
      "mb_read_s":        float,
      "kb_wrtn_s":        float,
      "mb_wrtn_s":        float,
      "kb_read":          integer,
      "mb_read":          integer,
      "kb_wrtn":          integer,
      "mb_wrtn":          integer,
      'kb_dscd':          integer,
      'mb_dscd':          integer,
      "rrqm_s":           float,
      "wrqm_s":           float,
      "r_s":              float,
      "w_s":              float,
      "rmb_s":            float,
      "rkb_s":            float,
      "wmb_s":            float,
      "wkb_s":            float,
      "avgrq_sz":         float,
      "avgqu_sz":         float,
      "await":            float,
      "r_await":          float,
      "w_await":          float,
      "svctm":            float,
      "aqu_sz":           float,
      "rareq_sz":         float,
      "wareq_sz":         float,
      "d_s":              float,
      "dkb_s":            float,
      "dmb_s":            float,
      "drqm_s":           float,
      "percent_drqm":     float,
      "d_await":          float,
      "dareq_sz":         float,
      "f_s":              float,
      "f_await":          float,
      "kb_dscd_s":        float,
      "mb_dscd_s":        float,
      "percent_util":     float,
      "percent_rrqm":     float,
      "percent_wrqm":     float,

      # below object only exists if using -qq or ignore_exceptions=True
      "_jc_meta": {
        "success":        boolean,     # false if error parsing
        "error":          string,      # exists if "success" is false
        "line":           string       # exists if "success" is false
      }
    }

Examples:

    $ iostat | jc --iostat-s
    {"percent_user":0.14,"percent_nice":0.0,"percent_system":0.16,...}
    {"device":"sda","tps":0.24,"kb_read_s":5.28,"kb_wrtn_s":1.1...}
    ...

    $ iostat | jc --iostat-s -r
    {"percent_user":"0.14","percent_nice":"0.00","percent_system":"0.16"...}
    {"device":"sda","tps":"0.24","kb_read_s":"5.28","kb_wrtn_s":"1.10"...}
    ...

<a id="jc.parsers.iostat_s.parse"></a>

### parse

```python
def parse(data, raw=False, quiet=False, ignore_exceptions=False)
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

Source: [`jc/parsers/iostat_s.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/iostat_s.py)

Version 1.3 by Kelly Brazil (kellyjonbrazil@gmail.com)
