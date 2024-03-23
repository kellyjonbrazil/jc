r"""jc - JSON Convert `xrandr` command output parser

Usage (cli):

    $ xrandr | jc --xrandr
    $ xrandr --properties | jc --xrandr

or

    $ jc xrandr

Usage (module):

    import jc
    result = jc.parse('xrandr', xrandr_command_output)

Schema:

    {
      "screens": [
        {
          "screen_number":                     integer,
          "minimum_width":                     integer,
          "minimum_height":                    integer,
          "current_width":                     integer,
          "current_height":                    integer,
          "maximum_width":                     integer,
          "maximum_height":                    integer,
          "devices": [
            {
              "props": {

                # either an EdidModel object or key value pairs
                <key_name> : {
                  "name": string,
                  "product_id": string,
                  "serial_number": string,
                }

              },
              "resolution_modes": [
                {
                  "resolution_width":          integer,
                  "resolution_height":         integer,
                  "is_high_resolution":        boolean,
                  "frequencies": [
                    {
                      "frequency":             float,
                      "is_current":            boolean,
                      "is_preferred":          boolean
                    }
                  ]
                }
              ]
            }
          ],
          "is_connected":                      boolean,
          "is_primary":                        boolean,
          "device_name":                       string,
          "model_name":                        string,
          "product_id"                         string,
          "serial_number":                     string,
          "resolution_width":                  integer,
          "resolution_height":                 integer,
          "offset_width":                      integer,
          "offset_height":                     integer,
          "dimension_width":                   integer,
          "dimension_height":                  integer,
          "rotation":                          string,
          "reflection":                        string
        }
      ]
    }

Examples:

    $ xrandr | jc --xrandr -p
    {
      "screens": [
        {
          "screen_number": 0,
          "minimum_width": 8,
          "minimum_height": 8,
          "current_width": 1920,
          "current_height": 1080,
          "maximum_width": 32767,
          "maximum_height": 32767,
          "devices": [
            {
              "resolution_modes": [
                {
                  "resolution_width": 1920,
                  "resolution_height": 1080,
                  "is_high_resolution": false,
                  "frequencies": [
                    {
                      "frequency": 60.03,
                      "is_current": true,
                      "is_preferred": true
                    }
                  ]
                },
              ],
              "is_connected": true,
              "is_primary": true,
              "device_name": "eDP1",
              "resolution_width": 1920,
              "resolution_height": 1080,
              "offset_width": 0,
              "offset_height": 0,
              "dimension_width": 310,
              "dimension_height": 170,
              "rotation": "normal",
              "reflection": "normal"
            }
          ]
        }
      ]
    }

    $ xrandr --properties | jc --xrandr -p
    {
      "screens": [
        {
          "devices": [
            {
              "props": {
                "EDID": [
                  "00ffff5700000000",
                  "001c01a5544d9a27",
                  "0e50540101010101",
                  "010101383e401010",
                  "3500350f00000000",
                  "0000000000fe0041",
                  "554f0a20000000fe",
                  "00423137200a0070"
                ],
                "scaling mode": [
                  "Full aspect ",
                  "supported: Full, Center, Full aspect"
                ],
                "Colorspace": [
                  "Default ",
                  "supported: Default, RGB_Wide_Gamut_Fixed_Point, RGB_Wide_Gamut_Floating_Point, opRGB, DCI-P3_RGB_D65, BT2020_RGB, BT601_YCC, BT709_YCC, XVYCC_601, XVYCC_709, SYCC_601, opYCC_601, BT2020_CYCC, BT2020_YCC"
                ],
                "EdidModel": {
                  "name": "Generic",
                  "product_id": "22333",
                  "serial_number": "0"
                }
              },
              "resolution_modes": [
                {
                  "resolution_width": 320,
                  "resolution_height": 180,
                  "is_high_resolution": false,
                  "frequencies": [
                    {
                      "frequency": 59.84,
                      "is_current": false,
                      "is_preferred": false
                    }
                  ]
                }
              ],
              "is_connected": true,
              "is_primary": true,
              "device_name": "eDP-1",
              "rotation": "normal",
              "reflection": "normal",
              "resolution_width": 1920,
              "resolution_height": 1080,
              "offset_width": 0,
              "offset_height": 0,
              "dimension_width": 309,
              "dimension_height": 174
            }
          ],
          "screen_number": 0,
          "minimum_width": 320,
          "minimum_height": 200,
          "current_width": 1920,
          "current_height": 1080,
          "maximum_width": 16384,
          "maximum_height": 16384
        }
      ]
    }
"""
from collections import defaultdict
from enum import Enum
import re
from typing import Dict, List, Tuple, Union

