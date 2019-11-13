# jc.parsers.route
jc - JSON CLI output utility route Parser

Usage:
    specify --route as the first argument if the piped input is coming from route

Examples:

    $ route -ee | jc --route -p
    [
      {
        "destination": "default",
        "gateway": "gateway",
        "genmask": "0.0.0.0",
        "flags": "UG",
        "metric": 100,
        "ref": 0,
        "use": 0,
        "iface": "ens33",
        "mss": 0,
        "window": 0,
        "irtt": 0
      },
      {
        "destination": "172.17.0.0",
        "gateway": "0.0.0.0",
        "genmask": "255.255.0.0",
        "flags": "U",
        "metric": 0,
        "ref": 0,
        "use": 0,
        "iface": "docker",
        "mss": 0,
        "window": 0,
        "irtt": 0
      },
      {
        "destination": "192.168.71.0",
        "gateway": "0.0.0.0",
        "genmask": "255.255.255.0",
        "flags": "U",
        "metric": 100,
        "ref": 0,
        "use": 0,
        "iface": "ens33",
        "mss": 0,
        "window": 0,
        "irtt": 0
      }
    ]

    $ route -ee | jc --route -p -r
    [
      {
        "destination": "default",
        "gateway": "gateway",
        "genmask": "0.0.0.0",
        "flags": "UG",
        "metric": "100",
        "ref": "0",
        "use": "0",
        "iface": "ens33",
        "mss": "0",
        "window": "0",
        "irtt": "0"
      },
      {
        "destination": "172.17.0.0",
        "gateway": "0.0.0.0",
        "genmask": "255.255.0.0",
        "flags": "U",
        "metric": "0",
        "ref": "0",
        "use": "0",
        "iface": "docker",
        "mss": "0",
        "window": "0",
        "irtt": "0"
      },
      {
        "destination": "192.168.71.0",
        "gateway": "0.0.0.0",
        "genmask": "255.255.255.0",
        "flags": "U",
        "metric": "100",
        "ref": "0",
        "use": "0",
        "iface": "ens33",
        "mss": "0",
        "window": "0",
        "irtt": "0"
      }
    ]

## process
```python
process(proc_data)
```

Final processing to conform to the schema.

Parameters:

    proc_data:   (dictionary) raw structured data to process

Returns:

    dictionary   structured data with the following schema:

    [
      {
        "destination":  string,
        "gateway":      string,
        "genmask":      string,
        "flags":        string,
        "metric":       integer,
        "ref":          integer,
        "use":          integer,
        "mss":          integer,
        "window":       integer,
        "irtt":         integer,
        "iface":        string
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

    dictionary   raw or processed structured data

