[Home](https://kellyjonbrazil.github.io/jc/)
# Table of Contents

* [jc.parsers.traceroute](#jc.parsers.traceroute)
  * [\_\_version\_\_](#jc.parsers.traceroute.__version__)
  * [\_Hop](#jc.parsers.traceroute._Hop)
    * [add\_probe](#jc.parsers.traceroute._Hop.add_probe)
  * [parse](#jc.parsers.traceroute.parse)

<a id="jc.parsers.traceroute"></a>

# jc.parsers.traceroute

jc - JSON CLI output utility `traceroute` command output parser

Supports `traceroute` and `traceroute6` output.

Note: On some operating systems you will need to redirect `STDERR` to
      `STDOUT` for destination info since the header line is sent to
      `STDERR`. A warning message will be printed to `STDERR` if the
      header row is not found.

      e.g. `$ traceroute 8.8.8.8 2>&1 | jc --traceroute`

Usage (cli):

    $ traceroute 1.2.3.4 | jc --traceroute

    or

    $ jc traceroute 1.2.3.4

Usage (module):

    import jc
    result = jc.parse('traceroute', traceroute_command_output)

    or

    import jc.parsers.traceroute
    result = jc.parsers.traceroute.parse(traceroute_command_output)

Schema:

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

<a id="jc.parsers.traceroute.__version__"></a>

### \_\_version\_\_

Copyright (C) 2015 Luis Benitez

Parses the output of a traceroute execution into an AST (Abstract Syntax Tree).

The MIT License (MIT)

Copyright (c) 2014 Luis Benitez

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

<a id="jc.parsers.traceroute._Hop"></a>

## \_Hop Objects

```python
class _Hop(object)
```

<a id="jc.parsers.traceroute._Hop.add_probe"></a>

### add\_probe

```python
def add_probe(probe)
```

Adds a Probe instance to this hop's results.

<a id="jc.parsers.traceroute.parse"></a>

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

Version 1.4 by Kelly Brazil (kellyjonbrazil@gmail.com)
