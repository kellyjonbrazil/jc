[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.iftop"></a>

# jc.parsers.iftop

jc - JSON Convert `iftop` command output parser

Usage (cli):

    $ iftop -i <device> -t -B -s1 | jc --iftop

Usage (module):

    import jc
    result = jc.parse('iftop', iftop_command_output)

Schema:

    [
      {
        "device":                   string,
        "ip_address":               string,
        "mac_address":              string,
        "clients": [
          {
            "index":                integer,
            "connections": [
              {
                "host_name":        string,
                "host_port":        string,   # can be service or missing
                "last_2s":          integer,
                "last_10s":         integer,
                "last_40s":         integer,
                "cumulative":       integer,
                "direction":        string
              }
            ]
          }
        ]
        "total_send_rate": {
          "last_2s":                integer,
          "last_10s":               integer,
          "last_40s":               integer
        }
        "total_receive_rate": {
          "last_2s":                integer,
          "last_10s":               integer,
          "last_40s":               integer
        }
        "total_send_and_receive_rate": {
          "last_2s":                integer,
          "last_10s":               integer,
          "last_40s":               integer
        }
        "peak_rate": {
          "last_2s":                integer,
          "last_10s":               integer,
          "last_40s":               integer
        }
        "cumulative_rate": {
          "last_2s":                integer,
          "last_10s":               integer,
          "last_40s":               integer
        }
      }
    ]

Examples:

    $ iftop -i enp0s3 -t -P -s1 | jc --iftop -p
    [
      {
        "device": "enp0s3",
        "ip_address": "10.10.15.129",
        "mac_address": "08:00:27:c0:4a:4f",
        "clients": [
          {
            "index": 1,
            "connections": [
              {
                "host_name": "ubuntu-2004-clean-01",
                "host_port": "ssh",
                "last_2s": 448,
                "last_10s": 448,
                "last_40s": 448,
                "cumulative": 112,
                "direction": "send"
              },
              {
                "host_name": "10.10.15.72",
                "host_port": "40876",
                "last_2s": 208,
                "last_10s": 208,
                "last_40s": 208,
                "cumulative": 52,
                "direction": "receive"
              }
            ]
          }
        ],
        "total_send_rate": {
          "last_2s": 448,
          "last_10s": 448,
          "last_40s": 448
        },
        "total_receive_rate": {
          "last_2s": 208,
          "last_10s": 208,
          "last_40s": 208
        },
        "total_send_and_receive_rate": {
          "last_2s": 656,
          "last_10s": 656,
          "last_40s": 656
        },
        "peak_rate": {
          "last_2s": 448,
          "last_10s": 208,
          "last_40s": 656
        },
        "cumulative_rate": {
          "last_2s": 112,
          "last_10s": 52,
          "last_40s": 164
        }
      }
    ]

    $ iftop -i enp0s3 -t -P -s1 | jc --iftop -p -r
    [
      {
        "device": "enp0s3",
        "ip_address": "10.10.15.129",
        "mac_address": "11:22:33:44:55:66",
        "clients": [
          {
            "index": 1,
            "connections": [
              {
                "host_name": "ubuntu-2004-clean-01",
                "host_port": "ssh",
                "last_2s": "448b",
                "last_10s": "448b",
                "last_40s": "448b",
                "cumulative": "112B",
                "direction": "send"
              },
              {
                "host_name": "10.10.15.72",
                "host_port": "40876",
                "last_2s": "208b",
                "last_10s": "208b",
                "last_40s": "208b",
                "cumulative": "52B",
                "direction": "receive"
              }
            ]
          }
        ],
        "total_send_rate": {
          "last_2s": "448b",
          "last_10s": "448b",
          "last_40s": "448b"
        },
        "total_receive_rate": {
          "last_2s": "208b",
          "last_10s": "208b",
          "last_40s": "208b"
        },
        "total_send_and_receive_rate": {
          "last_2s": "656b",
          "last_10s": "656b",
          "last_40s": "656b"
        },
        "peak_rate": {
          "last_2s": "448b",
          "last_10s": "208b",
          "last_40s": "656b"
        },
        "cumulative_rate": {
          "last_2s": "112B",
          "last_10s": "52B",
          "last_40s": "164B"
        }
      }
    ]

<a id="jc.parsers.iftop.parse"></a>

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
Compatibility:  linux

Source: [`jc/parsers/iftop.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/iftop.py)

Version 1.1 by Ron Green (11993626+georgettica@users.noreply.github.com)
