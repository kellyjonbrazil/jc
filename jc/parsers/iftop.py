r"""jc - JSON Convert `iftop` command output parser

Usage (cli):

    $ iftop -i <device> -t -B -s1 | jc --iftop

Usage (module):

    import jc
    result = jc.parse('iftop', iftop_command_output)

Schema:

    [
      {
        "device":                   string,
        "ip_address":               string,
        "mac_address":              string,
        "clients": [
          {
            "index":                integer,
            "connections": [
              {
                "host_name":        string,
                "host_port":        string,   # can be service or missing
                "last_2s":          integer,
                "last_10s":         integer,
                "last_40s":         integer,
                "cumulative":       integer,
                "direction":        string
              }
            ]
          }
        ]
        "total_send_rate": {
          "last_2s":                integer,
          "last_10s":               integer,
          "last_40s":               integer
        }
        "total_receive_rate": {
          "last_2s":                integer,
          "last_10s":               integer,
          "last_40s":               integer
        }
        "total_send_and_receive_rate": {
          "last_2s":                integer,
          "last_10s":               integer,
          "last_40s":               integer
        }
        "peak_rate": {
          "last_2s":                integer,
          "last_10s":               integer,
          "last_40s":               integer
        }
        "cumulative_rate": {
          "last_2s":                integer,
          "last_10s":               integer,
          "last_40s":               integer
        }
      }
    ]

Examples:

    $ iftop -i enp0s3 -t -P -s1 | jc --iftop -p
    [
      {
        "device": "enp0s3",
        "ip_address": "10.10.15.129",
        "mac_address": "08:00:27:c0:4a:4f",
        "clients": [
          {
            "index": 1,
            "connections": [
              {
                "host_name": "ubuntu-2004-clean-01",
                "host_port": "ssh",
                "last_2s": 448,
                "last_10s": 448,
                "last_40s": 448,
                "cumulative": 112,
                "direction": "send"
              },
              {
                "host_name": "10.10.15.72",
                "host_port": "40876",
                "last_2s": 208,
                "last_10s": 208,
                "last_40s": 208,
                "cumulative": 52,
                "direction": "receive"
              }
            ]
          }
        ],
        "total_send_rate": {
          "last_2s": 448,
          "last_10s": 448,
          "last_40s": 448
        },
        "total_receive_rate": {
          "last_2s": 208,
          "last_10s": 208,
          "last_40s": 208
        },
        "total_send_and_receive_rate": {
          "last_2s": 656,
          "last_10s": 656,
          "last_40s": 656
        },
        "peak_rate": {
          "last_2s": 448,
          "last_10s": 208,
          "last_40s": 656
        },
        "cumulative_rate": {
          "last_2s": 112,
          "last_10s": 52,
          "last_40s": 164
        }
      }
    ]

    $ iftop -i enp0s3 -t -P -s1 | jc --iftop -p -r
    [
      {
        "device": "enp0s3",
        "ip_address": "10.10.15.129",
        "mac_address": "11:22:33:44:55:66",
        "clients": [
          {
            "index": 1,
            "connections": [
              {
                "host_name": "ubuntu-2004-clean-01",
                "host_port": "ssh",
                "last_2s": "448b",
                "last_10s": "448b",
                "last_40s": "448b",
                "cumulative": "112B",
                "direction": "send"
              },
              {
                "host_name": "10.10.15.72",
                "host_port": "40876",
                "last_2s": "208b",
                "last_10s": "208b",
                "last_40s": "208b",
                "cumulative": "52B",
                "direction": "receive"
              }
            ]
          }
        ],
        "total_send_rate": {
          "last_2s": "448b",
          "last_10s": "448b",
          "last_40s": "448b"
        },
        "total_receive_rate": {
          "last_2s": "208b",
          "last_10s": "208b",
          "last_40s": "208b"
        },
        "total_send_and_receive_rate": {
          "last_2s": "656b",
          "last_10s": "656b",
          "last_40s": "656b"
        },
        "peak_rate": {
          "last_2s": "448b",
          "last_10s": "208b",
          "last_40s": "656b"
        },
        "cumulative_rate": {
          "last_2s": "112B",
          "last_10s": "52B",
          "last_40s": "164B"
        }
      }
    ]
"""
import re
from typing import List, Dict
from jc.jc_types import JSONDictType
import jc.utils


