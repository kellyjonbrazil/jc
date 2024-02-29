"""jc - JSON Convert `ethtool` command output parser

Usage (cli):

    $ ethtool <interface> | jc --ethtool

or

    $ jc ethtool <interface>

Usage (module):

    import jc
    result = jc.parse('ethtool', ethtool_command_output)

Schema:

    {
      "name":                               string,
      "supported_ports": [
                                            string
      ],
      "supported_link_modes": [
                                            string
      ],
      "supported_pause_frame_use":          string,
      "supports_auto_negotiation":          boolean,
      "supported_fec_modes": [
                                            string
      ],
      "advertised_link_modes": [
                                            string
      ],
      "advertised_pause_frame_use":         boolean,
      "advertised_auto_negotiation":        boolean,
      "advertised_fec_modes": [
                                            string
      ],
      "speed":                              string,
      "speed_bps":                          integer,
      "duplex":                             string,
      "auto_negotiation":                   boolean,
      "port":                               string,
      "phyad":                              string,
      "mdi_x":                              string,
      "transceiver":                        string,
      "supports_wake_on":                   string,
      "wake_on":                            string,
      "current_message_level": [
                                            string
      ],
      "link_detected":                      boolean
    }

Examples:

    $ ethtool | jc --ethtool -p
    []

    $ ethtool | jc --ethtool -p -r
    []
"""
from typing import List, Dict
from jc.jc_types import JSONDictType
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`ethtool` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    tags = ['command']
    magic_commands = ['ethtool']


__version__ = info.version


def _process(proc_data: JSONDictType) -> JSONDictType:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    bool_list = {'supports_auto_negotiation', 'advertised_auto_negotiation',
                 'auto_negotiation', 'link_detected', 'advertised_pause_frame_use'}

    if 'speed' in proc_data:
        proc_data['speed_bps'] = jc.utils.convert_size_to_int(proc_data['speed'])

    for key in bool_list:
        if key in proc_data:
            proc_data[key] = jc.utils.convert_to_bool(proc_data[key])

    return proc_data


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> JSONDictType:
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

    raw_output: Dict = {}
    supported_ports: List[str] = []
    supported_link_modes: List[str] = []
    supported_fec_modes: List[str] = []
    advertised_link_modes: List[str] = []
    advertised_fec_modes: List[str] = []
    current_message_level: List[str] = []
    mode: str = ''    # supported_link_modes, supported_fec_modes, advertised_link_modes,
                      # advertised_fec_modes, current_message_level

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):

            if line.startswith('Settings for '):
                raw_output['name'] = line.split()[2][:-1]
                continue

            data_line = line.replace('\t', ' ')
            if not data_line.startswith('         '):    # 9 spaces
                mode = ''

            if 'Supported ports:' in line:
                _, val = line.split(':', maxsplit=1)
                val = val.strip()[1:-1]
                val_list = val.split()
                supported_ports.extend(val_list)
                continue

            if 'Supported link modes:' in line:
                _, val = line.split(':', maxsplit=1)
                supported_link_modes.append(val.strip())
                mode = 'supported_link_modes'
                continue

            if 'Supported FEC modes:' in line:
                _, val = line.split(':', maxsplit=1)
                supported_fec_modes.append(val.strip())
                mode = 'supported_fec_modes'
                continue

            if 'Advertised link modes:' in line:
                _, val = line.split(':', maxsplit=1)
                advertised_link_modes.append(val.strip())
                mode = 'advertised_link_modes'
                continue

            if 'Advertised FEC modes:' in line:
                _, val = line.split(':', maxsplit=1)
                advertised_fec_modes.append(val.strip())
                mode = 'advertised_fec_modes'
                continue

            if 'Current message level:' in line:
                _, val = line.split(':', maxsplit=1)
                current_message_level.append(val.strip())
                mode = 'current_message_level'
                continue

            if mode == 'supported_link_modes':
                supported_link_modes.append(line.strip())
                continue

            if mode == 'supported_fec_modes':
                supported_fec_modes.append(line.strip())
                continue

            if mode == 'advertised_link_modes':
                advertised_link_modes.append(line.strip())
                continue

            if mode == 'advertised_fec_modes':
                advertised_fec_modes.append(line.strip())
                continue

            if mode == 'current_message_level':
                current_message_level.append(line.strip())
                continue

            key, val = line.split(':', maxsplit=1)
            key = jc.utils.normalize_key(key)
            val = val.strip()
            raw_output[key] = val

        if supported_ports:
            raw_output['supported_ports'] = supported_ports
        if supported_link_modes:
            raw_output['supported_link_modes'] = supported_link_modes
        if supported_fec_modes:
            raw_output['supported_fec_modes'] = supported_fec_modes
        if advertised_link_modes:
            raw_output['advertised_link_modes'] = advertised_link_modes
        if advertised_fec_modes:
            raw_output['advertised_fec_modes'] = advertised_fec_modes
        if current_message_level:
            raw_output['current_message_level'] = current_message_level

    return raw_output if raw else _process(raw_output)
