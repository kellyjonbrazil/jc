r"""jc - JSON Convert `amixer sget` command output parser

Usage (cli):

    $ amixer sget <control_name> | jc --amixer
    $ amixer sget Master | jc --amixer
    $ amixer sget Capture | jc --amixer
    $ amixer sget Speakers | jc --amixer

Usage (module):

    import jc
    result = jc.parse('amixer', <amixer_sget_command_output>)

Schema:

    {
        "control_name":                     string,
        "capabilities": [
                                            string
        ],
        "playback_channels": [
                                            string
        ],
        "limits": {
            "playback_min":                 integer,
            "playback_max":                 integer
        },
        "mono": {
            "playback_value":               integer,
            "percentage":                   integer,
            "db":                           float,
            "status":                       boolean
        }
    }

Examples:

    $ amixer sget Master | jc --amixer -p
    {
      "control_name": "Capture",
      "capabilities": [
        "cvolume",
        "cswitch"
      ],
      "playback_channels": [],
      "limits": {
        "playback_min": 0,
        "playback_max": 63
      },
      "front_left": {
        "playback_value": 63,
        "percentage": 100,
        "db": 30.0,
        "status": true
      },
      "front_right": {
        "playback_value": 63,
        "percentage": 100,
        "db": 30.0,
        "status": true
      }
    }

    $ amixer sget Master | jc --amixer -p -r
    {
        "control_name": "Master",
        "capabilities": [
            "pvolume",
            "pvolume-joined",
            "pswitch",
            "pswitch-joined"
        ],
        "playback_channels": [
            "Mono"
        ],
        "limits": {
            "playback_min": "0",
            "playback_max": "87"
        },
        "mono": {
            "playback_value": "87",
            "percentage": "100%",
            "db": "0.00db",
            "status": "on"
        }
    }
"""
from typing import Dict

import jc.utils
from jc.utils import convert_to_int
from jc.exceptions import ParseError

class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`amixer` command parser'
    author = 'Eden Refael'
    author_email = 'edenraf@hotmail.com'
    compatible = ['linux']
    magic_commands = ['amixer']
    tags = ['command']


__version__ = info.version