class info:
    """Provides parser metadata (version, author, etc.)"""
    version = "1.1"
    description = "`iftop` command parser"
    author = "Ron Green"
    author_email = "11993626+georgettica@users.noreply.github.com"
    compatible = ["linux"]
    tags = ["command"]


__version__ = info.version


def _process(proc_data: List[JSONDictType], quiet: bool = False) -> List[JSONDictType]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    string_to_bytes_fields = ["last_2s", "last_10s", "last_40s", "cumulative"]
    one_nesting = [
        "total_send_rate",
        "total_receive_rate",
        "total_send_and_receive_rate",
        "peak_rate",
        "cumulative_rate",
    ]

    if not proc_data:
        return proc_data
    for entry in proc_data:
        # print(f"{entry=}")
        for entry_key in entry:
            # print(f"{entry_key=}")
            if entry_key in one_nesting:
                # print(f"{entry[entry_key]=}")
                for one_nesting_item_key in entry[entry_key]:
                    # print(f"{one_nesting_item_key=}")
                    if one_nesting_item_key in string_to_bytes_fields:
                        entry[entry_key][one_nesting_item_key] = jc.utils.convert_size_to_int(entry[entry_key][one_nesting_item_key])
            elif entry_key == "clients":
                for client in entry[entry_key]:
                    # print(f"{client=}")
                    if "connections" not in client:
                        continue
                    for connection in client["connections"]:
                        # print(f"{connection=}")
                        for connection_key in connection:
                            # print(f"{connection_key=}")
                            if connection_key in string_to_bytes_fields:
                                connection[connection_key] = jc.utils.convert_size_to_int(connection[connection_key])
    return proc_data


