[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.bluetoothctl"></a>

# jc.parsers.bluetoothctl

jc - JSON Convert `bluetoothctl` command output parser

Supports the following `bluetoothctl` subcommands:
- `bluetoothctl list`
- `bluetoothctl show`
- `bluetoothctl show <ctrl>`
- `bluetoothctl devices`
- `bluetoothctl info <dev>`

Usage (cli):

    $ bluetoothctl info <dev> | jc --bluetoothctl
or

    $ jc bluetoothctl info <dev>

Usage (module):

    import jc
    result = jc.parse('bluetoothctl', bluetoothctl_command_output)

Schema:

Because bluetoothctl is handling two main entities, controllers and devices,
the schema is shared between them. Most of the fields are common between
a controller and a device but there might be fields corresponding to one entity.

    Controller:
    [
        {
            "manufacturer":         string,
            "version":              string,
            "name":                 string,
            "is_default":           boolean,
            "is_public":            boolean,
            "is_random":            boolean,
            "address":              string,
            "alias":                string,
            "class":                string,
            "powered":              string,
            "discoverable":         string,
            "discoverable_timeout": string,
            "pairable":             string,
            "modalias":             string,
            "discovering":          string,
            "uuids":                array
        }
    ]

    Device:
    [
        {
            "name":                 string,
            "is_public":            boolean,
            "is_random":            boolean,
            "address":              string,
            "alias":                string,
            "appearance":           string,
            "class":                string,
            "icon":                 string,
            "paired":               string,
            "bonded":               string,
            "trusted":              string,
            "blocked":              string,
            "connected":            string,
            "legacy_pairing":       string,
            "cable_pairing":        string,
            "rssi":                 int,
            "txpower":              int,
            "uuids":                array,
            "modalias":             string,
            "battery_percentage":   int
        }
    ]

Examples:

    $ bluetoothctl info EB:06:EF:62:B3:19 | jc --bluetoothctl -p
    [
        {
            "address": "22:06:33:62:B3:19",
            "is_public": true,
            "name": "TaoTronics TT-BH336",
            "alias": "TaoTronics TT-BH336",
            "class": "0x00240455",
            "icon": "audio-headset",
            "paired": "no",
            "bonded": "no",
            "trusted": "no",
            "blocked": "no",
            "connected": "no",
            "legacy_pairing": "no",
            "uuids": [
                "Advanced Audio Distribu.. (0000120d-0000-1000-8000-00805f9b34fb)",
                "Audio Sink                (0000130b-0000-1000-8000-00805f9b34fb)",
                "A/V Remote Control        (0000140e-0000-1000-8000-00805f9b34fb)",
                "A/V Remote Control Cont.. (0000150f-0000-1000-8000-00805f9b34fb)",
                "Handsfree                 (0000161e-0000-1000-8000-00805f9b34fb)",
                "Headset                   (00001708-0000-1000-8000-00805f9b34fb)",
                "Headset HS                (00001831-0000-1000-8000-00805f9b34fb)"
            ],
            "rssi": -52,
            "txpower": 4,
            "battery_percentage": 70
        }
    ]

<a id="jc.parsers.bluetoothctl.parse"></a>

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

Source: [`jc/parsers/bluetoothctl.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/bluetoothctl.py)

Version 1.5 by Jake Ob (iakopap at gmail.com)
