[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.nsd_control"></a>

# jc.parsers.nsd_control

jc - JSON Convert `nsd-control` command output parser

Usage (cli):

    $ nsd-control | jc --nsd-control

or

    $ jc nsd-control

Usage (module):

    import jc
    result = jc.parse('nsd_control', nsd_control_command_output)

Schema:

    [
      {
        "version":              string,
        "verbosity":            integer,
        "ratelimit":            integer
      }
    ]

    [
      {
        "zone":                 string
        "status": {
          "state":              string,
          "pattern":            string,  # Additional
          "catalog-member-id":  string,  # Additional
          "served-serial":      string,
          "commit-serial":      string,
          "notified-serial":    string,  # Conditional
          "wait":               string,
          "transfer":           string	 # Conditional
        }
      }
    ]

Examples:

    $ nsd-control | jc --nsd-control status
    [
      {
        "version": "4.6.2",
        "verbosity": "2",
        "ratelimit": "0"
      }
    ]

    $ nsd-control | jc --nsd-control zonestatus sunet.se
    [
      {
        "zone": "sunet.se",
        "status": {
          "state": "ok",
          "served-serial": "2023090704 since 2023-09-07T16:34:27",
          "commit-serial": "2023090704 since 2023-09-07T16:34:27",
          "wait": "28684 sec between attempts"
        }
      }
    ]

<a id="jc.parsers.nsd_control.parse"></a>

### parse

```python
def parse(data: str, raw: bool = False, quiet: bool = False)
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

Source: [`jc/parsers/nsd_control.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/nsd_control.py)

Version 1.2 by Pettai (pettai@sunet.se)
