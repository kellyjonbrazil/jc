[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.ping"></a>

# jc.parsers.ping

jc - JSON Convert `ping` command output parser

Supports `ping` and `ping6` output.

Usage (cli):

> Note:  Use the ping `-c` (count) option, otherwise data will not be
> piped to `jc`.

    $ ping -c 3 1.2.3.4 | jc --ping

or

    $ jc ping -c 3 1.2.3.4

Usage (module):

    import jc
    result = jc.parse('ping', ping_command_output)

Schema:

    {
      "source_ip":                   string,
      "destination_ip":              string,
      "data_bytes":                  integer,
      "pattern":                     string,        # null if not set
      "destination":                 string,
      "packets_transmitted":         integer,
      "packets_received":            integer,
      "packet_loss_percent":         float,
      "duplicates":                  integer,
      "errors":                      integer,
      "corrupted":                   integer,
      "round_trip_ms_min":           float,
      "round_trip_ms_avg":           float,
      "round_trip_ms_max":           float,
      "round_trip_ms_stddev":        float,
      "responses": [
        {
          "type":                    string,        # [0]
          "unparsed_line":           string,        # [1]
          "timestamp":               float,
          "bytes":                   integer,
          "response_ip":             string,
          "icmp_seq":                integer,
          "ttl":                     integer,
          "time_ms":                 float,
          "duplicate":               boolean,
          "vr":                      integer,       # [2]
          "hl":                      integer,       # [2]
          "tos":                     integer,       # [2]
          "len":                     integer,       # [2]
          "id":                      integer,       # [2]
          "flg":                     integer,       # [2]
          "off":                     integer,       # [2]
          "pro":                     integer,       # [2]
          "cks":                     ingeger,       # [2]
          "src":                     string,
          "dst":                     string
        }
      ]
    }

    [0] 'reply', 'timeout', 'unparsable_line', etc. See
        `_error_type.type_map` for all options
    [1] only if an 'unparsable_line' type
    [2] hex value converted to decimal

Examples:

    $ ping -c 3 -p ff cnn.com | jc --ping -p
    {
      "destination_ip": "151.101.1.67",
      "data_bytes": 56,
      "pattern": "0xff",
      "destination": "cnn.com",
      "packets_transmitted": 3,
      "packets_received": 3,
      "packet_loss_percent": 0.0,
      "duplicates": 0,
      "round_trip_ms_min": 28.015,
      "round_trip_ms_avg": 32.848,
      "round_trip_ms_max": 39.376,
      "round_trip_ms_stddev": 4.79,
      "responses": [
        {
          "type": "reply",
          "bytes": 64,
          "response_ip": "151.101.1.67",
          "icmp_seq": 0,
          "ttl": 59,
          "time_ms": 28.015,
          "duplicate": false
        },
        {
          "type": "reply",
          "bytes": 64,
          "response_ip": "151.101.1.67",
          "icmp_seq": 1,
          "ttl": 59,
          "time_ms": 39.376,
          "duplicate": false
        },
        {
          "type": "reply",
          "bytes": 64,
          "response_ip": "151.101.1.67",
          "icmp_seq": 2,
          "ttl": 59,
          "time_ms": 31.153,
          "duplicate": false
        }
      ]
    }

    $ ping -c 3 -p ff cnn.com | jc --ping -p -r
    {
      "destination_ip": "151.101.129.67",
      "data_bytes": "56",
      "pattern": "0xff",
      "destination": "cnn.com",
      "packets_transmitted": "3",
      "packets_received": "3",
      "packet_loss_percent": "0.0",
      "duplicates": "0",
      "round_trip_ms_min": "25.078",
      "round_trip_ms_avg": "29.543",
      "round_trip_ms_max": "32.553",
      "round_trip_ms_stddev": "3.221",
      "responses": [
        {
          "type": "reply",
          "bytes": "64",
          "response_ip": "151.101.129.67",
          "icmp_seq": "0",
          "ttl": "59",
          "time_ms": "25.078",
          "duplicate": false
        },
        {
          "type": "reply",
          "bytes": "64",
          "response_ip": "151.101.129.67",
          "icmp_seq": "1",
          "ttl": "59",
          "time_ms": "30.999",
          "duplicate": false
        },
        {
          "type": "reply",
          "bytes": "64",
          "response_ip": "151.101.129.67",
          "icmp_seq": "2",
          "ttl": "59",
          "time_ms": "32.553",
          "duplicate": false
        }
      ]
    }

<a id="jc.parsers.ping.parse"></a>

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

Source: [`jc/parsers/ping.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/ping.py)

Version 1.11 by Kelly Brazil (kellyjonbrazil@gmail.com)
