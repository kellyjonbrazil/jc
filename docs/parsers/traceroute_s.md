[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.traceroute_s"></a>

# jc.parsers.traceroute_s

jc - JSON Convert `traceroute` command output streaming parser

> This streaming parser outputs JSON Lines (cli) or returns an Iterable of
> Dictionaries (module)

Supports `traceroute` and `traceroute6` output.

> Note: On some operating systems you will need to redirect `STDERR` to
> `STDOUT` for destination info since the header line is sent to
> `STDERR`. A warning message will be printed to `STDERR` if the
> header row is not found.
>
> e.g. `$ traceroute 8.8.8.8 2>&1 | jc --traceroute-s`

Usage (cli):

    $ traceroute 1.2.3.4 | jc --traceroute-s

Usage (module):

    import jc
    result = jc.parse('traceroute_s', traceroute_command_output.splitlines())
    for item in result:
        # do something

Schema:

    {
      # 'header' or 'hop'
      "type":                 string,

      # 'header' type has the fields below:
      "destination_ip":       string,
      "destination_name":     string,
      "max_hops":             integer,
      "data_bytes":           integer,

      # 'hop' type has the fields below:
      "hop":                  integer,
      "probes": [
        {
          "annotation":       string,
          "asn":              integer,
          "ip":               string,
          "name":             string,
          "rtt":              float
        }
      ]

      # below object only exists if using -qq or ignore_exceptions=True
      "_jc_meta": {
        "success":            boolean,  # false if error parsing
        "error":              string,   # exists if "success" is false
        "line":               string    # exists if "success" is false
      }
    }

Examples:

    $ traceroute google.com | jc --traceroute-s -p
    {
      "type": "header",
      "destination_ip": "216.58.194.46",
      "destination_name": "google.com",
      "max_hops": 30,
      "data_bytes": 60
    }
    {
      "type": "hop",
      "hop": 1,
      "probes": [
        {
          "annotation": null,
          "asn": null,
          "ip": "216.230.231.141",
          "name": "216-230-231-141.static.houston.tx.oplink.net",
          "rtt": 198.574
        },
        {
          "annotation": null,
          "asn": null,
          "ip": "216.230.231.141",
          "name": "216-230-231-141.static.houston.tx.oplink.net",
          "rtt": null
        },
        {
          "annotation": null,
          "asn": null,
          "ip": "216.230.231.141",
          "name": "216-230-231-141.static.houston.tx.oplink.net",
          "rtt": 198.65
        }
      ]
    }
    ...

    $ traceroute google.com  | jc --traceroute-s -p -r
    {
      "type": "header",
      "destination_ip": "216.58.194.46",
      "destination_name": "google.com",
      "max_hops": "30",
      "data_bytes": "60"
    }
    {
      "type": "hop",
      "hop": "1",
      "probes": [
        {
          "annotation": null,
          "asn": null,
          "ip": "216.230.231.141",
          "name": "216-230-231-141.static.houston.tx.oplink.net",
          "rtt": "198.574"
        },
        {
          "annotation": null,
          "asn": null,
          "ip": "216.230.231.141",
          "name": "216-230-231-141.static.houston.tx.oplink.net",
          "rtt": null
        },
        {
          "annotation": null,
          "asn": null,
          "ip": "216.230.231.141",
          "name": "216-230-231-141.static.houston.tx.oplink.net",
          "rtt": "198.650"
        }
      ]
    }
    ...

<a id="jc.parsers.traceroute_s.parse"></a>

### parse

```python
def parse(data, raw=False, quiet=False, ignore_exceptions=False)
```

Main text parsing function. Returns an iterable object.

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

Source: [`jc/parsers/traceroute_s.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/traceroute_s.py)

Version 1.0 by Shintaro Kojima (goodies@codeout.net)
