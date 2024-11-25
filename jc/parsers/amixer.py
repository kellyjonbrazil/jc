from typing import List, Dict

import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1'
    description = '`amixer` command parser'
    author = 'Eden Refael'
    author_email = 'edenraf@hotmail.com'
    compatible = ['linux']
    magic_commands = ['amixer']
    tags = ['command']


__version__ = info.version

def _process(proc_data: List[Dict]) -> List[Dict]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured data to conform to the schema:
    """
    # int_list = {'expires'}
    #
    # # in BSD style, change name to null if it is a question mark
    # for entry in proc_data:
    #     if 'name' in entry and entry['name'] == '?':
    #         entry['name'] = None
    #
    #     for key in entry:
    #         if key in int_list:
    #             entry[key] = jc.utils.convert_to_int(entry[key])
    #
    # return proc_data


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> List[Dict]:
    """
    Main text parsing function, The amixer is alsa mixer tool and output, Will work with
    Linux OS only.

    Parameters:
        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:
        List of Dictionaries. Raw or processed structured data.
        push test
    """
    # checks os compatibility and print a stderr massage if not compatible. quiet True could remove this check.
    jc.utils.compatibility(__name__, info.compatible, quiet)

    # check if string
    jc.utils.input_type_check(data)

    raw_output = []
    lines = list(filter(None, data.splitlines())) # lines=cleandata

    data = {}
    # Strip and check for the first line to extract the control name directly
    first_line = lines[0].strip()
    if first_line.startswith("Simple mixer control"):
        # Extract the control name, removing the single quotes
        control_name = first_line.split("'")[1]  # Extracts the part inside the single quotes
    else:
        raise ValueError("Invalid amixer output format: missing control name.")

    # Add control name to the parsed data as a key
    data["control_name"] = control_name

    # Parse the rest of the output
    for line in lines[1:]:
        line = line.strip()
        if line.startswith("Capabilities:"):
            data["capabilities"] = line.split(":")[1].strip().split()
        elif line.startswith("Playback channels:"):
            data["playback_channels"] = line.split(":")[1].strip().split(" - ")
        elif line.startswith("Limits:"):
            limits = line.split(":")[1].strip().split(" - ")
            data["limits"] = {
                "playback_min": int(limits[0].split()[1]),
                "playback_max": int(limits[1])
            }
        elif line.startswith("Mono:") or line.startswith("Front Left:") or line.startswith("Front Right:"):
            # Identifying whether it's Mono, Front Left, or Front Right
            channel_name = line.split(":")[0].strip().lower().replace(" ", "_")
            channel_info = line.split(":")[1].strip()

            # Example: "Playback 255 [100%] [0.00dB] [on]"
            channel_data = channel_info.split(" ")
            playback_value = int(channel_data[0])
            percentage = channel_data[1][1:-1]  # Extract percentage e.g. "100%"
            db_value = channel_data[2][1:-3]  # Extract dB value e.g. "0.00dB"
            status = channel_data[3][1:-1]  # Extract status "on" or "off"

            # Storing channel data in the dict
            data[channel_name] = {
                "playback_value": playback_value,
                "percentage": percentage,
                "dB": db_value,
                "status": status
            }

    return data
    # another test

    # if jc.utils.has_data(data):

        # remove final Entries row if -v was used
        # if cleandata[-1].startswith('Entries:'):
    #         cleandata.pop(-1)
    #
    #     # detect if freebsd/osx style was used
    #     if cleandata[0][-1] == ']':
    #         for line in cleandata:
    #             splitline = line.split()
    #             output_line: Dict[str, Any] = {
    #                 'name': splitline[0],
    #                 'address': splitline[1].lstrip('(').rstrip(')'),
    #                 'hwtype': splitline[-1].lstrip('[').rstrip(']'),
    #                 'hwaddress': splitline[3],
    #                 'iface': splitline[5]
    #             }
    #
    #             if 'permanent' in splitline:
    #                 output_line['permanent'] = True
    #             else:
    #                 output_line['permanent'] = False
    #
    #             if 'expires' in splitline:
    #                 output_line['expires'] = splitline[-3]
    #
    #             raw_output.append(output_line)
    #
    #     # detect if linux style was used
    #     elif cleandata[0].startswith('Address'):
    #
    #         # fix header row to change Flags Mask to flags_mask
    #         cleandata[0] = cleandata[0].replace('Flags Mask', 'flags_mask')
    #         cleandata[0] = cleandata[0].lower()
    #
    #         raw_output = jc.parsers.universal.simple_table_parse(cleandata)
    #
    #     # otherwise, try bsd style
    #     else:
    #         for line in cleandata:
    #             splitline = line.split()
    #
    #             # Ignore AIX bucket information
    #             if 'bucket:' in splitline[0]:
    #                 continue
    #             elif 'There' in splitline[0] and 'are' in splitline[1]:
    #                 continue
    #
    #             # AIX uses (incomplete)
    #             elif '<incomplete>' not in splitline and '(incomplete)' not in splitline:
    #                 output_line = {
    #                     'name': splitline[0],
    #                     'address': splitline[1].lstrip('(').rstrip(')'),
    #                     'hwtype': splitline[4].lstrip('[').rstrip(']'),
    #                     'hwaddress': splitline[3],
    #                 }
    #                 # Handle permanence and ignore interface in AIX
    #                 if 'permanent' in splitline:
    #                     output_line['permanent'] = True
    #                 elif 'in' not in splitline[6]: # AIX doesn't show interface
    #                     output_line['iface'] = splitline[6]
    #
    #             else:
    #                 output_line = {
    #                     'name': splitline[0],
    #                     'address': splitline[1].lstrip('(').rstrip(')'),
    #                     'hwtype': None,
    #                     'hwaddress': None,
    #                 }
    #                 # AIX doesn't show interface
    #                 if len(splitline) >= 5:
    #                     output_line['iface'] = splitline[5]
    #
    #             raw_output.append(output_line)
    #
    # return raw_output if raw else _process(raw_output)


