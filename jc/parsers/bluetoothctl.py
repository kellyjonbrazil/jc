r"""jc - JSON Convert `bluetoothctl` command output parser

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
"""
import re
from typing import List, Dict, Optional, Any
from jc.jc_types import JSONDictType
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.4'
    description = '`bluetoothctl` command parser'
    author = 'Jake Ob'
    author_email = 'iakopap at gmail.com'
    compatible = ['linux']
    magic_commands = ['bluetoothctl']
    tags = ['command']


__version__ = info.version

try:
    from typing import TypedDict

    Controller = TypedDict(
        "Controller",
        {
            "manufacturer": str,
            "version": str,
            "name": str,
            "is_default": bool,
            "is_public": bool,
            "is_random": bool,
            "address": str,
            "alias": str,
            "class": str,
            "powered": str,
            "power_state": str,
            "discoverable": str,
            "discoverable_timeout": str,
            "pairable": str,
            "modalias": str,
            "discovering": str,
            "uuids": List[str],
        },
    )
    Device = TypedDict(
        "Device",
        {
            "name": str,
            "is_public": bool,
            "is_random": bool,
            "address": str,
            "alias": str,
            "appearance": str,
            "class": str,
            "icon": str,
            "paired": str,
            "bonded": str,
            "trusted": str,
            "blocked": str,
            "connected": str,
            "legacy_pairing": str,
            "rssi": int,
            "txpower": int,
            "uuids": List[str],
            "modalias": str,
            "battery_percentage": int
        },
    )
except ImportError:
    Controller = Dict[str, Any]  # type: ignore
    Device = Dict[str, Any]  # type: ignore


_controller_head_pattern = r"Controller (?P<address>([0-9A-F]{2}:){5}[0-9A-F]{2}) (?P<name>.+)"

_controller_line_pattern = (
    r"(\s*Manufacturer:\s*(?P<manufacturer>.+)"
    + r"|\s*Version:\s*(?P<version>.+)"
    + r"|\s*Name:\s*(?P<name>.+)"
    + r"|\s*Alias:\s*(?P<alias>.+)"
    + r"|\s*Class:\s*(?P<class>.+)"
    + r"|\s*Powered:\s*(?P<powered>.+)"
    + r"|\s*PowerState:\s*(?P<power_state>.+)"
    + r"|\s*Discoverable:\s*(?P<discoverable>.+)"
    + r"|\s*DiscoverableTimeout:\s*(?P<discoverable_timeout>.+)"
    + r"|\s*Pairable:\s*(?P<pairable>.+)"
    + r"|\s*Modalias:\s*(?P<modalias>.+)"
    + r"|\s*Discovering:\s*(?P<discovering>.+)"
    + r"|\s*UUID:\s*(?P<uuid>.+))"
)

def _parse_controller(next_lines: List[str]) -> Optional[Controller]:
    next_line = next_lines.pop()
    result = re.match(_controller_head_pattern, next_line)

    if not result:
        next_lines.append(next_line)
        return None

    matches = result.groupdict()

    name = matches["name"]

    if name.endswith("not available"):
        return None

    controller: Controller = {
            "manufacturer": '',
            "version": '',
            "name": '',
            "is_default": False,
            "is_public": False,
            "is_random": False,
            "address": matches["address"],
            "alias": '',
            "class": '',
            "powered": '',
            "power_state": '',
            "discoverable": '',
            "discoverable_timeout": '',
            "pairable": '',
            "modalias": '',
            "discovering": '',
            "uuids": [],
        }

    if name.endswith("[default]"):
        controller["is_default"] = True
        name = name.replace("[default]", "")
    elif name.endswith("(public)"):
        controller["is_public"] = True
        name = name.replace("(public)", "")
    elif name.endswith("(random)"):
        controller["is_random"] = True
        name = name.replace("(random)", "")

    controller["name"] = name.strip()

    while next_lines:
        next_line = next_lines.pop()
        result = re.match(_controller_line_pattern, next_line)

        if not result:
            next_lines.append(next_line)
            return controller

        matches = result.groupdict()

        if matches["manufacturer"]:
            controller["manufacturer"] = matches["manufacturer"]
        elif matches["version"]:
            controller["version"] = matches["version"]
        elif matches["name"]:
            controller["name"] = matches["name"]
        elif matches["alias"]:
            controller["alias"] = matches["alias"]
        elif matches["class"]:
            controller["class"] = matches["class"]
        elif matches["powered"]:
            controller["powered"] = matches["powered"]
        elif matches["power_state"]:
            controller["power_state"] = matches["power_state"]
        elif matches["discoverable"]:
            controller["discoverable"] = matches["discoverable"]
        elif matches["discoverable_timeout"]:
            controller["discoverable_timeout"] = matches["discoverable_timeout"]
        elif matches["pairable"]:
            controller["pairable"] = matches["pairable"]
        elif matches["modalias"]:
            controller["modalias"] = matches["modalias"]
        elif matches["discovering"]:
            controller["discovering"] = matches["discovering"]
        elif matches["uuid"]:
            if not "uuids" in controller:
                controller["uuids"] = []
            controller["uuids"].append(matches["uuid"])

    return controller

