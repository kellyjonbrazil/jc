[Home](https://kellyjonbrazil.github.io/jc/)

# jc.parsers.ping_s
jc - JSON CLI output utility `ping` command output streaming parser

Supports `ping` and `ping6` output.

Usage (cli):

    $ ping | jc --ping-s

> Note: When piping `jc` converted ping output to other processes it may appear the output is hanging due to the OS pipe buffers. This is because `ping` output is too small to quickly fill up the buffer. Use the `-u` option to unbuffer the `jc` output if you would like immediate output. See the [readme](https://github.com/kellyjonbrazil/jc/tree/streaming#streaming-parsers) for more information.

Usage (module):

    import jc.parsers.ping_s
    result = jc.parsers.ping_s.parse(ping_command_output.splitlines())    # result is an iterable object
    for item in result:
        # do something

Schema:

    {
      "type":                        string,        # 'reply', 'timeout', 'summary', etc. See `_error_type.type_map` for all options.
      "source_ip":                   string,
      "destination_ip":              string,
      "sent_bytes":                  integer,
      "pattern":                     string,        # (null if not set)
      "destination":                 string,
      "timestamp":                   float,
      "response_bytes":              integer,
      "response_ip":                 string,
      "icmp_seq":                    integer,
      "ttl":                         integer,
      "time_ms":                     float,
      "duplicate":                   boolean,
      "packets_transmitted":         integer,
      "packets_received":            integer,
      "packet_loss_percent":         float,
      "duplicates":                  integer,
      "round_trip_ms_min":           float,
      "round_trip_ms_avg":           float,
      "round_trip_ms_max":           float,
      "round_trip_ms_stddev":        float,
      "_meta":                                     # This object only exists if using -q or quiet=True
        {
          "success":                 booean,       # true if successfully parsed, false if error
          "error":                   string,       # exists if "success" is false
          "line":                    string        # exists if "success" is false
        }
    }

Examples:

    $ ping 1.1.1.1 | jc --ping-s
    {"type":"reply","destination_ip":"1.1.1.1","sent_bytes":56,"pattern":null,"response_bytes":64,"response_ip":"1.1.1.1","icmp_seq":0,"ttl":56,"time_ms":23.703}
    {"type":"reply","destination_ip":"1.1.1.1","sent_bytes":56,"pattern":null,"response_bytes":64,"response_ip":"1.1.1.1","icmp_seq":1,"ttl":56,"time_ms":22.862}
    {"type":"reply","destination_ip":"1.1.1.1","sent_bytes":56,"pattern":null,"response_bytes":64,"response_ip":"1.1.1.1","icmp_seq":2,"ttl":56,"time_ms":22.82}
    ...

    $ ping 1.1.1.1 | jc --ping-s -r
    {"type":"reply","destination_ip":"1.1.1.1","sent_bytes":"56","pattern":null,"response_bytes":"64","response_ip":"1.1.1.1","icmp_seq":"0","ttl":"56","time_ms":"23.054"}
    {"type":"reply","destination_ip":"1.1.1.1","sent_bytes":"56","pattern":null,"response_bytes":"64","response_ip":"1.1.1.1","icmp_seq":"1","ttl":"56","time_ms":"24.739"}
    {"type":"reply","destination_ip":"1.1.1.1","sent_bytes":"56","pattern":null,"response_bytes":"64","response_ip":"1.1.1.1","icmp_seq":"2","ttl":"56","time_ms":"23.232"}
    ...


## info
```python
info()
```
Provides parser metadata (version, author, etc.)

## parse
```python
parse(data, raw=False, quiet=False)
```

Main text parsing generator function. Returns an iterator object.

Parameters:

    data:        (iterable)  line-based text data to parse (e.g. sys.stdin or str.splitlines())
    raw:         (boolean)   output preprocessed JSON if True
    quiet:       (boolean)   suppress warning messages and ignore parsing exceptions if True

Yields:

    Dictionary. Raw or processed structured data.

Returns:

    Iterator object

## Parser Information
Compatibility:  linux, darwin, freebsd

Version 0.5 by Kelly Brazil (kellyjonbrazil@gmail.com)
