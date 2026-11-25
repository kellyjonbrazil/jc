[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.prometheus"></a>

# jc.parsers.prometheus

jc - JSON Convert Prometheus and OpenMetrics text format parser

Usage (cli):

    $ curl -s http://localhost:9100/metrics | jc --prometheus

or

    $ cat metrics.txt | jc --prometheus

Usage (module):

    import jc
    result = jc.parse('prometheus', prometheus_metrics_text)

Schema:

    [
      {
        "name":                     string,
        "labels": {
          "<label>":                string
        },
        "value":                    string,
        "value_float":              float,
        "timestamp":                string,
        "timestamp_float":          float,
        "help":                     string,
        "type":                     string,
        "unit":                     string,
        "exemplar": {
          "labels": {
            "<label>":              string
          },
          "value":                  string,
          "value_float":            float,
          "timestamp":              string,
          "timestamp_float":        float
        }
      }
    ]

Examples:

    $ cat metrics.txt | jc --prometheus -p
    [
      {
        "name": "http_requests_total",
        "labels": {
          "method": "post",
          "code": "200"
        },
        "value": "1027",
        "timestamp": "1395066363000",
        "help": "The total number of HTTP requests.",
        "type": "counter",
        "unit": null,
        "exemplar": null,
        "value_float": 1027.0,
        "timestamp_float": 1395066363000.0
      },
      {
        "name": "something_weird",
        "labels": {
          "problem": "division by zero"
        },
        "value": "+Inf",
        "timestamp": "-3982045",
        "help": null,
        "type": null,
        "unit": null,
        "exemplar": null,
        "value_float": null,
        "timestamp_float": -3982045.0
      },
      {
        "name": "http_request_duration_seconds_bucket",
        "labels": {
          "le": "0.05"
        },
        "value": "24054",
        "timestamp": null,
        "help": "A histogram of the request duration.",
        "type": "histogram",
        "unit": null,
        "exemplar": null,
        "value_float": 24054.0,
        "timestamp_float": null
      },
      ...
    ]

    $ cat metrics.txt | jc --prometheus -p -r
    [
      {
        "name": "http_requests_total",
        "labels": {
          "method": "post",
          "code": "200"
        },
        "value": "1027",
        "timestamp": "1395066363000",
        "help": "The total number of HTTP requests.",
        "type": "counter",
        "unit": null,
        "exemplar": null
      },
      {
        "name": "something_weird",
        "labels": {
          "problem": "division by zero"
        },
        "value": "+Inf",
        "timestamp": "-3982045",
        "help": null,
        "type": null,
        "unit": null,
        "exemplar": null
      },
      {
        "name": "http_request_duration_seconds_bucket",
        "labels": {
          "le": "0.05"
        },
        "value": "24054",
        "timestamp": null,
        "help": "A histogram of the request duration.",
        "type": "histogram",
        "unit": null,
        "exemplar": null
      },
      ...
    ]

<a id="jc.parsers.prometheus.parse"></a>

### parse

```python
def parse(data: str,
          raw: bool = False,
          quiet: bool = False) -> List[Dict[str, Any]]
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) unprocessed output if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    List of Dictionaries. Raw or processed structured data.

### Parser Information
Compatibility:  linux, darwin, cygwin, win32, aix, freebsd

Source: [`jc/parsers/prometheus.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/prometheus.py)

Version 1.0 by chensimian (chensimian@users.noreply.github.com)