import jc.utils
from jc.parsers.pyedid.edid import Edid
from jc.parsers.pyedid.helpers.edid_helper import EdidHelper

Match = None
try:
    # Added Python 3.7
    Match = re.Match
except AttributeError:
    Match = type(re.match("", ""))


class info:
    """Provides parser metadata (version, author, etc.)"""

    version = "2.1"
    description = "`xrandr` command parser"
    author = "Kevin Lyter"
    author_email = "code (at) lyterk.com"
    details = "Using parts of the pyedid library at https://github.com/jojonas/pyedid."
    compatible = ["linux", "darwin", "cygwin", "aix", "freebsd"]
    magic_commands = ["xrandr"]
    tags = ["command"]


__version__ = info.version

# NOTE: When developing, comment out the try statement and catch block to get
# TypedDict type hints and valid type errors.
try:
    # Added in Python 3.8
    from typing import TypedDict

    Frequency = TypedDict(
        "Frequency",
        {
            "frequency": float,
            "is_current": bool,
            "is_preferred": bool,
        },
    )
    ResolutionMode = TypedDict(
        "ResolutionMode",
        {
            "resolution_width": int,
            "resolution_height": int,
            "is_high_resolution": bool,
            "frequencies": List[Frequency],
        },
    )
    EdidModel = TypedDict(
        "EdidModel",
        {
            "name": str,
            "product_id": str,
            "serial_number": str,
        },
    )
    Props = Dict[str, Union[List[str], EdidModel]]
    Device = TypedDict(
        "Device",
        {
            "device_name": str,
            "model_name": str,
            "product_id": str,
            "serial_number": str,
            "is_connected": bool,
            "is_primary": bool,
            "resolution_width": int,
            "resolution_height": int,
            "offset_width": int,
            "offset_height": int,
            "dimension_width": int,
            "dimension_height": int,
            "props": Props,
            "resolution_modes": List[ResolutionMode],
            "rotation": str,
            "reflection": str,
        },
    )
    Screen = TypedDict(
        "Screen",
        {
            "screen_number": int,
            "minimum_width": int,
            "minimum_height": int,
            "current_width": int,
            "current_height": int,
            "maximum_width": int,
            "maximum_height": int,
            "devices": List[Device],
        },
    )
    Response = TypedDict(
        "Response",
        {
            "screens": List[Screen],
        },
    )
except ImportError:
    EdidModel = Dict[str, str]
    Props = Dict[str, Union[List[str], EdidModel]]
    Frequency = Dict[str, Union[float, bool]]
    ResolutionMode = Dict[str, Union[int, bool, List[Frequency]]]
    Device = Dict[str, Union[str, int, bool, List[ResolutionMode]]]
    Screen = Dict[str, Union[int, List[Device]]]
    Response = Dict[str, Screen]


_screen_pattern = (
    r"Screen (?P<screen_number>\d+): "
    + r"minimum (?P<minimum_width>\d+) x (?P<minimum_height>\d+), "
    + r"current (?P<current_width>\d+) x (?P<current_height>\d+), "
    + r"maximum (?P<maximum_width>\d+) x (?P<maximum_height>\d+)"
)