def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
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
    interface_item: Dict = {}
    current_client: Dict = {}
    clients: List = []
    is_previous_line_interface = False
    saw_already_host_line = False

    before_arrow = r"\s+(?P<index>\d+)\s+(?P<host_name>[^\s]+):(?P<host_port>[^\s]+)\s+"
    before_arrow_no_port = r"\s+(?P<index>\d+)\s+(?P<host_name>[^\s]+)\s+"
    after_arrow_before_newline = r"\s+(?P<send_last_2s>[^\s]+)\s+(?P<send_last_10s>[^\s]+)\s+(?P<send_last_40s>[^\s]+)\s+(?P<send_cumulative>[^\s]+)"
    newline_before_arrow = r"\s+(?P<receive_ip>.+):(?P<receive_port>\w+)\s+"
    newline_before_arrow_no_port = r"\s+(?P<receive_ip>.+)\s+"
    after_arrow_till_end = r"\s+(?P<receive_last_2s>[^\s]+)\s+(?P<receive_last_10s>[^\s]+)\s+(?P<receive_last_40s>[^\s]+)\s+(?P<receive_cumulative>[^\s]+)"
    re_linux_clients_before_newline = re.compile(
        rf"{before_arrow}=>{after_arrow_before_newline}"
    )
    re_linux_clients_before_newline_no_port = re.compile(
        rf"{before_arrow_no_port}=>{after_arrow_before_newline}"
    )
    re_linux_clients_after_newline_no_port = re.compile(
        rf"{newline_before_arrow_no_port}<={after_arrow_till_end}"
    )

    re_linux_clients_after_newline = re.compile(
        rf"{newline_before_arrow}<={after_arrow_till_end}"
    )

    re_total_send_rate = re.compile(
        r"Total send rate:\s+(?P<total_send_rate_last_2s>[^\s]+)\s+(?P<total_send_rate_last_10s>[^\s]+)\s+(?P<total_send_rate_last_40s>[^\s]+)"
    )
    re_total_receive_rate = re.compile(
        r"Total receive rate:\s+(?P<total_receive_rate_last_2s>[^\s]+)\s+(?P<total_receive_rate_last_10s>[^\s]+)\s+(?P<total_receive_rate_last_40s>[^\s]+)"
    )
    re_total_send_and_receive_rate = re.compile(
        r"Total send and receive rate:\s+(?P<total_send_and_receive_rate_last_2s>[^\s]+)\s+(?P<total_send_and_receive_rate_last_10s>[^\s]+)\s+(?P<total_send_and_receive_rate_last_40s>[^\s]+)"
    )
    re_peak_rate = re.compile(
        r"Peak rate \(sent/received/total\):\s+(?P<peak_rate_sent>[^\s]+)\s+(?P<peak_rate_received>[^\s]+)\s+(?P<peak_rate_total>[^\s]+)"
    )
    re_cumulative_rate = re.compile(
        r"Cumulative \(sent/received/total\):\s+(?P<cumulative_rate_sent>[^\s]+)\s+(?P<cumulative_rate_received>[^\s]+)\s+(?P<cumulative_rate_total>[^\s]+)"
    )

    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    if not jc.utils.has_data(data):
        return raw_output if raw else _process(raw_output, quiet=quiet)

    for line in filter(None, data.splitlines()):
        if line.startswith("interface:"):
            # Example:
            # interface: enp0s3
            interface_item["device"] = line.split(":")[1].strip()

        elif line.startswith("IP address is:"):
            # Example:
            # IP address is: 10.10.15.129
            interface_item["ip_address"] = line.split(":")[1].strip()

        elif line.startswith("MAC address is:"):
            # Example:
            # MAC address is: 08:00:27:c0:4a:4f
            # strip off the "MAC address is: " part
            data_without_front_list = line.split(":")[1:]

            # join the remaining parts back together
            data_without_front = ":".join(data_without_front_list)
            interface_item["mac_address"] = data_without_front.strip()

        elif line.startswith("Listening on"):
            # Example:
            # Listening on enp0s3
            pass

        elif (
            line.startswith("# Host name (port/service if enabled)")
            and not saw_already_host_line
        ):
            saw_already_host_line = True
            # Example:
            #    # Host name (port/service if enabled)            last 2s   last 10s   last 40s cumulative
            pass

        elif (
            line.startswith("# Host name (port/service if enabled)")
            and saw_already_host_line
        ):
            old_interface_item, interface_item = interface_item, {}
            interface_item.update(
                {
                    "device": old_interface_item["device"],
                    "ip_address": old_interface_item["ip_address"],
                    "mac_address": old_interface_item["mac_address"],
                }
            )

        elif "=>" in line and is_previous_line_interface and ":" in line:
            # should not happen
            pass

        elif "=>" in line and not is_previous_line_interface and ":" in line:
            # Example:
            #    1 ubuntu-2004-clean-01:ssh                 =>       448b       448b       448b       112B
            is_previous_line_interface = True
            match_raw = re_linux_clients_before_newline.match(line)

            if not match_raw:
                # this is a bug in iftop
                continue

            match_dict = match_raw.groupdict()
            current_client = {}
            current_client["index"] = int(match_dict["index"])
            current_client["connections"] = []
            current_client_send = {
                "host_name": match_dict["host_name"],
                "host_port": match_dict["host_port"],
                "last_2s": match_dict["send_last_2s"],
                "last_10s": match_dict["send_last_10s"],
                "last_40s": match_dict["send_last_40s"],
                "cumulative": match_dict["send_cumulative"],
                "direction": "send",
            }
            current_client["connections"].append(current_client_send)
            # not adding yet as the receive part is not yet parsed

        elif "=>" in line and not is_previous_line_interface and ":" not in line:
            # should not happen
            pass

        elif "=>" in line and is_previous_line_interface and ":" not in line:
            is_previous_line_interface = True
            match_raw = re_linux_clients_before_newline_no_port.match(line)

            if not match_raw:
                # this is a bug in iftop
                continue

            match_dict = match_raw.groupdict()
            current_client = {}
            current_client["index"] = int(match_dict["index"])
            current_client["connections"] = []
            current_client_send = {
                "host_name": match_dict["host_name"],
                "last_2s": match_dict["send_last_2s"],
                "last_10s": match_dict["send_last_10s"],
                "last_40s": match_dict["send_last_40s"],
                "cumulative": match_dict["send_cumulative"],
                "direction": "send",
            }
            current_client["connections"].append(current_client_send)
            # not adding yet as the receive part is not yet parsed

        elif "<=" in line and not is_previous_line_interface and ":" in line:
            # should not happen
            pass

        elif "<=" in line and is_previous_line_interface and ":" in line:
            # Example:
            #      10.10.15.72:40876                        <=       208b       208b       208b        52B
            is_previous_line_interface = False
            match_raw = re_linux_clients_after_newline.match(line)

            if not match_raw:
                # this is a bug in iftop
                continue

            match_dict = match_raw.groupdict()
            current_client_receive = {
                "host_name": match_dict["receive_ip"],
                "host_port": match_dict["receive_port"],
                "last_2s": match_dict["receive_last_2s"],
                "last_10s": match_dict["receive_last_10s"],
                "last_40s": match_dict["receive_last_40s"],
                "cumulative": match_dict["receive_cumulative"],
                "direction": "receive",
            }

            current_client["connections"].append(current_client_receive)
            clients.append(current_client)

        elif "<=" in line and not is_previous_line_interface and ":" not in line:
            # should not happen
            pass

        elif "<=" in line and is_previous_line_interface and ":" not in line:
            # Example:
            #      10.10.15.72:40876                        <=       208b       208b       208b        52B
            is_previous_line_interface = False
            match_raw = re_linux_clients_after_newline_no_port.match(line)

            if not match_raw:
                # this is a bug in iftop
                continue

            match_dict = match_raw.groupdict()
            current_client_receive = {
                "host_name": match_dict["receive_ip"],
                "last_2s": match_dict["receive_last_2s"],
                "last_10s": match_dict["receive_last_10s"],
                "last_40s": match_dict["receive_last_40s"],
                "cumulative": match_dict["receive_cumulative"],
                "direction": "receive",
            }

            current_client["connections"].append(current_client_receive)
            clients.append(current_client)

        # check if all of the characters are dashes or equal signs
        elif all(c == "-" for c in line):
            pass

        elif line.startswith("Total send rate"):
            # Example:
            # Total send rate:                                       448b       448b       448b
            match_raw = re_total_send_rate.match(line)

            if not match_raw:
                # this is a bug in iftop
                continue

            match_dict = match_raw.groupdict()
            interface_item["total_send_rate"] = {}
            interface_item["total_send_rate"].update(
                {
                    "last_2s": match_dict["total_send_rate_last_2s"],
                    "last_10s": match_dict["total_send_rate_last_10s"],
                    "last_40s": match_dict["total_send_rate_last_40s"],
                }
            )

        elif line.startswith("Total receive rate"):
            # Example:
            # Total receive rate:                                    208b       208b       208b
            match_raw = re_total_receive_rate.match(line)

            if not match_raw:
                # this is a bug in iftop
                continue

            match_dict = match_raw.groupdict()
            interface_item["total_receive_rate"] = {}
            interface_item["total_receive_rate"].update(
                {
                    "last_2s": match_dict["total_receive_rate_last_2s"],
                    "last_10s": match_dict["total_receive_rate_last_10s"],
                    "last_40s": match_dict["total_receive_rate_last_40s"],
                }
            )

        elif line.startswith("Total send and receive rate"):
            # Example:
            # Total send and receive rate:                           656b       656b       656b
            match_raw = re_total_send_and_receive_rate.match(line)

            if not match_raw:
                # this is a bug in iftop
                continue

            match_dict = match_raw.groupdict()
            interface_item["total_send_and_receive_rate"] = {}
            interface_item["total_send_and_receive_rate"].update(
                {
                    "last_2s": match_dict["total_send_and_receive_rate_last_2s"],
                    "last_10s": match_dict["total_send_and_receive_rate_last_10s"],
                    "last_40s": match_dict["total_send_and_receive_rate_last_40s"],
                }
            )

        elif line.startswith("Peak rate"):
            match_raw = re_peak_rate.match(line)

            if not match_raw:
                # this is a bug in iftop
                continue

            match_dict = match_raw.groupdict()
            interface_item["peak_rate"] = {}
            interface_item["peak_rate"].update(
                {
                    "last_2s": match_dict["peak_rate_sent"],
                    "last_10s": match_dict["peak_rate_received"],
                    "last_40s": match_dict["peak_rate_total"],
                }
            )

        elif line.startswith("Cumulative"):
            match_raw = re_cumulative_rate.match(line)

            if not match_raw:
                # this is a bug in iftop
                continue

            match_dict = match_raw.groupdict()
            interface_item["cumulative_rate"] = {}
            interface_item["cumulative_rate"].update(
                {
                    "last_2s": match_dict["cumulative_rate_sent"],
                    "last_10s": match_dict["cumulative_rate_received"],
                    "last_40s": match_dict["cumulative_rate_total"],
                }
            )

        elif all(c == "=" for c in line):
            interface_item["clients"] = clients
            clients = []
            # keep the copy here as without it keeps the objects linked
            raw_output.append(interface_item.copy())

    return raw_output if raw else _process(raw_output, quiet=quiet)
