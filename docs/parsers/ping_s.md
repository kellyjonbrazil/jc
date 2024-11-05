[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.ping_s"></a>

# jc.parsers.ping_s

jc - JSON Convert `ping` command output streaming parser

> This streaming parser outputs JSON Lines (cli) or returns an Iterable of
> Dictionaries (module)

Supports `ping` and `ping6` output.

Usage (cli):

    $ ping 1.2.3.4 | jc --ping-s

> Note: When piping `jc` converted `ping` output to other processes it may
> appear the output is hanging due to the OS pipe buffers. This is because
> `ping` output is too small to quickly fill up the buffer. Use the `-u`
> option to unbuffer the `jc` output if you would like immediate output.
> See the [readme](https://github.com/kellyjonbrazil/jc/tree/master#unbuffering-output)
> for more information.

Usage (module):

    import jc

    result = jc.parse('ping_s', ping_command_output.splitlines())
    for item in result:
        # do something

Schema:

    {
      "type":                       string,   # [0]
      "source_ip":                  string,
      "destination_ip":             string,
      "sent_bytes":                 integer,
      "pattern":                    string,   # null if not set
      "destination":                string,
      "timestamp":                  float,
      "response_bytes":             integer,
      "response_ip":                string,
      "icmp_seq":                   integer,
      "ttl":                        integer,
      "time_ms":                    float,
      "duplicate":                  boolean,
      "packets_transmitted":        integer,
      "packets_received":           integer,
      "packet_loss_percent":        float,
      "duplicates":                 integer,
      "errors":                     integer,  # null if not set
      "corrupted":                  integer,  # null if not set
      "round_trip_ms_min":          float,    # null if not set
      "round_trip_ms_avg":          float,    # null if not set
      "round_trip_ms_max":          float,    # null if not set
      "round_trip_ms_stddev":       float,    # null if not set

      # below object only exists if using -qq or ignore_exceptions=True
      "_jc_meta": {
        "success":                  boolean,  # false if error parsing
        "error":                    string,   # exists if "success" is false
        "line":                     string    # exists if "success" is false
      }
    }

    [0] 'reply', 'timeout', 'summary', etc. See `_error_type.type_map`
        for all options.

Examples:

    $ ping 1.1.1.1 | jc --ping-s
    {"type":"reply","destination_ip":"1.1.1.1","sent_bytes":56,"patte...}
    {"type":"reply","destination_ip":"1.1.1.1","sent_bytes":56,"patte...}
    {"type":"reply","destination_ip":"1.1.1.1","sent_bytes":56,"patte...}
    ...

    $ ping 1.1.1.1 | jc --ping-s -r
    {"type":"reply","destination_ip":"1.1.1.1","sent_bytes":"56","patte...}
    {"type":"reply","destination_ip":"1.1.1.1","sent_bytes":"56","patte...}
    {"type":"reply","destination_ip":"1.1.1.1","sent_bytes":"56","patte...}
    ...

<a id="jc.parsers.ping_s.parse"></a>

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
Compatibility:  linux, darwin, freebsd

Source: [`jc/parsers/ping_s.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/ping_s.py)

Version 1.6 by Kelly Brazil (kellyjonbrazil@gmail.com)
