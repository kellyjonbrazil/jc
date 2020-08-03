
# jc.parsers.route
jc - JSON CLI output utility route Parser

Usage:

    specify --route as the first argument if the piped input is coming from route

Compatibility:

    'linux'

Examples:

    $ route -ee | jc --route -p
    [
      {
        "destination": "default",
        "gateway": "_gateway",
        "genmask": "0.0.0.0",
        "flags": "UG",
        "metric": 202,
        "ref": 0,
        "use": 0,
        "iface": "ens33",
        "mss": 0,
        "window": 0,
        "irtt": 0,
        "flags_pretty": [
          "UP",
          "GATEWAY"
        ]
      },
      {
        "destination": "192.168.71.0",
        "gateway": "0.0.0.0",
        "genmask": "255.255.255.0",
        "flags": "U",
        "metric": 202,
        "ref": 0,
        "use": 0,
        "iface": "ens33",
        "mss": 0,
        "window": 0,
        "irtt": 0,
        "flags_pretty": [
          "UP"
        ]
      }
    ]


    $ route -ee | jc --route -p -r
    [
      {
        "destination": "default",
        "gateway": "_gateway",
        "genmask": "0.0.0.0",
        "flags": "UG",
        "metric": "202",
        "ref": "0",
        "use": "0",
        "iface": "ens33",
        "mss": "0",
        "window": "0",
        "irtt": "0"
      },
      {
        "destination": "192.168.71.0",
        "gateway": "0.0.0.0",
        "genmask": "255.255.255.0",
        "flags": "U",
        "metric": "202",
        "ref": "0",
        "use": "0",
        "iface": "ens33",
        "mss": "0",
        "window": "0",
        "irtt": "0"
      }
    ]



## info
```python
info()
```


## process
```python
process(proc_data)
```

Final processing to conform to the schema.

Parameters:

    proc_data:   (dictionary) raw structured data to process

Returns:

    List of dictionaries. Structured data with the following schema:

    [
      {
        "destination":     string,
        "gateway":         string,
        "genmask":         string,
        "flags":           string,
        "flags_pretty": [
                           string,
        ]
        "metric":          integer,
        "ref":             integer,
        "use":             integer,
        "mss":             integer,
        "window":          integer,
        "irtt":            integer,
        "iface":           string
      }
    ]


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

    List of dictionaries. Raw or processed structured data.

