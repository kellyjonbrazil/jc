r"""
    jc - JSON Convert Windows `route` command output parser
"""


import re
from typing import List

SEPARATORS = (
    "===========================================================================",
    "  None"
)

# 22...00 50 56 c0 00 01 ......VMware Virtual Ethernet Adapter for VMnet1
# {"id": 22, "mac": "00 50 56 c0 00 01", "name": "VMware Virtual Ethernet Adapter for VMnet1"}
INTERFACE_REGEX = re.compile(
    r"^(?P<id>\d+)\.{3}(?P<mac>.{17})[\s+\.]+(?P<name>[^\n\r]+)$"
)

ROUTE_TABLES = ("IPv4 Route Table", "IPv6 Route Table")
ROUTE_TYPES = ("Active Routes:", "Persistent Routes:")


def get_lines_until_seperator(iterator):
    lines = []
    for line in iterator:
        if line in SEPARATORS:
            break
        lines.append(line)
    return lines


def normalize_route_table(route_table: List[str]):
    headers = route_table[0]
    headers = headers.lower()
    headers = headers.replace("network destination", "destination")
    headers = headers.replace("if", "iface")
    headers = headers.replace("interface", "iface")
    headers = headers.replace("netmask", "genmask")
    headers_count = len(headers.split())

    previous_line_has_all_the_data = True
    normalized_route_table = [headers]
    for row in route_table[1:]:
        row = row.strip()

        has_all_the_data = len(row.split()) == headers_count
        # If the number of columns doesn't match the number of headers in the current and previous line, concatenating them.
        if not has_all_the_data and not previous_line_has_all_the_data:
            previous_line = normalized_route_table.pop(
                len(normalized_route_table) - 1)
            row = f'{previous_line}  {row}'
            has_all_the_data = True

        normalized_route_table.append(row.strip())
        previous_line_has_all_the_data = has_all_the_data

    return normalized_route_table


def parse(cleandata: List[str]):
    """
    Main text parsing function for Windows route

    Parameters:

        cleandata:   (string)  text data to parse

    Returns:

        List of Dictionaries. Raw structured data.
    """

    raw_output = []
    data_iterator = iter(cleandata)
    for line in data_iterator:
        if not line:
            continue

        if line == "Interface List":
            # Interface List
            # 8...00 ff 58 60 5f 61 ......TAP-Windows Adapter V9
            # 52...00 15 5d fd 0d 45 ......Hyper-V Virtual Ethernet Adapter
            # ===========================================================================

            interfaces = []
            for interface_line in data_iterator:
                interface_line = interface_line.strip()
                if interface_line in SEPARATORS:
                    break

                interface_match = INTERFACE_REGEX.search(interface_line)
                if interface_match:
                    interfaces.append(interface_match.groupdict())

            if interfaces:
                raw_output.append({"interfaces": interfaces})
            continue

        full_route_table = []
        if line in ROUTE_TABLES:
            next(data_iterator)  # Skipping the table title.

            # Persistent Routes:
            # Network Address          Netmask  Gateway Address  Metric
            # 157.0.0.0        255.0.0.0      157.55.80.1       3
            # ===========================================================================
            for route_line in data_iterator:
                if route_line in ROUTE_TYPES:
                    import jc.parsers.universal
                    route_table = get_lines_until_seperator(
                        data_iterator
                    )
                    if not route_table:
                        continue

                    route_table = normalize_route_table(
                        route_table
                    )
                    full_route_table.extend(
                        jc.parsers.universal.simple_table_parse(
                            route_table
                        )
                    )

            raw_output.extend(full_route_table)

    return raw_output
