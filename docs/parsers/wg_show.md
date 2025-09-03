[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.wg_show"></a>

# jc.parsers.wg_show

jc - JSON Convert `wg show` command output parser

Parses the output of the `wg show all dump` command, providing structured JSON output for easy integration and analysis.

Usage (cli):

    $ wg show all dump | jc --wg-show

or

    $ jc wg show all dump

Usage (module):

    import jc
    result = jc.parse('wg-show', wg_command_output)

Schema:

    [
      {
        "device":                       string,
        "private_key":                  string,
        "public_key":                   string,
        "listen_port":                  integer,
        "fwmark":                       integer,
        "peers": [
          {
            "public_key":               string,
            "preshared_key":            string,
            "endpoint":                 string,
            "latest_handshake":         integer,
            "transfer_rx":              integer,
            "transfer_sx":              integer,
            "persistent_keepalive":     integer,
            "allowed_ips": [
                                        string
            ]
          }
        ]
      }
    ]

Examples:

    $ wg show all dump | jc --wg-show -p
    [
      {
        "device": "wg0",
        "private_key": "aEbVdvHSEp3oofHDNVCsUoaRSxk1Og8/pTLof5yF+1M=",
        "public_key": "OIxbQszw1chdO5uigAxpsl4fc/h04yMYafl72gUbakM=",
        "listen_port": 51820,
        "fwmark": null,
        "peers": [
          {
            "public_key": "sQFGAhSdx0aC7DmTFojzBOW8Ccjv1XV5+N9FnkZu5zc=",
            "preshared_key": null,
            "endpoint": "79.134.136.199:40036",
            "latest_handshake": 1728809756,
            "transfer_rx": 1378724,
            "transfer_sx": 406524,
            "persistent_keepalive": null,
            "allowed_ips": ["10.10.0.2/32"]
          },
          {
            "public_key": "B9csmpvrv4Q7gpjc6zAbNNO8hIOYfpBqxmik2aNpwwE=",
            "preshared_key": null,
            "endpoint": "79.134.136.199:35946",
            "latest_handshake": 1728809756,
            "transfer_rx": 4884248,
            "transfer_sx": 3544596,
            "persistent_keepalive": null,
            "allowed_ips": ["10.10.0.3/32"]
          },
          {
            "public_key": "miiSYR5UdevREhlWpmnci+vv/dEGLHbNtKu7u1CuOD4=",
            "preshared_key": null,
            "allowed_ips": ["10.10.0.4/32"]
          },
          {
            "public_key": "gx9+JHLHJvOfBNjTmZ8KQAnThFFiZMQrX1kRaYcIYzw=",
            "preshared_key": null,
            "endpoint": "173.244.225.194:45014",
            "latest_handshake": 1728809827,
            "transfer_rx": 1363652,
            "transfer_sx": 458252,
            "persistent_keepalive": null,
            "allowed_ips": ["10.10.0.5/32"]
          }
        ]
      }
    ]

    $ wg show all dump | jc --wg-show -p -r
    [
      {
        "device": "wg0",
        "private_key": "aEbVdvHSEp3oofHDNVCsUoaRSxk1Og8/pTLof5yF+1M=",
        "public_key": "OIxbQszw1chdO5uigAxpsl4fc/h04yMYafl72gUbakM=",
        "listen_port": 51820,
        "fwmark": null,
        "peers": {
          "sQFGAhSdx0aC7DmTFojzBOW8Ccjv1XV5+N9FnkZu5zc=": {
            "preshared_key": null,
            "endpoint": "79.134.136.199:40036",
            "latest_handshake": 1728809756,
            "transfer_rx": 1378724,
            "transfer_sx": 406524,
            "persistent_keepalive": -1,
            "allowed_ips": ["10.10.0.2/32"]
          },
          "B9csmpvrv4Q7gpjc6zAbNNO8hIOYfpBqxmik2aNpwwE=": {
            "preshared_key": null,
            "endpoint": "79.134.136.199:35946",
            "latest_handshake": 1728809756,
            "transfer_rx": 4884248,
            "transfer_sx": 3544596,
            "persistent_keepalive": -1,
            "allowed_ips": ["10.10.0.3/32"]
          },
          "miiSYR5UdevREhlWpmnci+vv/dEGLHbNtKu7u1CuOD4=": {
            "preshared_key": null,
            "allowed_ips": ["10.10.0.4/32"]
          },
          "gx9+JHLHJvOfBNjTmZ8KQAnThFFiZMQrX1kRaYcIYzw=": {
            "preshared_key": null,
            "endpoint": "173.244.225.194:45014",
            "latest_handshake": 1728809827,
            "transfer_rx": 1363652,
            "transfer_sx": 458252,
            "persistent_keepalive": -1,
            "allowed_ips": ["10.10.0.5/32"]
          }
        }
      }
    ]

<a id="jc.parsers.wg_show.parse"></a>

### parse

```python
def parse(data: str,
          raw: bool = False,
          quiet: bool = False) -> List[Dict[str, Any]]
```

Main text parsing function.

Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

Parameters:

    data:        (str)  Text data to parse, typically the output from `wg show all dump`
    raw:         (bool) If True, returns unprocessed output
    quiet:       (bool) Suppress warning messages if True

Returns:

    List[Dict]: Parsed data in JSON-friendly format, either raw or processed.

### Parser Information
Compatibility:  linux, darwin, cygwin, win32, aix, freebsd

Source: [`jc/parsers/wg_show.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/wg_show.py)

Version 1.0 by Hamza Saht (hamzasaht01@gmail.com)
