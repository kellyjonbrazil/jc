r"""
    jc - JSON Convert Windows `netstat` command output parser
"""


from typing import Dict, List

POSSIBLE_PROTOCOLS = ("TCP", "UDP", "TCPv6", "UDPv6")

def normalize_headers(headers: str):
    """
        Normalizes the headers to match the jc netstat parser style
        (local_address -> local_address, local_port...).
    """

    headers = headers.lower().strip()
    headers = headers.replace("local address", "local_address")
    headers = headers.replace("foreign address", "foreign_address")
    return headers.split()


def parse(cleandata: List[str]):
    """
    Main text parsing function for Windows netstat

    Parameters:

        cleandata:   (string)  text data to parse

    Returns:

        List of Dictionaries. Raw structured data.
    """

    raw_output = []
    cleandata.pop(0)  # Removing the "Active Connections" header.
    # a run cut short (`netstat -q | head -1`) can end right after the
    # "Active Connections" line, leaving no header row to normalize
    if not cleandata:
        return raw_output
    headers = normalize_headers(cleandata.pop(0))

    # find the state column and the header after it once, not for every row
    state_next_header = None
    has_state = "state" in headers
    if has_state:
        next_index = headers.index("state") + 1
        if len(headers) > next_index:
            state_next_header = headers[next_index]

    for line in cleandata:
        line = line.strip()

        # -b: an owner line's first word is not a protocol (even if it starts with one)
        first_word = line.split(maxsplit=1)[:1]
        if not first_word or first_word[0] not in POSSIBLE_PROTOCOLS:
            # a run cut short can end on an owner line before any connection
            # line was seen, so there is no entry to attach it to
            if not raw_output:
                continue
            line_data = raw_output.pop(len(raw_output) - 1)
            line_data['program_name'] = line
            raw_output.append(line_data)
            continue

        line_data = line.split()
        line_data: Dict[str, str] = dict(zip(headers, line_data))
        for key in list(line_data.keys()):
            if key == "local_address":
                # a run cut short can end a line before its port
                if ":" in line_data[key]:
                    local_address, local_port = line_data[key].rsplit(
                        ":", maxsplit=1)
                    line_data["local_address"] = local_address
                    line_data["local_port"] = local_port
                continue

            if key == "foreign_address":
                # a run cut short can end a line before its port
                if ":" in line_data[key]:
                    foreign_address, foreign_port = line_data[key].rsplit(
                        ":", maxsplit=1)
                    line_data["foreign_address"] = foreign_address
                    line_data["foreign_port"] = foreign_port
                continue

            # There is no state in UDP, so the data after the "state" header will leak.
            if key == "proto" and has_state and line_data["proto"] == "UDP":
                # a run cut short can end a UDP line before the column that
                # leaks into "state", leaving nothing to move
                if state_next_header is not None and "state" in line_data:
                    line_data[state_next_header] = line_data["state"]
                    line_data["state"] = ''

        raw_output.append(line_data)

    return raw_output
