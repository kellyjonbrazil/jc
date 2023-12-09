"""jc - JSON Convert `iftop` command output parser

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
                "host_port":        string, # can be service or missing
                "last_2s":          string,
                "last_10s":         string,
                "last_40s":         string,
                "cumulative":       string,
                "direction":        string
              }
            ]
          }
        ]
        "total_send_rate": {
          "last_2s":                string,
          "last_10s":               string,
          "last_40s":               string
        }
        "total_receive_rate": {
          "last_2s":                string,
          "last_10s":               string,
          "last_40s":               string
        }
        "total_send_and_receive_rate": {
          "last_2s":                string,
          "last_10s":               string,
          "last_40s":               string
        }
        "peak_rate": {
          "last_2s":                string,
          "last_10s":               string,
          "last_40s":               string
        }
        "cumulative_rate": {
          "last_2s":                string,
          "last_10s":               string,
          "last_40s":               string
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
from collections import namedtuple
from numbers import Number


class info:
    """Provides parser metadata (version, author, etc.)"""
    version = "1.0"
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
                        entry[entry_key][one_nesting_item_key] = _parse_size(entry[entry_key][one_nesting_item_key])
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
                                connection[connection_key] = _parse_size(connection[connection_key])
    return proc_data

# _parse_size from https://github.com/xolox/python-humanfriendly

# Copyright (c) 2021 Peter Odding

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Note: this function can be replaced with jc.utils.convert_size_to_int
#       in the future.
def _parse_size(size, binary=False):
    """
    Parse a human readable data size and return the number of bytes.

    :param size: The human readable file size to parse (a string).
    :param binary: :data:`True` to use binary multiples of bytes (base-2) for
                   ambiguous unit symbols and names, :data:`False` to use
                   decimal multiples of bytes (base-10).
    :returns: The corresponding size in bytes (an integer).
    :raises: :exc:`InvalidSize` when the input can't be parsed.

    This function knows how to parse sizes in bytes, kilobytes, megabytes,
    gigabytes, terabytes and petabytes. Some examples:

    >>> from humanfriendly import parse_size
    >>> parse_size('42')
    42
    >>> parse_size('13b')
    13
    >>> parse_size('5 bytes')
    5
    >>> parse_size('1 KB')
    1000
    >>> parse_size('1 kilobyte')
    1000
    >>> parse_size('1 KiB')
    1024
    >>> parse_size('1 KB', binary=True)
    1024
    >>> parse_size('1.5 GB')
    1500000000
    >>> parse_size('1.5 GB', binary=True)
    1610612736
    """
    def tokenize(text):
        tokenized_input = []
        for token in re.split(r'(\d+(?:\.\d+)?)', text):
            token = token.strip()
            if re.match(r'\d+\.\d+', token):
                tokenized_input.append(float(token))
            elif token.isdigit():
                tokenized_input.append(int(token))
            elif token:
                tokenized_input.append(token)
        return tokenized_input

    SizeUnit = namedtuple('SizeUnit', 'divider, symbol, name')
    CombinedUnit = namedtuple('CombinedUnit', 'decimal, binary')
    disk_size_units = (
        CombinedUnit(SizeUnit(1000**1, 'KB', 'kilobyte'), SizeUnit(1024**1, 'KiB', 'kibibyte')),
        CombinedUnit(SizeUnit(1000**2, 'MB', 'megabyte'), SizeUnit(1024**2, 'MiB', 'mebibyte')),
        CombinedUnit(SizeUnit(1000**3, 'GB', 'gigabyte'), SizeUnit(1024**3, 'GiB', 'gibibyte')),
        CombinedUnit(SizeUnit(1000**4, 'TB', 'terabyte'), SizeUnit(1024**4, 'TiB', 'tebibyte')),
        CombinedUnit(SizeUnit(1000**5, 'PB', 'petabyte'), SizeUnit(1024**5, 'PiB', 'pebibyte')),
        CombinedUnit(SizeUnit(1000**6, 'EB', 'exabyte'), SizeUnit(1024**6, 'EiB', 'exbibyte')),
        CombinedUnit(SizeUnit(1000**7, 'ZB', 'zettabyte'), SizeUnit(1024**7, 'ZiB', 'zebibyte')),
        CombinedUnit(SizeUnit(1000**8, 'YB', 'yottabyte'), SizeUnit(1024**8, 'YiB', 'yobibyte')),
    )
    tokens = tokenize(size)
    if tokens and isinstance(tokens[0], Number):
        # Get the normalized unit (if any) from the tokenized input.
        normalized_unit = tokens[1].lower() if len(tokens) == 2 and isinstance(tokens[1], str) else ''
        # If the input contains only a number, it's assumed to be the number of
        # bytes. The second token can also explicitly reference the unit bytes.
        if len(tokens) == 1 or normalized_unit.startswith('b'):
            return int(tokens[0])
        # Otherwise we expect two tokens: A number and a unit.
        if normalized_unit:
            # Convert plural units to singular units, for details:
            # https://github.com/xolox/python-humanfriendly/issues/26
            normalized_unit = normalized_unit.rstrip('s')
            for unit in disk_size_units:
                # First we check for unambiguous symbols (KiB, MiB, GiB, etc)
                # and names (kibibyte, mebibyte, gibibyte, etc) because their
                # handling is always the same.
                if normalized_unit in (unit.binary.symbol.lower(), unit.binary.name.lower()):
                    return int(tokens[0] * unit.binary.divider)
                # Now we will deal with ambiguous prefixes (K, M, G, etc),
                # symbols (KB, MB, GB, etc) and names (kilobyte, megabyte,
                # gigabyte, etc) according to the caller's preference.
                if (normalized_unit in (unit.decimal.symbol.lower(), unit.decimal.name.lower()) or
                        normalized_unit.startswith(unit.decimal.symbol[0].lower())):
                    return int(tokens[0] * (unit.binary.divider if binary else unit.decimal.divider))
    # We failed to parse the size specification.
    return None


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
