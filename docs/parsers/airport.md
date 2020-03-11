# jc.parsers.airport
jc - JSON CLI output utility airport -I Parser

Usage:

    specify --airport as the first argument if the piped input is coming from airport -I (OSX)

    This program can be found at:
    /System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport

Compatibility:

    'darwin'

Examples:

    $ airport -I | jc --airport -p
    {
      "agrctlrssi": -66,
      "agrextrssi": 0,
      "agrctlnoise": -90,
      "agrextnoise": 0,
      "state": "running",
      "op_mode": "station",
      "lasttxrate": 195,
      "maxrate": 867,
      "lastassocstatus": 0,
      "802_11_auth": "open",
      "link_auth": "wpa2-psk",
      "bssid": "3c:37:86:15:ad:f9",
      "ssid": "SnazzleDazzle",
      "mcs": 0,
      "channel": "48,80"
    }

    $ airport -I | jc --airport -p -r
    {
      "agrctlrssi": "-66",
      "agrextrssi": "0",
      "agrctlnoise": "-90",
      "agrextnoise": "0",
      "state": "running",
      "op_mode": "station",
      "lasttxrate": "195",
      "maxrate": "867",
      "lastassocstatus": "0",
      "802_11_auth": "open",
      "link_auth": "wpa2-psk",
      "bssid": "3c:37:86:15:ad:f9",
      "ssid": "SnazzleDazzle",
      "mcs": "0",
      "channel": "48,80"
    }

## info
```python
info(self, /, *args, **kwargs)
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
      "agrctlrssi":        integer,
      "agrextrssi":        integer,
      "agrctlnoise":       integer,
      "agrextnoise":       integer,
      "state":             string,
      "op_mode":           string,
      "lasttxrate":        integer,
      "maxrate":           integer,
      "lastassocstatus":   integer,
      "802_11_auth":       string,
      "link_auth":         string,
      "bssid":             string,
      "ssid":              string,
      "mcs":               integer,
      "channel":           string
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

