"""jc - JSON Convert `iftop` command output parser

No `iftop` options are supported.


Usage (cli):

    $ iftop -i <device> -t -P -s 1 | jc --iftop

Usage (module):

    import jc
    result = jc.parse('iftop', iftop_command_output)

Schema:

    [
      {
        "device": string,
        "ip_address": string,
        "mac_address": string,
        "clients": [
            {
                "index": integer,
                "send": {
                    "host_name": string,
                    "host_port": string, # can be service
                    "last_2s": string,
                    "last_10s": string,
                    "last_40s": string,
                    "cumulative": string,
                },
                "receive": {
                    "host_name": string,
                    "host_port": string, # can be service
                    "last_2s": string,
                    "last_10s": string,
                    "last_40s": string,
                    "cumulative": string,
                }
            }
        ]
        "total_send_rate": {
            "last_2s": string,
            "last_10s": string,
            "last_40s": string,
        }
        "total_receive_rate": {
            "last_2s": string,
            "last_10s": string,
            "last_40s": string,
        }
        "total_send_and_receive_rate": {
            "last_2s": string,
            "last_10s": string,
            "last_40s": string,
        }
        "peak_rate": {
            "last_2s": string,
            "last_10s": string,
            "last_40s": string,
        }
        "cumulative_rate": {
            "last_2s": string,
            "last_10s": string,
            "last_40s": string,
        }


Examples:

    $ iftop -i eno0 -t -P -s 1 | jc --iftop -p -r
    [
      {
        "device": eno0,
        "ip_address": "192.168.71.137",
        "mac_address": "11:22:33:44:55:66",
        "clients": [
            {
                "index": 1,
                "send": {
                    "host_name": "host",
                    "host_port": "443"
                    "last_2s": "2.14Mb",
                    "last_10s": "2.14Mb",
                    "last_40s": "2.14Mb",
                    "cumulative": "548KB",
                }
                "receive": {
                    "host_name": "target",
                    "host_port": "51234"
                    "last_2s": "4.79Kb",
                    "last_10s": "4.79Kb",
                    "last_40s": "4.79Kb",
                    "cumulative": "1.20KB",
                }
            }
        ]
        "total_send_rate": {
            "last_2s": "2.14Mb",
            "last_10s": "2.14Mb",
            "last_40s": "2.14Mb",
        }
        "total_receive_rate": {
            "last_2s": "4.79Kb",
            "last_10s": "4.79Kb",
            "last_40s": "4.79Kb",
        }
        "total_send_and_receive_rate": {
            "last_2s": "268.09Kb",
            "last_10s": "268.09Kb",
            "last_40s": "268.09Kb",
        }
        "peak_rate": {
            "last_2s": "2.14Mb",
            "last_10s": "2.14Mb",
            "last_40s": "2.14Mb",
        }
        "cumulative_rate": {
            "last_2s": string,
            "last_10s": string,
            "last_40s": string,
        }
"""
import re
from typing import List, Dict
from jc.jc_types import JSONDictType
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '0.1'
    description = '`iftop` command parser'
    author = 'Ron Green'
    author_email = '11993626+georgettica@users.noreply.github.com'
    compatible = ['linux']
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
    pass


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

    # raw_output: List[Dict] = []

    # for backwards compatibility, preset all fields to None
    interface_obj: Dict = {
        "device": None,
        "ip_address": None,
        "mac_address": None,
        "clients": None,
        "total_send_rate": None,
        "total_receive_rate": None,
        "total_send_and_receive_rate": None,
        "peak_rate": None,
        "cumulative_rate": None,
    }

    interface_item: Dict = interface_obj.copy()  # noqa: F841

    # clients: List = []

    re_linux_device = re.compile(r'''
    Listening\son\s(?P<device>.+)
    ''', re.IGNORECASE | re.VERBOSE)

