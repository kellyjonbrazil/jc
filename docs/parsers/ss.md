
# jc.parsers.ss
jc - JSON CLI output utility ss Parser

Usage:

    specify --ss as the first argument if the piped input is coming from ss

Limitations:

    Extended information options like -e and -p are not supported and may cause parsing irregularities

Compatibility:

    'linux'

Examples:

      $ sudo ss -a | jc --ss -p
      [
        {
          "netid": "nl",
          "state": "UNCONN",
          "recv_q": 0,
          "send_q": 0,
          "peer_address": "*",
          "channel": "rtnl:kernel"
        },
        {
          "netid": "nl",
          "state": "UNCONN",
          "recv_q": 0,
          "send_q": 0,
          "peer_address": "*",
          "pid": 893,
          "channel": "rtnl:systemd-resolve"
        },
        ...
        {
          "netid": "p_raw",
          "state": "UNCONN",
          "recv_q": 0,
          "send_q": 0,
          "peer_address": "*",
          "link_layer": "LLDP",
          "interface": "ens33"
        },
        {
          "netid": "u_dgr",
          "state": "UNCONN",
          "recv_q": 0,
          "send_q": 0,
          "local_port": "93066",
          "peer_address": "*",
          "peer_port": "0",
          "path": "/run/user/1000/systemd/notify"
        },
        {
          "netid": "u_seq",
          "state": "LISTEN",
          "recv_q": 0,
          "send_q": 128,
          "local_port": "20699",
          "peer_address": "*",
          "peer_port": "0",
          "path": "/run/udev/control"
        },
        ...
        {
          "netid": "icmp6",
          "state": "UNCONN",
          "recv_q": 0,
          "send_q": 0,
          "local_address": "*",
          "local_port": "ipv6-icmp",
          "peer_address": "*",
          "peer_port": "*",
          "interface": "ens33"
        },
        {
          "netid": "udp",
          "state": "UNCONN",
          "recv_q": 0,
          "send_q": 0,
          "local_address": "127.0.0.53",
          "local_port": "domain",
          "peer_address": "0.0.0.0",
          "peer_port": "*",
          "interface": "lo"
        },
        {
          "netid": "tcp",
          "state": "LISTEN",
          "recv_q": 0,
          "send_q": 128,
          "local_address": "127.0.0.53",
          "local_port": "domain",
          "peer_address": "0.0.0.0",
          "peer_port": "*",
          "interface": "lo"
        },
        {
          "netid": "tcp",
          "state": "LISTEN",
          "recv_q": 0,
          "send_q": 128,
          "local_address": "0.0.0.0",
          "local_port": "ssh",
          "peer_address": "0.0.0.0",
          "peer_port": "*"
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
          "peer_address": "*",
          "channel": "rtnl:kernel"
        },
        {
          "netid": "nl",
          "state": "UNCONN",
          "recv_q": "0",
          "send_q": "0",
          "peer_address": "*",
          "pid": "893",
          "channel": "rtnl:systemd-resolve"
        },
        ...
        {
          "netid": "p_raw",
          "state": "UNCONN",
          "recv_q": "0",
          "send_q": "0",
          "peer_address": "*",
          "link_layer": "LLDP",
          "interface": "ens33"
        },
        {
          "netid": "u_dgr",
          "state": "UNCONN",
          "recv_q": "0",
          "send_q": "0",
          "local_port": "93066",
          "peer_address": "*",
          "peer_port": "0",
          "path": "/run/user/1000/systemd/notify"
        },
        {
          "netid": "u_seq",
          "state": "LISTEN",
          "recv_q": "0",
          "send_q": "128",
          "local_port": "20699",
          "peer_address": "*",
          "peer_port": "0",
          "path": "/run/udev/control"
        },
        ...
        {
          "netid": "icmp6",
          "state": "UNCONN",
          "recv_q": "0",
          "send_q": "0",
          "local_address": "*",
          "local_port": "ipv6-icmp",
          "peer_address": "*",
          "peer_port": "*",
          "interface": "ens33"
        },
        {
          "netid": "udp",
          "state": "UNCONN",
          "recv_q": "0",
          "send_q": "0",
          "local_address": "127.0.0.53",
          "local_port": "domain",
          "peer_address": "0.0.0.0",
          "peer_port": "*",
          "interface": "lo"
        },
        {
          "netid": "tcp",
          "state": "LISTEN",
          "recv_q": "0",
          "send_q": "128",
          "local_address": "127.0.0.53",
          "local_port": "domain",
          "peer_address": "0.0.0.0",
          "peer_port": "*",
          "interface": "lo"
        },
        {
          "netid": "tcp",
          "state": "LISTEN",
          "recv_q": "0",
          "send_q": "128",
          "local_address": "0.0.0.0",
          "local_port": "ssh",
          "peer_address": "0.0.0.0",
          "peer_port": "*"
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
        "interface":        string,
        "link_layer"        string,
        "channel":          string,
        "path":             string,
        "pid":              integer
      }
    ]

    Information from https://www.cyberciti.biz/files/ss.html used to define field names


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

