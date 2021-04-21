[Home](https://kellyjonbrazil.github.io/jc/)

# jc.parsers.ufw
jc - JSON CLI output utility `ufw status` command output parser

Usage (cli):

    $ ufw status | jc --ufw

    or

    $ jc ufw status

Usage (module):

    import jc.parsers.ufw
    result = jc.parsers.ufw.parse(ufw_command_output)

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
          "to_transport":           string,     # null if to_service is set
          "to_start_port":          integer,    # null if to_service is set
          "to_end_port":            integer,    # null if to_service is set
          "to_service":             string,     # null if any above are set
          "from_ip":                string,
          "from_ip_prefix":         integer,
          "from_interface":         string,
          "from_transport":         string,     # null if from_service is set
          "from_start_port":        integer,    # null if from_service is set
          "from_end_port":          integer,    # null if from_service is set
          "from_service":           string,     # null if any above are set
          "comment":                string      # null if no comment
        }
      ]
    }

Examples:

    $ ufw status verbose numbered | jc --ufw -p
    {
      "status": "active",
      "logging": "on",
      "logging_level": "low",
      "default": "deny (incoming), allow (outgoing), deny (routed)",
      "new_profiles": "skip",
      "rules": [
        {
          "action": "ALLOW",
          "action_direction": "IN",
          "index": 1,
          "network_protocol": "ipv4",
          "to_interface": "any",
          "to_transport": "tcp",
          "to_start_port": 22,
          "to_end_port": 22,
          "to_service": null,
          "to_ip": "0.0.0.0",
          "to_ip_prefix": "0",
          "comment": null,
          "from_ip": "0.0.0.0",
          "from_ip_prefix": "0",
          "from_interface": "any",
          "from_transport": "any",
          "from_start_port": 0,
          "from_end_port": 65535,
          "from_service": null
        },
        {
          "action": "ALLOW",
          "action_direction": "IN",
          "index": 2,
          "network_protocol": "ipv6",
          "to_interface": "any",
          "to_transport": "tcp",
          "to_start_port": 22,
          "to_end_port": 22,
          "to_service": null,
          "to_ip": "::",
          "to_ip_prefix": "0",
          "comment": null,
          "from_ip": "::",
          "from_ip_prefix": "0",
          "from_interface": "any",
          "from_transport": "any",
          "from_start_port": 0,
          "from_end_port": 65535,
          "from_service": null
        },
        {
          "action": "ALLOW",
          "action_direction": "IN",
          "index": 3,
          "network_protocol": "ipv4",
          "to_interface": "any",
          "to_transport": null,
          "to_service": "Apache Full",
          "to_start_port": null,
          "to_end_port": null,
          "to_ip": "0.0.0.0",
          "to_ip_prefix": "0",
          "comment": null,
          "from_ip": "0.0.0.0",
          "from_ip_prefix": "0",
          "from_interface": "any",
          "from_transport": "any",
          "from_start_port": 0,
          "from_end_port": 65535,
          "from_service": null
        },
        {
          "action": "ALLOW",
          "action_direction": "IN",
          "index": 4,
          "network_protocol": "ipv6",
          "to_interface": "any",
          "to_ip": "2405:204:7449:49fc:f09a:6f4a:bc93:1955",
          "to_ip_prefix": "128",
          "to_transport": "any",
          "to_start_port": 0,
          "to_end_port": 65535,
          "to_service": null,
          "comment": null,
          "from_ip": "::",
          "from_ip_prefix": "0",
          "from_interface": "any",
          "from_transport": "any",
          "from_start_port": 0,
          "from_end_port": 65535,
          "from_service": null
        },
        {
          "action": "ALLOW",
          "action_direction": "IN",
          "index": 5,
          "network_protocol": "ipv4",
          "to_interface": "en0",
          "to_ip": "10.10.10.10",
          "to_ip_prefix": "32",
          "to_transport": "any",
          "to_start_port": 0,
          "to_end_port": 65535,
          "to_service": null,
          "comment": null,
          "from_ip": "0.0.0.0",
          "from_ip_prefix": "0",
          "from_interface": "any",
          "from_transport": "any",
          "from_start_port": 0,
          "from_end_port": 65535,
          "from_service": null
        }
      ]
    }

    $ ufw status verbose numbered | jc --ufw -p -r
    {
      "status": "active",
      "logging": "on",
      "logging_level": "low",
      "default": "deny (incoming), allow (outgoing), deny (routed)",
      "new_profiles": "skip",
      "rules": [
        {
          "action": "ALLOW",
          "action_direction": "IN",
          "index": "1",
          "network_protocol": "ipv4",
          "to_interface": "any",
          "to_transport": "tcp",
          "to_start_port": "22",
          "to_end_port": "22",
          "to_service": null,
          "to_ip": "0.0.0.0",
          "to_ip_prefix": "0",
          "comment": null,
          "from_ip": "0.0.0.0",
          "from_ip_prefix": "0",
          "from_interface": "any",
          "from_transport": "any",
          "from_start_port": "0",
          "from_end_port": "65535",
          "from_service": null
        },
        {
          "action": "ALLOW",
          "action_direction": "IN",
          "index": "2",
          "network_protocol": "ipv6",
          "to_interface": "any",
          "to_transport": "tcp",
          "to_start_port": "22",
          "to_end_port": "22",
          "to_service": null,
          "to_ip": "::",
          "to_ip_prefix": "0",
          "comment": null,
          "from_ip": "::",
          "from_ip_prefix": "0",
          "from_interface": "any",
          "from_transport": "any",
          "from_start_port": "0",
          "from_end_port": "65535",
          "from_service": null
        },
        {
          "action": "ALLOW",
          "action_direction": "IN",
          "index": "3",
          "network_protocol": "ipv4",
          "to_interface": "any",
          "to_transport": null,
          "to_service": "Apache Full",
          "to_start_port": null,
          "to_end_port": null,
          "to_ip": "0.0.0.0",
          "to_ip_prefix": "0",
          "comment": null,
          "from_ip": "0.0.0.0",
          "from_ip_prefix": "0",
          "from_interface": "any",
          "from_transport": "any",
          "from_start_port": "0",
          "from_end_port": "65535",
          "from_service": null
        },
        {
          "action": "ALLOW",
          "action_direction": "IN",
          "index": "4",
          "network_protocol": "ipv6",
          "to_interface": "any",
          "to_ip": "2405:204:7449:49fc:f09a:6f4a:bc93:1955",
          "to_ip_prefix": "128",
          "to_transport": "any",
          "to_start_port": "0",
          "to_end_port": "65535",
          "to_service": null,
          "comment": null,
          "from_ip": "::",
          "from_ip_prefix": "0",
          "from_interface": "any",
          "from_transport": "any",
          "from_start_port": "0",
          "from_end_port": "65535",
          "from_service": null
        },
        {
          "action": "ALLOW",
          "action_direction": "IN",
          "index": "5",
          "network_protocol": "ipv4",
          "to_interface": "en0",
          "to_ip": "10.10.10.10",
          "to_ip_prefix": "32",
          "to_transport": "any",
          "to_start_port": "0",
          "to_end_port": "65535",
          "to_service": null,
          "comment": null,
          "from_ip": "0.0.0.0",
          "from_ip_prefix": "0",
          "from_interface": "any",
          "from_transport": "any",
          "from_start_port": "0",
          "from_end_port": "65535",
          "from_service": null
        }
      ]
    }


## info
```python
info()
```
Provides parser metadata (version, author, etc.)

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

## Parser Information
Compatibility:  linux

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
