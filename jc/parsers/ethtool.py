r"""jc - JSON Convert `ethtool` command output parser

Supports standard `ethtool` output and the `--module-info` option.

Usage (cli):

    $ ethtool <interface> | jc --ethtool
    $ ethtool --module-info <interface> | jc --ethtool

or

    $ jc ethtool <interface>
    $ jc ethtool --module-info <interface>

Usage (module):

    import jc
    result = jc.parse('ethtool', ethtool_command_output)

Schema:

Note: many units fields are converted to integers and floats
when detected. Use raw output for the original string values.

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
      "link_detected":                      boolean,
      "identifier":                         string,
      "extended_identifier":                string,
      "connector":                          string,
      "transceiver_codes":                  string,
      "transceiver_type": [
                                            string
      ],
      "encoding":                           string,
      "br_nominal":                         string,
      "rate_identifier":                    string,
      "length_smf_km":                      string,
      "length_smf":                         string,
      "length_50um":                        string,
      "length_62_5um":                      string,
      "length_copper":                      string,
      "length_om3":                         string,
      "passive_cu_cmplnce":                 string,
      "vendor_name":                        string,
      "vendor_oui":                         string,
      "vendor_pn":                          string,
      "vendor_rev":                         string,
      "option_values":                      string,
      "br_margin_max":                      string,
      "br_margin_min":                      string
    }

Examples:

    $ ethtool enp0s3 | jc --ethtool -p
    {
      "name": "enp0s3",
      "supported_pause_frame_use": "No",
      "supports_auto_negotiation": true,
      "supported_fec_modes": "Not reported",
      "advertised_pause_frame_use": false,
      "advertised_auto_negotiation": true,
      "advertised_fec_modes": "Not reported",
      "speed": "1000Mb/s",
      "duplex": "Full",
      "port": "Twisted Pair",
      "phyad": "0",
      "transceiver": "internal",
      "auto_negotiation": false,
      "mdi_x": "off (auto)",
      "supports_wake_on": "umbg",
      "wake_on": "d",
      "link_detected": true,
      "supported_ports": [
        "TP"
      ],
      "supported_link_modes": [
        "10baseT/Half",
        "10baseT/Full",
        "100baseT/Half",
        "100baseT/Full",
        "1000baseT/Full"
      ],
      "advertised_link_modes": [
        "10baseT/Half",
        "10baseT/Full",
        "100baseT/Half",
        "100baseT/Full",
        "1000baseT/Full"
      ],
      "current_message_level": [
        "0x00000007 (7)",
        "drv probe link"
      ],
      "speed_bps": 1000000000
    }

    $ ethtool --module-info enp0s3 | jc --ethtool -p
    {
      "identifier": "0x03 (SFP)",
      "extended_identifier": "0x04 (GBIC/SFP defined by 2-wire interface ID)",
      "connector": "0x21 (Copper pigtail)",
      "transceiver_codes": "0x01 0x00 0x00 0x04 0x00 0x04 0x80 0xd5 0x00",
      "transceiver_type": [
        "Infiniband: 1X Copper Passive",
        "Ethernet: 1000BASE-CX",
        "Passive Cable",
        "FC: Twin Axial Pair (TW)",
        "FC: 1200 MBytes/sec",
        "FC: 800 MBytes/sec",
        "FC: 400 MBytes/sec",
        "FC: 200 MBytes/sec",
        "FC: 100 MBytes/sec"
      ],
      "encoding": "0x00 (unspecified)",
      "br_nominal": "10300MBd",
      "rate_identifier": "0x00 (unspecified)",
      "length_smf_km": "0km",
      "length_smf": "0m",
      "length_50um": "0m",
      "length_62_5um": "0m",
      "length_copper": "2m",
      "length_om3": "0m",
      "passive_cu_cmplnce": "0x01 (SFF-8431 appendix E) [SFF-8472 rev10.4 only]",
      "vendor_name": "UbiquitiNetworks",
      "vendor_oui": "00:40:20",
      "vendor_pn": "UDC-2",
      "vendor_rev": "",
      "option_values": "0x00 0x00",
      "br_margin_max": "0%",
      "br_margin_min": "0%"
    }
"""
import re
from typing import List, Dict
from jc.jc_types import JSONDictType
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.1'
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

    # find and convert units
    # "0.0468 mW / -13.30 dBm" or "-40.00 degrees C / -40.00 degrees F"
    degrees_re = re.compile(r'(?P<deg_c>.*?) degrees C \/ (?P<deg_f>.*?) degrees F')
    power_re = re.compile(r'(?P<pow_mw>.*?) mW \/ (?P<pow_dbm>.*?) dBm')

    for key, val in proc_data.copy().items():
        if isinstance(val, str):
            degrees_match = re.match(degrees_re, val)
            if degrees_match:
                degrees_dict = degrees_match.groupdict()
                proc_data[key + '_celsius'] = float(degrees_dict['deg_c'])
                proc_data[key + '_farenheit'] = float(degrees_dict['deg_f'])
                del proc_data[key]
                continue

            power_match = re.match(power_re, val)
            if power_match:
                power_dict = power_match.groupdict()
                proc_data[key + '_mw'] = float(power_dict['pow_mw'])
                proc_data[key + '_dbm'] = float(power_dict['pow_dbm'])
                del proc_data[key]
                continue

            if val.endswith(' V'):
                proc_data[key + '_v'] = jc.utils.convert_to_float(val)
                del proc_data[key]
                continue

            if val.endswith(' mA'):
                proc_data[key + '_ma'] = jc.utils.convert_to_float(val)
                del proc_data[key]
                continue

    return proc_data


