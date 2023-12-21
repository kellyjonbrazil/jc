[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.ufw"></a>

# jc.parsers.ufw

jc - JSON Convert `ufw status` command output parser

Usage (cli):

    $ ufw status | jc --ufw

or

    $ jc ufw status

Usage (module):

    import jc
    result = jc.parse('ufw', ufw_command_output)

Schema:

    {
      "status":                     string,
      "logging":                    string,
      "logging_level":              string,
      "default":                    string,
      "new_profiles":               string,
      "rules": [
        {
          "action":                 string,
          "action_direction":       string,     # null if blank
          "index":                  integer,    # null if blank
          "network_protocol":       string,
          "to_ip":                  string,
          "to_ip_prefix":           integer,
          "to_interface":           string,
          "to_transport":           string,
          "to_ports": [
                                    integer
          ],
          "to_port_ranges": [
            {
              "start":              integer,
              "end":                integer
            }
          ],
          "to_service":             string,     # [0]
          "from_ip":                string,
          "from_ip_prefix":         integer,
          "from_interface":         string,
          "from_transport":         string,
          "from_ports": [
                                    integer
          ],
          "from_port_ranges": [
            {
              "start":              integer,
              "end":                integer
            }
          ],
          "from_service":           string,     # [1]
          "comment":                string      # null if no comment
        }
      ]
    }

    [0] null if any 'to' ports or port_ranges are set
    [1] null if any 'from' ports or port_ranges are set

Examples:

    $ ufw status verbose | jc --ufw -p
    {
      "status": "active",
      "logging": "on",
      "logging_level": "low",
      "default": "deny (incoming), allow (outgoing), disabled (routed)",
      "new_profiles": "skip",
      "rules": [
        {
          "action": "ALLOW",
          "action_direction": "IN",
          "index": null,
          "network_protocol": "ipv4",
          "to_interface": "any",
          "to_transport": "any",
          "to_service": null,
          "to_ports": [
            22
          ],
          "to_ip": "0.0.0.0",
          "to_ip_prefix": 0,
          "comment": null,
          "from_ip": "0.0.0.0",
          "from_ip_prefix": 0,
          "from_interface": "any",
          "from_transport": "any",
          "from_port_ranges": [
            {
              "start": 0,
              "end": 65535
            }
          ],
          "from_service": null
        },
        {
          "action": "ALLOW",
          "action_direction": "IN",
          "index": null,
          "network_protocol": "ipv4",
          "to_interface": "any",
          "to_transport": "tcp",
          "to_service": null,
          "to_ports": [
            80,
            443
          ],
          "to_ip": "0.0.0.0",
          "to_ip_prefix": 0,
          "comment": null,
          "from_ip": "0.0.0.0",
          "from_ip_prefix": 0,
          "from_interface": "any",
          "from_transport": "any",
          "from_port_ranges": [
            {
              "start": 0,
              "end": 65535
            }
          ],
          "from_service": null
        },
        ...
      ]
    }

    $ ufw status verbose | jc --ufw -p -r
    {
      "status": "active",
      "logging": "on",
      "logging_level": "low",
      "default": "deny (incoming), allow (outgoing), disabled (routed)",
      "new_profiles": "skip",
      "rules": [
        {
          "action": "ALLOW",
          "action_direction": "IN",
          "index": null,
          "network_protocol": "ipv4",
          "to_interface": "any",
          "to_transport": "any",
          "to_service": null,
          "to_ports": [
            "22"
          ],
          "to_ip": "0.0.0.0",
          "to_ip_prefix": "0",
          "comment": null,
          "from_ip": "0.0.0.0",
          "from_ip_prefix": "0",
          "from_interface": "any",
          "from_transport": "any",
          "from_port_ranges": [
            {
              "start": "0",
              "end": "65535"
            }
          ],
          "from_service": null
        },
        {
          "action": "ALLOW",
          "action_direction": "IN",
          "index": null,
          "network_protocol": "ipv4",
          "to_interface": "any",
          "to_transport": "tcp",
          "to_service": null,
          "to_ports": [
            "80",
            "443"
          ],
          "to_ip": "0.0.0.0",
          "to_ip_prefix": "0",
          "comment": null,
          "from_ip": "0.0.0.0",
          "from_ip_prefix": "0",
          "from_interface": "any",
          "from_transport": "any",
          "from_port_ranges": [
            {
              "start": "0",
              "end": "65535"
            }
          ],
          "from_service": null
        },
        ...
      ]
    }

<a id="jc.parsers.ufw.parse"></a>

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
Compatibility:  linux

Source: [`jc/parsers/ufw.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/ufw.py)

Version 1.2 by Kelly Brazil (kellyjonbrazil@gmail.com)