# eDP1 connected primary 1920x1080+0+0 (normal left inverted right x axis y axis)
#       310mm x 170mm
# regex101 demo link
_device_pattern = (
    r"(?P<device_name>.+) "
    + r"(?P<is_connected>(connected|disconnected)) ?"
    + r"(?P<is_primary> primary)? ?"
    + r"((?P<resolution_width>\d+)x(?P<resolution_height>\d+)"
    + r"\+(?P<offset_width>\d+)\+(?P<offset_height>\d+))? "
    + r"(?P<rotation>(normal|right|left|inverted)?) ?"
    + r"(?P<reflection>(X axis|Y axis|X and Y axis)?) ?"
    + r"(\(normal left inverted right x axis y axis\))?"
    + r"( ?((?P<dimension_width>\d+)mm x (?P<dimension_height>\d+)mm)?)?"
)

# 1920x1080i     60.03*+  59.93
# 1920x1080     60.00 +  50.00    59.94
_resolution_mode_pattern = r"\s*(?P<resolution_width>\d+)x(?P<resolution_height>\d+)(?P<is_high_resolution>i)?\s+(?P<rest>.*)"
_frequencies_pattern = r"(((?P<frequency>\d+\.\d+)(?P<star>\*| |)(?P<plus>\+?)?)+)"


# Values sometimes appear on the same lines as the keys (CscMatrix), sometimes on the line
# below (as with EDIDs), and sometimes both (CTM).
# Capture the key line that way.
#
# CTM: 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0 0
#         0 1
# CscMatrix: 65536 0 0 0 0 65536 0 0 0 0 65536 0
# EDID:
#         00ffffffffffff0010ac33424c303541
#         0f210104b53c22783eee95a3544c9926
_prop_key_pattern = r"\s+(?P<key>[\w| |\-|_]+):\s?(?P<maybe_value>.*)"


class LineType(Enum):
    Screen = 1
    Device = 2
    ResolutionMode = 3
    PropKey = 4
    PropValue = 5
    Invalid = 6


class _Line:
    """Provide metadata about line to make handling it more simple across fn boundaries"""

    def __init__(self, s: str, t: LineType, m: Match):
        self.s = s
        self.t = t
        self.m = m

    @classmethod
    def categorize(cls, line: str) -> "_Line":
        """Iterate through line char by char to see what type of line it is. Apply regexes for more distinctness. Save the regexes and return them for later processing."""
        i = 0
        tab_count = 0
        while True:
            try:
                c = line[i]
            except:
                # Really shouldn't be getting to the end of the line
                raise Exception(f"Reached end of line unexpectedly: '{line}'")

            if not c.isspace():
                if tab_count == 0:
                    screen_match = re.match(_screen_pattern, line)
                    if screen_match:
                        return cls(line, LineType.Screen, screen_match)

                    device_match = re.match(_device_pattern, line)
                    if device_match:
                        return cls(line, LineType.Device, device_match)
                    else:
                        break
                elif tab_count == 1:
                    match = re.match(_prop_key_pattern, line)
                    if match:
                        return cls(line, LineType.PropKey, match)
                    else:
                        break
                else:
                    match = re.match(r"\s+(.*)\s+", line)
                    if match:
                        return cls(line, LineType.PropValue, match)
                    else:
                        break
            else:
                if c == " ":
                    match = re.match(_resolution_mode_pattern, line)
                    if match:
                        return cls(line, LineType.ResolutionMode, match)
                    else:
                        break
                elif c == "\t":
                    tab_count += 1
            i += 1
        raise Exception(f"Line could not be categorized: '{line}'")


def _parse_screen(line: _Line) -> Screen:
    d = line.m.groupdict()

    screen: Screen = {"devices": []}  # type: ignore # Will be populated, but not immediately.
    for k, v in d.items():
        screen[k] = int(v)

    return screen


