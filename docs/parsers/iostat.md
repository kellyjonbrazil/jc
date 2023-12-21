[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.iostat"></a>

# jc.parsers.iostat

jc - JSON Convert `iostat` command output parser

> Note: `iostat` version 11 and higher include a JSON output option

Usage (cli):

    $ iostat | jc --iostat

or

    $ jc iostat

Usage (module):

    import jc
    result = jc.parse('iostat', iostat_command_output)

Schema:

    [
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
        "percent_wrqm":     float
      }
    ]

Examples:

    $ iostat | jc --iostat -p
    [
      {
          "percent_user": 0.15,
          "percent_nice": 0.0,
          "percent_system": 0.18,
          "percent_iowait": 0.0,
          "percent_steal": 0.0,
          "percent_idle": 99.67,
          "type": "cpu"
      },
      {
          "device": "sda",
          "tps": 0.29,
          "kb_read_s": 7.22,
          "kb_wrtn_s": 1.25,
          "kb_read": 194341,
          "kb_wrtn": 33590,
          "type": "device"
      },
      {
          "device": "dm-0",
          "tps": 0.29,
          "kb_read_s": 5.99,
          "kb_wrtn_s": 1.17,
          "kb_read": 161361,
          "kb_wrtn": 31522,
          "type": "device"
      },
      {
          "device": "dm-1",
          "tps": 0.0,
          "kb_read_s": 0.08,
          "kb_wrtn_s": 0.0,
          "kb_read": 2204,
          "kb_wrtn": 0,
          "type": "device"
      }
    ]

    $ iostat | jc --iostat -p -r
    [
      {
        "percent_user": "0.15",
        "percent_nice": "0.00",
        "percent_system": "0.18",
        "percent_iowait": "0.00",
        "percent_steal": "0.00",
        "percent_idle": "99.67",
        "type": "cpu"
      },
      {
        "device": "sda",
        "tps": "0.29",
        "kb_read_s": "7.22",
        "kb_wrtn_s": "1.25",
        "kb_read": "194341",
        "kb_wrtn": "33590",
        "type": "device"
      },
      {
        "device": "dm-0",
        "tps": "0.29",
        "kb_read_s": "5.99",
        "kb_wrtn_s": "1.17",
        "kb_read": "161361",
        "kb_wrtn": "31522",
        "type": "device"
      },
      {
        "device": "dm-1",
        "tps": "0.00",
        "kb_read_s": "0.08",
        "kb_wrtn_s": "0.00",
        "kb_read": "2204",
        "kb_wrtn": "0",
        "type": "device"
      }
    ]

<a id="jc.parsers.iostat.parse"></a>

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

Source: [`jc/parsers/iostat.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/iostat.py)

Version 1.1 by Kelly Brazil (kellyjonbrazil@gmail.com)