def _parse_default(data: str) -> JSONDictType:
    raw_output: Dict = {}
    supported_ports: List[str] = []
    supported_link_modes: List[str] = []
    supported_fec_modes: List[str] = []
    advertised_link_modes: List[str] = []
    link_partner_advertised_link_modes: List[str] = []
    advertised_fec_modes: List[str] = []
    current_message_level: List[str] = []
    mode: str = ''  # supported_link_modes, supported_fec_modes, advertised_link_modes,
                    # link_partner_advertised_link_modes, advertised_fec_modes, current_message_level

    for line in filter(None, data.splitlines()):

        if line.startswith('Settings for '):
            raw_output['name'] = line.split()[2][:-1]
            continue

        data_line = line.replace('\t', '    ')
        if not data_line.startswith('         '):  # 9 spaces
            mode = ''

        if 'Supported ports:' in line:
            _, val = line.split(':', maxsplit=1)
            val = val.strip()[1:-1]
            val_list = val.split()
            supported_ports.extend(val_list)
            continue

        if 'Supported link modes:' in line and 'Not reported' not in line:
            _, val = line.split(':', maxsplit=1)
            val = val.strip()
            val_list = val.split()
            supported_link_modes.extend(val_list)
            mode = 'supported_link_modes'
            continue

        if 'Supported FEC modes:' in line and 'Not reported' not in line:
            _, val = line.split(':', maxsplit=1)
            val = val.strip()
            val_list = val.split()
            supported_fec_modes.extend(val_list)
            mode = 'supported_fec_modes'
            continue

        if 'Advertised link modes:' in line and 'Not reported' not in line:
            _, val = line.split(':', maxsplit=1)
            val = val.strip()
            val_list = val.split()
            advertised_link_modes.extend(val_list)
            mode = 'advertised_link_modes'
            continue

        if 'Link partner advertised link modes:' in line and 'Not reported' not in line:
            _, val = line.split(':', maxsplit=1)
            val = val.strip()
            val_list = val.split()
            link_partner_advertised_link_modes.extend(val_list)
            mode = 'link_partner_advertised_link_modes'
            continue

        if 'Advertised FEC modes:' in line and 'Not reported' not in line:
            _, val = line.split(':', maxsplit=1)
            val = val.strip()
            val_list = val.split()
            advertised_fec_modes.extend(val_list)
            mode = 'advertised_fec_modes'
            continue

        if 'Current message level:' in line:
            _, val = line.split(':', maxsplit=1)
            current_message_level.append(val.strip())
            mode = 'current_message_level'
            continue

        if mode == 'supported_link_modes':
            val = line.strip()
            val_list = val.split()
            supported_link_modes.extend(val_list)
            continue

        if mode == 'supported_fec_modes':
            val = line.strip()
            val_list = val.split()
            supported_fec_modes.extend(val_list)
            continue

        if mode == 'advertised_link_modes':
            val = line.strip()
            val_list = val.split()
            advertised_link_modes.extend(val_list)
            continue

        if mode == 'link_partner_advertised_link_modes':
            val = line.strip()
            val_list = val.split()
            link_partner_advertised_link_modes.extend(val_list)
            continue

        if mode == 'advertised_fec_modes':
            val = line.strip()
            val_list = val.split()
            advertised_fec_modes.extend(val_list)
            continue

        if mode == 'current_message_level':
            current_message_level.append(line.strip())
            continue

        key, val = line.split(':', maxsplit=1)
        key = jc.utils.normalize_key(key)
        val = val.strip()
        raw_output[key] = val

    list_vals = [
        (supported_ports, 'supported_ports'),
        (supported_link_modes, 'supported_link_modes'),
        (supported_fec_modes, 'supported_fec_modes'),
        (advertised_link_modes, 'advertised_link_modes'),
        (link_partner_advertised_link_modes, 'link_partner_advertised_link_modes'),
        (advertised_fec_modes, 'advertised_fec_modes'),
        (current_message_level, 'current_message_level')
    ]

    for obj_list, obj_key in list_vals:
        if raw_output.get(obj_key, '').lower() == 'not reported':
            raw_output[obj_key] = []
        else:
            if obj_list:
                raw_output[obj_key] = obj_list

    return raw_output


def _parse_module_info(data: str) -> JSONDictType:
    raw_output: Dict = {}
    previous_key: str = ''
    multi_value: List[str] = []

    for line in filter(None, data.splitlines()):
        key, val = line.strip().split(':', maxsplit=1)
        key = jc.utils.normalize_key(key)
        val = val.strip()

        if key == previous_key:
            multi_value.append(val)
            continue

        else:
            if len(multi_value) > 1:
                raw_output[previous_key] = multi_value
                multi_value = []
                multi_value.append(val)
                previous_key = key
                continue

            elif len(multi_value) == 1:
                raw_output[previous_key] = multi_value[0]
                multi_value = []
                multi_value.append(val)
                previous_key = key
                continue

            else:
                raw_output[previous_key] = ''
                multi_value.append(val)
                previous_key = key
                continue

    if len(multi_value) > 1:
        raw_output[key] = multi_value

    elif len(multi_value) == 1:
        raw_output[key] = multi_value[0]

    else:
        raw_output[key] = ''

    if '' in raw_output:
        del raw_output['']

    return raw_output


def parse(data: str, raw: bool = False, quiet: bool = False) -> JSONDictType:
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

    if jc.utils.has_data(data):

        if data.strip().startswith('Settings for '):
            raw_output = _parse_default(data)

        elif data.strip().startswith('Identifier '):
            raw_output = _parse_module_info(data)

    return raw_output if raw else _process(raw_output)
