[Home](https://kellyjonbrazil.github.io/jc/)

# jc.parsers.iostat_s
jc - JSON CLI output utility `iostat` command output streaming parser

> This streaming parser outputs JSON Lines

Note: `iostat` version 11 and higher include a JSON output option

Usage (cli):

    $ iostat | jc --iostat-s

Usage (module):

    import jc
    result = jc.parse('iostat_s', iostat_command_output.splitlines())    # result is an iterable object
    for item in result:
        # do something

    or

    import jc.parsers.iostat_s
    result = jc.parsers.iostat_s.parse(iostat_command_output.splitlines())    # result is an iterable object
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
      "_jc_meta":                      # This object only exists if using -qq or ignore_exceptions=True
        {
          "success":      boolean,     # true if successfully parsed, false if error
          "error":        string,      # exists if "success" is false
          "line":         string       # exists if "success" is false
        }
    }

Examples:

    $ iostat | jc --iostat-s
    {"percent_user":0.14,"percent_nice":0.0,"percent_system":0.16,"percent_iowait":0.0,"percent_steal":0.0,"percent_idle":99.7,"type":"cpu"}
    {"device":"sda","tps":0.24,"kb_read_s":5.28,"kb_wrtn_s":1.1,"kb_read":203305,"kb_wrtn":42368,"type":"device"}
    ...

    $ iostat | jc --iostat-s -r
    {"percent_user":"0.14","percent_nice":"0.00","percent_system":"0.16","percent_iowait":"0.00","percent_steal":"0.00","percent_idle":"99.70","type":"cpu"}
    {"device":"sda","tps":"0.24","kb_read_s":"5.28","kb_wrtn_s":"1.10","kb_read":"203305","kb_wrtn":"42368","type":"device"}
    ...


## info
```python
info()
```
Provides parser metadata (version, author, etc.)

## parse
```python
parse(data, raw=False, quiet=False, ignore_exceptions=False)
```

Main text parsing generator function. Returns an iterator object.

Parameters:

    data:              (iterable)  line-based text data to parse (e.g. sys.stdin or str.splitlines())
    raw:               (boolean)   output preprocessed JSON if True
    quiet:             (boolean)   suppress warning messages if True
    ignore_exceptions: (boolean)   ignore parsing exceptions if True

Yields:

    Dictionary. Raw or processed structured data.

Returns:

    Iterator object

## Parser Information
Compatibility:  linux

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