def _process(proc_data: Dict) -> Dict:
    """
    Processes raw structured data to match the schema requirements.

    Parameters:
        proc_data: (dict) raw structured data from the parser

    Returns:
        (dict) processed structured data adhering to the schema
    """
    if not proc_data:
        return {}

    # Initialize the processed dictionary
    processed = {
        "control_name": proc_data.get("control_name", ""),
        "capabilities": proc_data.get("capabilities", []),
        "playback_channels": proc_data.get("playback_channels", []),
        "limits": {
            "playback_min": convert_to_int(proc_data.get("limits", {}).get("playback_min", 0)),
            "playback_max": convert_to_int(proc_data.get("limits", {}).get("playback_max", 0)),
        },
    }

    # Process Mono or channel-specific data
    channels = ["mono", "front_left", "front_right"]
    for channel in channels:
        if channel in proc_data:
            channel_data = proc_data[channel]
            processed[channel] = {
                "playback_value": convert_to_int(channel_data.get("playback_value", 0)),
                "percentage": convert_to_int(channel_data.get("percentage", "0%").strip("%")),
                "db": float(channel_data.get("db", "0.0db").strip("db")),
                "status": channel_data.get("status", "off") == "on",
            }

    return processed


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> Dict:
    """
    Main text parsing function

    Parameters:
        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:
        Dictionary. Raw or processed structured data.
    """
    """
    The Algorithm for parsing the `amixer sget` command, Input Explained/Rules/Pseudo Algorithm:
    1. There will always be the first line which tells the user about the control name.
    2. There will always be the Capabilities which include many of capabilities - It will be listed and separated by `" "`.
    3. After that we'll need to distinct between the Channel - Could be many of channels - It will be listed and separated
       by `" "`.
        3a. Capture channels - List of channels
        3b. Playback channels - List of channels
    4. Limits - We'll always have the minimum limit and the maximum limit.

    Input Example:
        1."":~$ amixer sget Capture
        Simple mixer control 'Capture',0
          Capabilities: cvolume cswitch
          Capture channels: Front Left - Front Right
          Limits: Capture 0 - 63
          Front Left: Capture 63 [100%] [30.00db] [on]
          Front Right: Capture 63 [100%] [30.00db] [on]

        2."":~$ amixer sget Master
        Simple mixer control 'Master',0
          Capabilities: pvolume pvolume-joined pswitch pswitch-joined
          Playback channels: Mono
          Limits: Playback 0 - 87
          Mono: Playback 87 [100%] [0.00db] [on]

        3."":~$ amixer sget Speaker
        Simple mixer control 'Speaker',0
          Capabilities: pvolume pswitch
          Playback channels: Front Left - Front Right
          Limits: Playback 0 - 87
          Mono:
          Front Left: Playback 87 [100%] [0.00db] [on]
          Front Right: Playback 87 [100%] [0.00db] [on]

        4."":~$ amixer sget Headphone
        Simple mixer control 'Headphone',0
          Capabilities: pvolume pswitch
          Playback channels: Front Left - Front Right
          Limits: Playback 0 - 87
          Mono:
          Front Left: Playback 0 [0%] [-65.25db] [off]
          Front Right: Playback 0 [0%] [-65.25db] [off]
    """
    # checks os compatibility and print a stderr massage if not compatible. quiet True could remove this check.
    jc.utils.compatibility(__name__, info.compatible, quiet)

    # check if string
    jc.utils.input_type_check(data)

    # starts the parsing from here
    mapping: Dict = {}

    if jc.utils.has_data(data):
        # split lines and than work on each line
        lines = data.splitlines()
        first_line = lines[0].strip()

        # Extract the control name from the first line
        if first_line.startswith("Simple mixer control"):
            control_name = first_line.split("'")[1]
        else:
            raise ParseError("Invalid amixer output format: missing control name.")
        # map the control name
        mapping["control_name"] = control_name

        # Process subsequent lines for capabilities, channels, limits, and channel-specific mapping.
        # gets the lines from the next line - because we already took care the first line.
        for line in lines[1:]:
            # strip the line (maybe there are white spaces in the begin&end)
            line = line.strip()

            if line.startswith("Capabilities:"):
                mapping["capabilities"] = line.split(":")[1].strip().split()
            elif line.startswith("Playback channels:"):
                mapping["playback_channels"] = line.split(":")[1].strip().split(" - ")
            elif line.startswith("Limits:"):
                limits = line.split(":")[1].strip().split(" - ")
                mapping["limits"] = {
                    "playback_min": limits[0].split()[1],
                    "playback_max": limits[1]
                }
            elif line.startswith("Mono:") or line.startswith("Front Left:") or line.startswith("Front Right:"):
                # Identify the channel name and parse its information
                channel_name = line.split(":")[0].strip().lower().replace(" ", "_")
                channel_info = line.split(":")[1].strip()
                # Example: "Playback 255 [100%] [0.00db] [on]"
                channel_data = channel_info.split(" ")
                if channel_data[0] == "":
                    continue

                if "dB" in channel_data[3]:
                    db_value = channel_data[3].strip("[]")
                    status = channel_data[4].strip("[]")
                else:
                    db_value = "0.0db"
                    status = channel_data[3].strip("[]")

                playback_value = channel_data[1]
                percentage = channel_data[2].strip("[]")  # Extract percentage e.g., "100%"

                # Store channel mapping in the dictionary
                mapping[channel_name] = {
                    "playback_value": playback_value,
                    "percentage": percentage,
                    "db": db_value.lower(),
                    "status": status
                }

    return mapping if raw else _process(mapping)
