[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.systemextensionsctl"></a>

# jc.parsers.systemextensionsctl

jc - JSON Convert `systemextensionsctl list` command output parser

Usage (cli):

    $ systemextensionsctl list | jc --systemextensionsctl

or

    $ jc systemextensionsctl list

Usage (module):

    import jc
    result = jc.parse('systemextensionsctl', systemextensionsctl_command_output)

Schema:

    [
      {
        "category":                 string,
        "enabled":                  boolean,
        "active":                   boolean,
        "team_id":                  string/null,
        "bundle_id":                string,
        "version":                  string,
        "build":                    string,
        "name":                     string,
        "state":                    string
      }
    ]

Examples:

    $ systemextensionsctl list | jc --systemextensionsctl -p
    [
      {
        "category": "com.apple.system_extension.network_extension",
        "enabled": true,
        "active": true,
        "team_id": "TZ3UEPFYKD",
        "bundle_id": "com.checkpoint.fw.filter",
        "version": "871010711",
        "build": "6",
        "name": "Check Point Firewall",
        "state": "activated enabled"
      },
      {
        "category": "com.apple.system_extension.network_extension",
        "enabled": true,
        "active": true,
        "team_id": "UBF8T346G9",
        "bundle_id": "com.microsoft.wdav.netext",
        "version": "101.47.27",
        "build": "101.47.27",
        "name": "Microsoft Defender ATP Network Extension",
        "state": "activated enabled"
      },
      {
        "category": "com.apple.system_extension.endpoint_security",
        "enabled": true,
        "active": true,
        "team_id": "UBF8T346G9",
        "bundle_id": "com.microsoft.wdav.epsext",
        "version": "101.47.27",
        "build": "101.47.27",
        "name": "Microsoft Defender ATP Endpoint Security Extension",
        "state": "activated enabled"
      },
      {
        "category": "com.apple.system_extension.driver_extension",
        "enabled": true,
        "active": true,
        "team_id": "G43BCU2T37",
        "bundle_id": "org.pqrs.Karabiner-DriverKit-VirtualHIDDevice",
        "version": "1.0.0",
        "build": "1.0.0",
        "name": "org.pqrs.Karabiner-DriverKit-VirtualHIDDevice",
        "state": "activated enabled"
      }
    ]

    $ systemextensionsctl list | jc --systemextensionsctl -p -r
    [
      {
        "category": "com.apple.system_extension.network_extension",
        "enabled": "*",
        "active": "*",
        "team_id": "TZ3UEPFYKD",
        "bundle_id": "com.checkpoint.fw.filter",
        "version": "871010711",
        "build": "6",
        "name": "Check Point Firewall",
        "state": "activated enabled"
      },
      ...
    ]

<a id="jc.parsers.systemextensionsctl.parse"></a>

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
Compatibility:  darwin

Source: [`jc/parsers/systemextensionsctl.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/systemextensionsctl.py)

Version 1.0 by Ron Green (11993626+georgettica@users.noreply.github.com)
