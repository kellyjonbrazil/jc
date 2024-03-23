r"""jc - JSON Convert `iwconfig` command output parser

No `iwconfig` options are supported.

Usage (cli):

    $ iwconfig | jc --iwconfig

or

    $ jc iwconfig

Usage (module):

    import jc
    result = jc.parse('iwconfig', iwconfig_command_output)

Schema:

    [
        {
            "name":                         string,
            "protocol":                     string,
            "essid":                        string,
            "mode":                         string,
            "frequency":                    float,
            "frequency_unit":               string,
            "access_point":                 string,
            "bit_rate":                     float,
            "bit_rate_unit":                string,
            "tx_power":                     integer,
            "tx_power_unit":                string,
            "retry_short_limit":            integer,
            "rts_threshold":                boolean,
            "fragment_threshold":           boolean,
            "power_management":             boolean,
            "link_quality":                 string,
            "signal_level":                 integer,
            "signal_level_unit":            string,
            "rx_invalid_nwid":              integer,
            "rx_invalid_crypt":             integer,
            "rx_invalid_frag":              integer,
            "tx_excessive_retries":         integer,
            "invalid_misc":                 integer,
            "missed_beacon":                integer
        }
    ]

Examples:

    $  iwconfig | jc --iwconfig -p
    [
      {
        "name": "wlp5s0",
        "protocol": "IEEE 802.11",
        "essid": "BLABLABLA",
        "mode": "Managed",
        "frequency": 5.18,
        "frequency_unit": "GHz",
        "access_point": "E6:64:DA:16:51:BF",
        "bit_rate": 6.0,
        "bit_rate_unit": "Mb/s",
        "tx_power": 30,
        "tx_power_unit": "dBm",
        "retry_short_limit": 7,
        "rts_threshold": false,
        "fragment_threshold": false,
        "power_management": true,
        "link_quality": "61/70",
        "signal_level": -49,
        "signal_level_unit": "dBm",
        "rx_invalid_nwid": 0,
        "rx_invalid_crypt": 0,
        "rx_invalid_frag": 0,
        "tx_excessive_retries": 0,
        "invalid_misc": 2095,
        "missed_beacon": 0
      }
    ]
"""
import re
from typing import List, Dict
from jc.jc_types import JSONDictType
import jc.utils

class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.2'
    description = '`iwconfig` command parser'
    author = 'Thomas Vincent'
    author_email = 'vrince@gmail.com'
    compatible = ['linux']
    magic_commands = ['iwconfig']
    tags = ['command']


__version__ = info.version


def _process(proc_data: List[JSONDictType]) -> List[JSONDictType]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    int_list = [
        'signal_level', 'rx_invalid_nwid', 'rx_invalid_crypt', 'rx_invalid_frag',
        'tx_excessive_retries', 'invalid_misc', 'missed_beacon', 'tx_power', 'retry_short_limit'
    ]
    float_list = ['frequency', 'bit_rate']
    bool_list = ['rts_threshold', 'fragment_threshold', 'power_management']

    proc_data = [ { key: int(value) if key in int_list else value for key, value in proc_data_item.items() } for proc_data_item in proc_data ]
    proc_data = [ { key: float(value) if key in float_list else value for key, value in proc_data_item.items() } for proc_data_item in proc_data ]
    proc_data = [ { key: value == 'on' if key in bool_list else value for key, value in proc_data_item .items() } for proc_data_item in proc_data ]

    return proc_data


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> List[JSONDictType]:
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

    raw_output: List[Dict] = []

    re_interface = re.compile(r'^(?P<name>[a-zA-Z0-9:._\-]+)\s+(?P<protocol>([a-zA-Z0-9]+\s)*[a-zA-Z0-9.]+)\s+ESSID:\"(?P<essid>[a-zA-Z0-9:._\s\-^!#%&\'()*,/:;<>@`{|}~]+)\"')
    re_mode = re.compile(r'Mode:(?P<mode>\w+)')
    re_frequency = re.compile(r'Frequency:(?P<frequency>[0-9.]+)\s(?P<frequency_unit>\w+)')
    re_access_point = re.compile(r'Access Point:\s*(?P<access_point>[0-9A-F:]+)')
    re_bit_rate = re.compile(r'Bit Rate=(?P<bit_rate>[0-9.]+)\s(?P<bit_rate_unit>[\w\/]+)')
    re_tx_power= re.compile(r'Tx-Power=(?P<tx_power>[-0-9]+)\s(?P<tx_power_unit>[\w]+)')
    re_retry_short_limit = re.compile(r'Retry short limit:(?P<retry_short_limit>[0-9\/]+)')
    re_rts_threshold = re.compile(r'RTS thr:(?P<rts_threshold>(off|on))')
    re_fragment_threshold = re.compile(r'Fragment thr:(?P<fragment_threshold>(off|on))')
    re_power_management = re.compile(r'Power Management:(?P<power_management>(off|on))')
    re_link_quality = re.compile(r'Link Quality=(?P<link_quality>[0-9\/]+)')
    re_signal_level = re.compile(r'Signal level=(?P<signal_level>[-0-9]+)\s(?P<signal_level_unit>[\w]+)')
    re_rx_invalid_nwid = re.compile(r'Rx invalid nwid:(?P<rx_invalid_nwid>[-0-9]+)')
    re_rx_invalid_crypt = re.compile(r'Rx invalid crypt:(?P<rx_invalid_crypt>[-0-9]+)')
    re_rx_invalid_frag = re.compile(r'Rx invalid frag:(?P<rx_invalid_frag>[-0-9]+)')
    re_tx_excessive_retries = re.compile(r'Tx excessive retries:(?P<tx_excessive_retries>[-0-9]+)')
    re_invalid_misc = re.compile(r'Invalid misc:(?P<invalid_misc>[0-9]+)')
    re_missed_beacon = re.compile(r'Missed beacon:(?P<missed_beacon>[0-9]+)')

    re_all = [
        re_mode, re_frequency, re_access_point, re_bit_rate, re_tx_power,
        re_retry_short_limit, re_rts_threshold, re_fragment_threshold, re_power_management,
        re_link_quality, re_signal_level, re_rx_invalid_nwid, re_rx_invalid_crypt,
        re_rx_invalid_frag, re_tx_excessive_retries, re_invalid_misc, re_missed_beacon
    ]

    interface_item = None
    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):

            # Find new interface lines
            interface_match = re.search(re_interface, line)
            if interface_match:
                if interface_item is not None:
                    raw_output.append(interface_item)

                interface_item = dict()
                interface_item.update(interface_match.groupdict())
                continue

            # we do not have any interface yet continue to search for it --> next line
            if interface_item is None:
                continue

            # Filling interface with whatever we can find
            for re_entry in re_all:
                match = re.search(re_entry, line)
                if match:
                    interface_item.update(match.groupdict())

    if interface_item is not None:
        raw_output.append(interface_item)

    return raw_output if raw else _process(raw_output)
