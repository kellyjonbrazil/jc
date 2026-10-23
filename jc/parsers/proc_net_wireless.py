r"""jc - JSON Convert `/proc/net/wireless` file parser

Usage (cli):

    $ cat /proc/net/wireless | jc --proc

or

    $ jc /proc/net/wireless

or

    $ cat /proc/net/wireless | jc --proc-net-wireless

Usage (module):

    import jc
    result = jc.parse('proc', proc_net_wireless_file)

or

    import jc
    result = jc.parse('proc_net_wireless', proc_net_wireless_file)

Schema:

    [
      {
        "Iface":                  string,
        "Status":                 integer,
        "QualityLink":            integer,
        "QualityLevel":           integer,
        "QualityNoise":           integer,
        "DiscPktNwid":            integer,
        "DiscPktCrypt":           integer,
        "DiscPktFrag":            integer,
        "DiscPktRetry":           integer,
        "DiscPktMisc":            integer,
        "MissedBeacon":           integer,
      }
  ]

Examples:

    $ cat /proc/net/wireless | jc --proc -p
    [
      {
        "interface": "lo",
        "r_bytes": 13222,
        "r_packets": 152,
        "r_errs": 0,
        "r_drop": 0,
        "r_fifo": 0,
        "r_frame": 0,
        "r_compressed": 0,
        "r_multicast": 0,
        "t_bytes": 13222,
        "t_packets": 152,
        "t_errs": 0,
        "t_drop": 0,
        "t_fifo": 0,
        "t_colls": 0,
        "t_carrier": 0,
        "t_compressed": 0
      },
      ...
    ]

    $ cat /proc/net/wireless | jc --proc-net-wireless -p -r
    [
      {
        "interface": "lo:",
        "r_bytes": "13222",
        "r_packets": "152",
        "r_errs": "0",
        "r_drop": "0",
        "r_fifo": "0",
        "r_frame": "0",
        "r_compressed": "0",
        "r_multicast": "0",
        "t_bytes": "13222",
        "t_packets": "152",
        "t_errs": "0",
        "t_drop": "0",
        "t_fifo": "0",
        "t_colls": "0",
        "t_carrier": "0",
        "t_compressed": "0"
      },
      ...
    ]
"""
from typing import List, Dict
import jc.utils
from jc.parsers.universal import simple_table_parse


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`/proc/net/wireless` file parser'
    author = 'Michael Klemm'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    tags = ['file']
    hidden = True


__version__ = info.version


def _process(proc_data: List[Dict]) -> List[Dict]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    for item in proc_data:
        if 'interface' in item:
            item['interface'] = item['interface'][:-1]

        for key, val in item.items():
            try:
                item[key] = int(val.rstrip('.'))
            except Exception:
                pass

    return proc_data


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> List[Dict]:
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

    raw_output: List = []

    if jc.utils.has_data(data):

        header = 'Iface Status QualityLink QualityLevel QualityNoise DiscPktNwid DiscPktCrypt DiscPktFrag DiscPktRetry DiscPktMisc MissedBeacon'
        data_splitlines = data.splitlines()
        data_splitlines.pop(0)
        data_splitlines[0] = header
        raw_output = simple_table_parse(data_splitlines)

    return raw_output if raw else _process(raw_output)