_device_head_pattern = r"Device (?P<address>([0-9A-F]{2}:){5}[0-9A-F]{2}) (?P<name>.+)"

_device_line_pattern = (
    r"(\s*Name:\s*(?P<name>.+)"
    + r"|\s*Alias:\s*(?P<alias>.+)"
    + r"|\s*Appearance:\s*(?P<appearance>.+)"
    + r"|\s*Class:\s*(?P<class>.+)"
    + r"|\s*Icon:\s*(?P<icon>.+)"
    + r"|\s*Paired:\s*(?P<paired>.+)"
    + r"|\s*Bonded:\s*(?P<bonded>.+)"
    + r"|\s*Trusted:\s*(?P<trusted>.+)"
    + r"|\s*Blocked:\s*(?P<blocked>.+)"
    + r"|\s*Connected:\s*(?P<connected>.+)"
    + r"|\s*LegacyPairing:\s*(?P<legacy_pairing>.+)"
    + r"|\s*Modalias:\s*(?P<modalias>.+)"
    + r"|\s*RSSI:\s*(?P<rssi>.+)"
    + r"|\s*TxPower:\s*(?P<txpower>.+)"
    + r"|\s*Battery\sPercentage:\s*0[xX][0-9a-fA-F]*\s*\((?P<battery_percentage>[0-9]+)\)"
    + r"|\s*UUID:\s*(?P<uuid>.+))"
)


def _parse_device(next_lines: List[str], quiet: bool) -> Optional[Device]:
    next_line = next_lines.pop()
    result = re.match(_device_head_pattern, next_line)

    if not result:
        next_lines.append(next_line)
        return None

    matches = result.groupdict()

    name = matches["name"]

    if name.endswith("not available"):
        return None

    device: Device = {
        "name": '',
        "is_public": False,
        "is_random": False,
        "address": matches["address"],
        "alias": '',
        "appearance": '',
        "class": '',
        "icon": '',
        "paired": '',
        "bonded": '',
        "trusted": '',
        "blocked": '',
        "connected": '',
        "legacy_pairing": '',
        "rssi": 0,
        "txpower": 0,
        "uuids": [],
        "modalias": '',
        "battery_percentage": 0
    }

    if name.endswith("(public)"):
        device["is_public"] = True
        name = name.replace("(public)", "")
    elif name.endswith("(random)"):
        device["is_random"] = True
        name = name.replace("(random)", "")

    device["name"] = name.strip()

    while next_lines:
        next_line = next_lines.pop()
        result = re.match(_device_line_pattern, next_line)

        if not result:
            next_lines.append(next_line)
            return device

        matches = result.groupdict()

        if matches["name"]:
            device["name"] = matches["name"]
        elif matches["alias"]:
            device["alias"] = matches["alias"]
        elif matches["appearance"]:
            device["appearance"] = matches["appearance"]
        elif matches["class"]:
            device["class"] = matches["class"]
        elif matches["icon"]:
            device["icon"] = matches["icon"]
        elif matches["paired"]:
            device["paired"] = matches["paired"]
        elif matches["bonded"]:
            device["bonded"] = matches["bonded"]
        elif matches["trusted"]:
            device["trusted"] = matches["trusted"]
        elif matches["blocked"]:
            device["blocked"] = matches["blocked"]
        elif matches["connected"]:
            device["connected"] = matches["connected"]
        elif matches["legacy_pairing"]:
            device["legacy_pairing"] = matches["legacy_pairing"]
        elif matches["rssi"]:
            rssi = matches["rssi"]
            try:
                device["rssi"] = int(rssi)
            except ValueError:
                if not quiet:
                    jc.utils.warning_message([f"{next_line} : rssi - {rssi} is not int-able"])
        elif matches["txpower"]:
            txpower = matches["txpower"]
            try:
                device["txpower"] = int(txpower)
            except ValueError:
                if not quiet:
                    jc.utils.warning_message([f"{next_line} : txpower - {txpower} is not int-able"])
        elif matches["uuid"]:
            if not "uuids" in device:
                device["uuids"] = []
            device["uuids"].append(matches["uuid"])
        elif matches["modalias"]:
            device["modalias"] = matches["modalias"]
        elif matches["battery_percentage"]:
            battery_percentage = matches["battery_percentage"]
            try:
                device["battery_percentage"] = int(battery_percentage)
            except ValueError:
                if not quiet:
                    jc.utils.warning_message([f"{next_line} : battery_percentage - {battery_percentage} is not int-able"])

    return device

def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of Dictionaries. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)
    result: List = []

    if jc.utils.has_data(data):
        linedata = data.splitlines()
        linedata.reverse()

        while linedata:
            element = None
            if data.startswith("Controller"):
                element = _parse_controller(linedata)
            elif data.startswith("Device"):
                element = _parse_device(linedata, quiet)  # type: ignore

            if element:
                result.append(element)
            else:
                break

    return result
