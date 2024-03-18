[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.openvpn"></a>

# jc.parsers.openvpn

jc - JSON Convert openvpn-status.log file parser

The `*_epoch` calculated timestamp fields are naive. (i.e. based on
the local time of the system the parser is run on)

Usage (cli):

    $ cat openvpn-status.log | jc --openvpn

Usage (module):

    import jc
    result = jc.parse('openvpn', openvpn_status_log_file_output)

Schema:

    {
      "clients": [
        {
          "common_name":                        string,
          "real_address":                       string,
          "real_address_prefix":                integer,  # [0]
          "real_address_port":                  integer,  # [0]
          "bytes_received":                     integer,
          "bytes_sent":                         integer,
          "connected_since":                    string,
          "connected_since_epoch":              integer,
          "updated":                            string,
          "updated_epoch":                      integer,
        }
      ],
      "routing_table": [
        {
          "virtual_address":                    string,
          "virtual_address_prefix":             integer,  # [0]
          "virtual_address_port":               integer,  # [0]
          "common_name":                        string,
          "real_address":                       string,
          "real_address_prefix":                integer,  # [0]
          "real_address_port":                  integer,  # [0]
          "last_reference":                     string,
          "last_reference_epoch":               integer,
        }
      ],
      "global_stats": {
        "max_bcast_mcast_queue_len":            integer
      }
    }

    [0] null/None if not found

Examples:

    $ cat openvpn-status.log | jc --openvpn -p
    {
      "clients": [
        {
          "common_name": "foo@example.com",
          "real_address": "10.10.10.10",
          "bytes_received": 334948,
          "bytes_sent": 1973012,
          "connected_since": "Thu Jun 18 04:23:03 2015",
          "updated": "Thu Jun 18 08:12:15 2015",
          "real_address_prefix": null,
          "real_address_port": 49502,
          "connected_since_epoch": 1434626583,
          "updated_epoch": 1434640335
        },
        {
          "common_name": "foo@example.com",
          "real_address": "10.10.10.10",
          "bytes_received": 334948,
          "bytes_sent": 1973012,
          "connected_since": "Thu Jun 18 04:23:03 2015",
          "updated": "Thu Jun 18 08:12:15 2015",
          "real_address_prefix": null,
          "real_address_port": 49503,
          "connected_since_epoch": 1434626583,
          "updated_epoch": 1434640335
        }
      ],
      "routing_table": [
        {
          "virtual_address": "192.168.255.118",
          "common_name": "baz@example.com",
          "real_address": "10.10.10.10",
          "last_reference": "Thu Jun 18 08:12:09 2015",
          "virtual_address_prefix": null,
          "virtual_address_port": null,
          "real_address_prefix": null,
          "real_address_port": 63414,
          "last_reference_epoch": 1434640329
        },
        {
          "virtual_address": "10.200.0.0",
          "common_name": "baz@example.com",
          "real_address": "10.10.10.10",
          "last_reference": "Thu Jun 18 08:12:09 2015",
          "virtual_address_prefix": 16,
          "virtual_address_port": null,
          "real_address_prefix": null,
          "real_address_port": 63414,
          "last_reference_epoch": 1434640329
        }
      ],
      "global_stats": {
        "max_bcast_mcast_queue_len": 0
      }
    }

    $ cat openvpn-status.log | jc --openvpn -p -r
    {
      "clients": [
        {
          "common_name": "foo@example.com",
          "real_address": "10.10.10.10:49502",
          "bytes_received": "334948",
          "bytes_sent": "1973012",
          "connected_since": "Thu Jun 18 04:23:03 2015",
          "updated": "Thu Jun 18 08:12:15 2015"
        },
        {
          "common_name": "foo@example.com",
          "real_address": "10.10.10.10:49503",
          "bytes_received": "334948",
          "bytes_sent": "1973012",
          "connected_since": "Thu Jun 18 04:23:03 2015",
          "updated": "Thu Jun 18 08:12:15 2015"
        }
      ],
      "routing_table": [
        {
          "virtual_address": "192.168.255.118",
          "common_name": "baz@example.com",
          "real_address": "10.10.10.10:63414",
          "last_reference": "Thu Jun 18 08:12:09 2015"
        },
        {
          "virtual_address": "10.200.0.0/16",
          "common_name": "baz@example.com",
          "real_address": "10.10.10.10:63414",
          "last_reference": "Thu Jun 18 08:12:09 2015"
        }
      ],
      "global_stats": {
        "max_bcast_mcast_queue_len": "0"
      }
    }

<a id="jc.parsers.openvpn.parse"></a>

### parse

```python
def parse(data: str, raw: bool = False, quiet: bool = False) -> Dict[str, Any]
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) unprocessed output if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    Dictionary. Raw or processed structured data.

### Parser Information
Compatibility:  linux, darwin, cygwin, win32, aix, freebsd

Source: [`jc/parsers/openvpn.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/openvpn.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
