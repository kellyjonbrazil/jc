r"""jc - JSON Convert `amixer sget` command output parser
Usage (cli):
    $ amixer sget <control_name> | jc --amixer
    $ amixer sget Master | jc --amixer
    $ amixer sget Capture | jc --amixer
    $ amixer sget Speakers | jc --amixer
Usage (module):
    import jc
    result = jc.parse('amixer', <amixer sget command output>)
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
        "playback_min":                 string,
        "playback_max":                 string
    },
    "mono": {
        "playback_value":               string,
        "percentage":                   string,
        "dB":                           string,
        "status":                       string
    }
}

Examples:
$ amixer sget Master | jc --amixer -p
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
        "dB": "0.00dB",
        "status": "on"
    }
}

"""
from typing import List, Dict

import jc.utils


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

def _process(proc_data: dict) -> dict:
    """
    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        dictionary of amixer sget <control_name>
    """
    return proc_data


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> List[Dict]:
    """
    Main text parsing function, The amixer is alsa mixer tool and output, Will work with Linux OS only.


    Parameters:
        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True


    Returns:
        List of Dictionaries. Raw or processed structured data.
        push test
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
          Front Left: Capture 63 [100%] [30.00dB] [on]
          Front Right: Capture 63 [100%] [30.00dB] [on]




        2."":~$ amixer sget Master
        Simple mixer control 'Master',0
          Capabilities: pvolume pvolume-joined pswitch pswitch-joined
          Playback channels: Mono
          Limits: Playback 0 - 87
          Mono: Playback 87 [100%] [0.00dB] [on]





        3."":~$ amixer sget Speaker
        Simple mixer control 'Speaker',0
          Capabilities: pvolume pswitch
          Playback channels: Front Left - Front Right
          Limits: Playback 0 - 87
          Mono:
          Front Left: Playback 87 [100%] [0.00dB] [on]
          Front Right: Playback 87 [100%] [0.00dB] [on]




        4."":~$ amixer sget Headphone
        Simple mixer control 'Headphone',0
          Capabilities: pvolume pswitch
          Playback channels: Front Left - Front Right
          Limits: Playback 0 - 87
          Mono:
          Front Left: Playback 0 [0%] [-65.25dB] [off]
          Front Right: Playback 0 [0%] [-65.25dB] [off]
    """
    # checks os compatibility and print a stderr massage if not compatible. quiet True could remove this check.
    jc.utils.compatibility(__name__, info.compatible, quiet)

    # check if string
    jc.utils.input_type_check(data)

    # starts the parsing from here
    mapping = {}
    # split lines and than work on each line
    lines = data.splitlines()
    first_line = lines[0].strip()

    # Extract the control name from the first line
    if first_line.startswith("Simple mixer control"):
        control_name = first_line.split("'")[1]
    else:
        raise ValueError("Invalid amixer output format: missing control name.")
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
            # Example: "Playback 255 [100%] [0.00dB] [on]"
            channel_data = channel_info.split(" ")
            if channel_data[0] == "":
                continue
            playback_value = channel_data[1]
            percentage = channel_data[2].strip("[]")  # Extract percentage e.g., "100%"
            db_value = channel_data[3].strip("[]")  # Extract dB value e.g., "0.00dB"
            status = channel_data[4].strip("[]")  # Extract status e.g., "on" or "off"

            # Store channel mapping in the dictionary
            mapping[channel_name] = {
                "playback_value": playback_value,
                "percentage": percentage,
                "dB": db_value,
                "status": status
            }
    return _process(mapping) if raw else mapping


if __name__ == '__main__':
    data_sget_master = """Simple mixer control 'Master',0
      Capabilities: pvolume pvolume-joined pswitch pswitch-joined
      Playback channels: Mono
      Limits: Playback 0 - 87
      Mono: Playback 87 [100%] [0.00dB] [on]"""

    data_sget_capture = """Simple mixer control 'Capture',0
      Capabilities: cvolume cswitch
      Capture channels: Front Left - Front Right
      Limits: Capture 0 - 63
      Front Left: Capture 63 [100%] [30.00dB] [on]
      Front Right: Capture 63 [100%] [30.00dB] [on]"""


    data_sget_speakers = """Simple mixer control 'Speaker',0
      Capabilities: pvolume pswitch
      Playback channels: Front Left - Front Right
      Limits: Playback 0 - 87
      Mono:
      Front Left: Playback 87 [100%] [0.00dB] [on]
      Front Right: Playback 87 [100%] [0.00dB] [on]"""

    data_sget_headphones = """Simple mixer control 'Headphone',0
      Capabilities: pvolume pswitch
      Playback channels: Front Left - Front Right
      Limits: Playback 0 - 87
      Mono:
      Front Left: Playback 0 [0%] [-65.25dB] [off]
      Front Right: Playback 0 [0%] [-65.25dB] [off]"""
    output_data_sget_master = parse(data=data_sget_master)
    output_data_sget_speakers = parse(data=data_sget_speakers)
    output_data_sget_headphones = parse(data=data_sget_headphones)
    output_data_sget_capture = parse(data=data_sget_capture)
    di = {'master': output_data_sget_master,
          'speakers': output_data_sget_speakers,
          'headphones': output_data_sget_headphones,
          'capture': output_data_sget_capture}
    for key, val in di.items():
        print(f"[info] for key: {key}")
        print(f"[info] the output is: {val}")