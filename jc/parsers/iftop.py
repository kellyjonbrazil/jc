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


    re_linux_device = re.compile(r'interface:\s+(?P<device>.+)')
    re_linux_ip = re.compile(r'IP address is:\s+(?P<ip_address>.+)')
    re_linux_mac = re.compile(r'MAC address is:\s+(?P<mac_address>.+)')
    before_arrow = r'(?P<index>\d+)\s+(?P<host_name>.+):(?P<host_port>\w+)\s+'
    after_arrow_before_newline = r'\s+(?P<send_last_2s>[^\s]+)\s+(?P<send_last_10s>[^\s]+)\s+(?P<send_last_40s>[^\s]+)\s+(?P<send_cumulative>[^\s]+)'
    newline_before_arrow = r'\s+(?P<receive_ip>.+):(?P<receive_port>\w+)\s+'
    after_arrow_till_end =r'\s+(?P<receive_last_2s>[^\s]+)\s+(?P<receive_last_10s>[^\s]+)\s+(?P<receive_last_40s>[^\s]+)\s+(?P<receive_cumulative>[^\s]+)'
    re_linux_clients = re.compile(f'{before_arrow}=>{after_arrow_before_newline}{newline_before_arrow}<={after_arrow_till_end}', re.MULTILINE)
    re_total_send_rate = re.compile(r'Total send rate:\s+(?P<total_send_rate_last_2s>[^\s]+)\s+(?P<total_send_rate_last_10s>[^\s]+)\s+(?P<total_send_rate_last_40s>[^\s]+)')
    re_total_receive_rate = re.compile(r'Total receive rate:\s+(?P<total_receive_rate_last_2s>[^\s]+)\s+(?P<total_receive_rate_last_10s>[^\s]+)\s+(?P<total_receive_rate_last_40s>[^\s]+)')
    re_total_send_and_receive_rate = re.compile(r'Total send and receive rate:\s+(?P<total_send_and_receive_rate_last_2s>[^\s]+)\s+(?P<total_send_and_receive_rate_last_10s>[^\s]+)\s+(?P<total_send_and_receive_rate_last_40s>[^\s]+)')
    re_peak_rate = re.compile(r'Peak rate \(sent/received/total\):\s+(?P<peak_rate_sent>[^\s]+)\s+(?P<peak_rate_received>[^\s]+)\s+(?P<peak_rate_total>[^\s]+)')
    re_cumulative_rate = re.compile(r'Cumulative \(sent/received/total\):\s+(?P<cumulative_rate_sent>[^\s]+)\s+(?P<cumulative_rate_received>[^\s]+)\s+(?P<cumulative_rate_total>[^\s]+)')

    if not jc.utils.has_data(data):
        return []

    linux_device_match = re_linux_device.match(data)["device"]
    linux_ip_match = re_linux_ip.match(data)["ip_address"]
    linux_mac_match = re_linux_mac.match(data)["mac_address"]

    total_send_rate_match = re_total_send_rate.match(data)
    total_receive_rate_match = re_total_receive_rate.match(data)
    total_send_and_receive_rate_match = re_total_send_and_receive_rate.match(data)

    peak_rate_match = re_peak_rate.match(data)
    cumulative_rate_match = re_cumulative_rate.match(data)

    interface_obj["device"] = linux_device_match
    interface_obj["ip_address"] = linux_ip_match
    interface_obj["mac_address"] = linux_mac_match
    
    interface_obj["clients"] = []
    print(data)
    # breakpoint()
    
    matches = re_linux_clients.finditer(data)
    for match in matches:
        current_client = {}
        groupdict = match.groupdict()
        current_client["index"] = groupdict["index"]
        current_client["send_host_name"] = groupdict["host_name"]
        current_client["send_host_port"] = groupdict["host_port"]
        current_client["send_last_2s"] = groupdict["send_last_2s"]
        current_client["send_last_10s"] = groupdict["send_last_10s"]
        current_client["send_last_40s"] = groupdict["send_last_40s"]
        current_client["send_cumulative"] = groupdict["send_cumulative"]
        current_client["receive_ip"] = groupdict["receive_ip"]
        current_client["receive_port"] = groupdict["receive_port"]
        current_client["receive_last_2s"] = groupdict["receive_last_2s"]
        current_client["receive_last_10s"] = groupdict["receive_last_10s"]
        current_client["receive_last_40s"] = groupdict["receive_last_40s"]
        current_client["receive_cumulative"] = groupdict["receive_cumulative"]
        interface_obj["clients"].append(current_client)

    interface_obj["total_send_rate"] = {
        "last_2s": total_send_rate_match["total_send_rate_last_2s"],
        "last_10s": total_send_rate_match["total_send_rate_last_10s"],
        "last_40s": total_send_rate_match["total_send_rate_last_40s"],
    }

    interface_obj["total_receive_rate"] = {
        "last_2s": total_receive_rate_match["total_receive_rate_last_2s"],
        "last_10s": total_receive_rate_match["total_receive_rate_last_10s"],
        "last_40s": total_receive_rate_match["total_receive_rate_last_40s"],
    }

    interface_obj["total_send_and_receive_rate"] = {
        "last_2s": total_send_and_receive_rate_match["total_send_and_receive_rate_last_2s"],
        "last_10s": total_send_and_receive_rate_match["total_send_and_receive_rate_last_10s"],
        "last_40s": total_send_and_receive_rate_match["total_send_and_receive_rate_last_40s"],
    }

    interface_obj["peak_rate"] = {
        "last_2s": peak_rate_match["peak_rate_sent"],
        "last_10s": peak_rate_match["peak_rate_received"],
        "last_40s": peak_rate_match["peak_rate_total"],
    }

    interface_obj["cumulative_rate"] = {
        "last_2s": cumulative_rate_match["cumulative_rate_sent"],
        "last_10s": cumulative_rate_match["cumulative_rate_received"],
        "last_40s": cumulative_rate_match["cumulative_rate_total"],
    }
