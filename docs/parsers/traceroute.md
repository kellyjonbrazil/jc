# jc.parsers.traceroute
jc - JSON CLI output utility traceroute Parser

Usage:

    specify --traceroute as the first argument if the piped input is coming from traceroute

    Note: on OSX and FreeBSD be sure to redirect STDERR to STDOUT since the header line is sent to STDERR
          e.g. $ traceroute 8.8.8.8 2>&1 | jc --traceroute

Compatibility:

    'linux', 'darwin', 'freebsd'

Examples:

    $ traceroute google.com | jc --traceroute -p
    {
      "destination_ip": "216.58.194.46",
      "destination_name": "google.com",
      "hops": [
        {
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
        },
        ...
      ]
    }

    $ traceroute google.com  | jc --traceroute -p -r
    {
      "destination_ip": "216.58.194.46",
      "destination_name": "google.com",
      "hops": [
        {
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
        },
        ...
      ]
    }

## info
```python
info(self, /, *args, **kwargs)
```

## Hop
```python
Hop(self, idx)
```

## process
```python
process(proc_data)
```

Final processing to conform to the schema.

Parameters:

    proc_data:   (dictionary) raw structured data to process

Returns:

    Dictionary. Structured data with the following schema:

    {
      "destination_ip":         string,
      "destination_name":       string,
      "hops": [
        {
          "hop":                integer,
          "probes": [
            {
              "annotation":     string,
              "asn":            integer,
              "ip":             string,
              "name":           string,
              "rtt":            float
            }
          ]
        }
      ]
    }

## parse
```python
parse(data, raw=False, quiet=False)
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) output preprocessed JSON if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    Dictionary. Raw or processed structured data.

