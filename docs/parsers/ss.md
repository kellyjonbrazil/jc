# jc.parsers.ss
jc - JSON CLI output utility ss Parser

Usage:
    specify --ss as the first argument if the piped input is coming from ss

Examples:

      $ sudo ss -a | jc --ss -p
      [
        {
          "netid": "nl",
          "state": "UNCONN",
          "recv_q": 0,
          "send_q": 0,
          "local_address": "rtnl",
          "local_port": "kernel",
          "peer_address": "*"
        },
        {
          "netid": "nl",
          "state": "UNCONN",
          "recv_q": 0,
          "send_q": 0,
          "local_address": "rtnl",
          "local_port": "systemd-resolve/893",
          "peer_address": "*"
        },
        {
          "netid": "nl",
          "state": "UNCONN",
          "recv_q": 0,
          "send_q": 0,
          "local_address": "rtnl",
          "local_port": "systemd/1",
          "peer_address": "*"
        },
        ...
        {
          "netid": "tcp",
          "state": "LISTEN",
          "recv_q": 0,
          "send_q": 128,
          "local_address": "127.0.0.1",
          "local_port": "35485",
          "peer_address": "0.0.0.0",
          "peer_port": "*",
          "interface": "lo"
        },
        {
          "netid": "tcp",
          "state": "LISTEN",
          "recv_q": 0,
          "send_q": 128,
          "local_address": "[::]",
          "local_port": "ssh",
          "peer_address": "[::]",
          "peer_port": "*"
        },
        {
          "netid": "v_str",
          "state": "ESTAB",
          "recv_q": 0,
          "send_q": 0,
          "local_address": "999900439",
          "local_port": "1023",
          "peer_address": "0",
          "peer_port": "976",
          "local_port_num": 1023,
          "peer_port_num": 976
        }
      ]

      $ sudo ss -a | jc --ss -p -r
      [
        {
          "netid": "nl",
          "state": "UNCONN",
          "recv_q": "0",
          "send_q": "0",
          "local_address": "rtnl",
          "local_port": "kernel",
          "peer_address": "*"
        },
        {
          "netid": "nl",
          "state": "UNCONN",
          "recv_q": "0",
          "send_q": "0",
          "local_address": "rtnl",
          "local_port": "systemd-resolve/893",
          "peer_address": "*"
        },
        {
          "netid": "nl",
          "state": "UNCONN",
          "recv_q": "0",
          "send_q": "0",
          "local_address": "rtnl",
          "local_port": "systemd/1",
          "peer_address": "*"
        },
        ...
        {
          "netid": "tcp",
          "state": "LISTEN",
          "recv_q": "0",
          "send_q": "128",
          "local_address": "127.0.0.1",
          "local_port": "35485",
          "peer_address": "0.0.0.0",
          "peer_port": "*",
          "interface": "lo"
        },
        {
          "netid": "tcp",
          "state": "LISTEN",
          "recv_q": "0",
          "send_q": "128",
          "local_address": "[::]",
          "local_port": "ssh",
          "peer_address": "[::]",
          "peer_port": "*"
        },
        {
          "netid": "v_str",
          "state": "ESTAB",
          "recv_q": "0",
          "send_q": "0",
          "local_address": "999900439",
          "local_port": "1023",
          "peer_address": "0",
          "peer_port": "976"
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
        "netid":            string,
        "state":            string,
        "recv_q":           integer,
        "send_q":           integer,
        "local_address":    string,
        "local_port":       string,
        "local_port_num":   integer,
        "peer_address":     string,
        "peer_port":        string,
        "peer_port_num":    integer,
        "interface":        string
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