def _parse_device(line: _Line) -> Device:
    matches = line.m.groupdict()

    device: Device = {
        "props": defaultdict(list),
        "resolution_modes": [],
        "is_connected": matches["is_connected"] == "connected",
        "is_primary": matches["is_primary"] is not None
        and len(matches["is_primary"]) > 0,
        "device_name": matches["device_name"],
        "rotation": matches["rotation"] or "normal",
        "reflection": matches["reflection"] or "normal",
    }
    for k, v in matches.items():
        if k not in {
            "is_connected",
            "is_primary",
            "device_name",
            "rotation",
            "reflection",
        }:
            try:
                if v:
                    device[k] = int(v)
            except ValueError:
                raise Exception([f"{line.s} : {k} - {v} is not int-able"])

    return device


def _parse_resolution_mode(line: _Line) -> ResolutionMode:
    frequencies: List[Frequency] = []

    d = line.m.groupdict()
    resolution_width = int(d["resolution_width"])
    resolution_height = int(d["resolution_height"])
    is_high_resolution = d["is_high_resolution"] is not None

    mode: ResolutionMode = {
        "resolution_width": resolution_width,
        "resolution_height": resolution_height,
        "is_high_resolution": is_high_resolution,
        "frequencies": frequencies,
    }

    result = re.finditer(_frequencies_pattern, d["rest"])
    if not result:
        return mode

    for match in result:
        d = match.groupdict()
        frequency = float(d["frequency"])
        is_current = len(d["star"].strip()) > 0
        is_preferred = len(d["plus"].strip()) > 0
        f: Frequency = {
            "frequency": frequency,
            "is_current": is_current,
            "is_preferred": is_preferred,
        }
        mode["frequencies"].append(f)
    return mode


def _parse_props(index: int, line: _Line, lines: List[str]) -> Tuple[int, Props]:
    tmp_props: Dict[str, List[str]] = {}
    key = ""
    while index <= len(lines):
        if line.t == LineType.PropKey:
            d = line.m.groupdict()
            # See _prop_key_pattern
            key = d["key"]
            maybe_value = d["maybe_value"]
            if not maybe_value:
                tmp_props[key] = []
            else:
                tmp_props[key] = [maybe_value]
        elif line.t == LineType.PropValue:
            tmp_props[key].append(line.s.strip())
        else:
            # We've gone past our props and need to ascend
            index = index - 1
            break
        index += 1
        try:
            line = _Line.categorize(lines[index])
        except:
            pass

    props: Props = {}
    if "EDID" in tmp_props:
        edid = Edid(EdidHelper.hex2bytes("".join(tmp_props["EDID"])))
        model: EdidModel = {
            "name": edid.name or "Generic",
            "product_id": str(edid.product),
            "serial_number": str(edid.serial),
        }
        props["EdidModel"] = model

    return index, {**tmp_props, **props}


def parse(data: str, raw: bool = False, quiet: bool = False) -> Response:
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    index = 0
    lines = data.splitlines()
    screen, device = None, None

    # temporary fix to ignore specific unhandled lines
    ignore_pattern = re.compile(r'^\s+(h|v):\s+(height|width)\s+\d+\s+start\s+\d+\s+end')

    result: Response = {"screens": []}
    if jc.utils.has_data(data):
        while index < len(lines):

            # temporary fix to ignore specific unhandled lines
            ignore_re = ignore_pattern.match(lines[index])
            if ignore_re:
                index += 1
                continue

            line = _Line.categorize(lines[index])
            if line.t == LineType.Screen:
                screen = _parse_screen(line)
                result["screens"].append(screen)
            elif line.t == LineType.Device:
                device = _parse_device(line)
                if not screen:
                    raise Exception("There should be an identifiable screen")
                screen["devices"].append(device)
            elif line.t == LineType.ResolutionMode:
                resolution_mode = _parse_resolution_mode(line)
                if not device:
                    raise Exception("Undefined device")
                device["resolution_modes"].append(resolution_mode)
            elif line.t == LineType.PropKey:
                # Props needs to be state aware, it owns the index.
                ix, props = _parse_props(index, line, lines)
                index = ix
                if not device:
                    raise Exception("Undefined device")
                device["props"] = props
            index += 1

    return result
