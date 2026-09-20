r"""jc - JSON Convert `conntrack` command output parser

Parses the default connection tracking table from `conntrack -L` and the
event log from `conntrack -E`. The `expect`, `dying`, and `unconfirmed`
tables and the `-o xml` and `-o save` output formats are not supported.

Each line becomes one item. `-L` listing lines have no event name, so
`event` is `null`, while `-E` lines set `event` to `NEW`, `UPDATE`, or
`DESTROY`. `timeout` and `state` are `null` when conntrack does not print
them: `[DESTROY]` lines drop the timeout and UDP and ICMP entries have no
TCP state.

The original and reply tuples are kept in separate fields. Tuple fields use
the names conntrack prints with an `orig_` or `reply_` prefix, so
protocol-specific fields such as ICMP `type`/`code`/`id` and GRE
`srckey`/`dstkey` are handled the same way. Non-directional trailing fields
(`mark`, `use`, `portid`, ...) keep their own names. Bracket flags such as
`[UNREPLIED]`, `[ASSURED]`, and `[EXPECTED]` are collected in `status`.

With `-o extended` the address family is printed before the protocol
(`ipv4 2 tcp ...`), which populates `family` and `family_number`. With
`-o timestamp` the event time is prepended to event lines, which populates
`event_timestamp`.

Usage (cli):

    $ conntrack -L | jc --conntrack

or

    $ jc conntrack -L

Usage (module):

    import jc
    result = jc.parse('conntrack', conntrack_command_output)

Schema:

    [
      {
        "event":             string/null,
        "event_timestamp":   float/null,
        "family":            string/null,
        "family_number":     integer/null,
        "protocol":          string,
        "protocol_number":   integer,
        "timeout":           integer/null,
        "state":             string/null,
        "status": [
                             string
        ],
        "orig_src":          string,
        "orig_dst":          string,
        "orig_sport":        integer,
        "orig_dport":        integer,
        "reply_src":         string,
        "reply_dst":         string,
        "reply_sport":       integer,
        "reply_dport":       integer,
        "mark":              integer/null,
        "use":               integer/null
      }
    ]

Examples:

    $ conntrack -L | jc --conntrack -p
    [
      {
        "event": null,
        "event_timestamp": null,
        "family": null,
        "family_number": null,
        "protocol": "tcp",
        "protocol_number": 6,
        "timeout": 115,
        "state": "TIME_WAIT",
        "status": [
          "ASSURED"
        ],
        "orig_src": "10.42.0.18",
        "orig_dst": "192.168.67.80",
        "orig_sport": 34884,
        "orig_dport": 9000,
        "reply_src": "192.168.67.80",
        "reply_dst": "192.168.114.132",
        "reply_sport": 9000,
        "reply_dport": 65479,
        "mark": 0,
        "use": 1
      }
    ]

    $ conntrack -E | jc --conntrack -p
    [
      {
        "event": "NEW",
        "event_timestamp": null,
        "family": null,
        "family_number": null,
        "protocol": "tcp",
        "protocol_number": 6,
        "timeout": 120,
        "state": "SYN_SENT",
        "status": [
          "UNREPLIED"
        ],
        "orig_src": "10.42.0.1",
        "orig_dst": "10.42.0.18",
        "orig_sport": 56474,
        "orig_dport": 8080,
        "reply_src": "10.42.0.18",
        "reply_dst": "10.42.0.1",
        "reply_sport": 8080,
        "reply_dport": 56474
      }
    ]
"""
from typing import Dict, List, Optional, Tuple
from jc.jc_types import JSONDictType
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`conntrack` command parser'
    author = 'Tung Lam'
    author_email = '53996158+tunglambk@users.noreply.github.com'
    compatible = ['linux']
    tags = ['command']
    magic_commands = ['conntrack']


__version__ = info.version

# event names printed by `conntrack -E`
_events = ('NEW', 'UPDATE', 'DESTROY')

# conntrack prints the reply tuple with the same field names as the original
# tuple, so the second `src` marks the start of the reply direction
_first_tuple_key = 'src'

# fields that are always numeric when conntrack prints them. Everything else
# in a tuple (addresses, security contexts, labels, ...) stays a string.
_int_keys = {
    'family_number', 'protocol_number', 'timeout',
    'sport', 'dport', 'type', 'code', 'id', 'srckey', 'dstkey',
    'packets', 'bytes', 'mark', 'use', 'portid', 'zone'
}


def _process(proc_data: List[JSONDictType]) -> List[JSONDictType]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    for entry in proc_data:
        for key, value in entry.items():
            if key == 'status':
                continue

            if key == 'event_timestamp':
                entry[key] = jc.utils.convert_to_float(value)
                continue

            base_key = key

            for prefix in ('orig_', 'reply_'):
                if key.startswith(prefix):
                    base_key = key[len(prefix):]
                    break

            if base_key in _int_keys:
                entry[key] = jc.utils.convert_to_int(value)

    return proc_data


def _parse_line(line: str) -> Optional[Dict]:
    """
    Parse a single `conntrack -L` or `conntrack -E` line. Returns `None` if
    the line is not a conntrack tuple, such as the trailing
    `N flow entries have been shown.` summary.
    """
    tokens = line.split()

    if not tokens:
        return None

    event = None
    event_timestamp = None

    # `-E` lines start with the event name; `-o timestamp` puts the event
    # time in front of it
    if tokens[0].startswith('[') and tokens[0].endswith(']'):
        first = tokens[0][1:-1]
        tokens = tokens[1:]

        if first in _events:
            event = first
        else:
            try:
                float(first)
            except ValueError:
                return None

            event_timestamp = first

            if tokens and tokens[0].startswith('[') and tokens[0].endswith(']'):
                event = tokens[0][1:-1]
                tokens = tokens[1:]
            else:
                return None

            if event not in _events:
                return None

    if len(tokens) < 2:
        return None

    protocol = tokens[0]

    if protocol.startswith('[') or '=' in protocol or protocol[0].isdigit():
        return None

    if not tokens[1].isdigit():
        return None

    protocol_number = tokens[1]
    idx = 2
    family = None
    family_number = None

    # `-o extended` prints the address family and its number before the
    # protocol, e.g. `ipv4 2 tcp 6 120 ...`. A TCP state is alphabetic too,
    # but the token after it is the first tuple field rather than a number.
    if (idx + 1 < len(tokens)
            and tokens[idx][0].isalpha()
            and '=' not in tokens[idx]
            and not tokens[idx].startswith('[')
            and tokens[idx + 1].isdigit()):
        family = protocol
        family_number = protocol_number
        protocol = tokens[idx]
        protocol_number = tokens[idx + 1]
        idx += 2

    timeout = None

    if idx < len(tokens) and tokens[idx].isdigit():
        timeout = tokens[idx]
        idx += 1

    state = None

    if idx < len(tokens) and '=' not in tokens[idx] and not tokens[idx].startswith('['):
        state = tokens[idx]
        idx += 1

    status: List[str] = []
    fields: List[Tuple[str, str]] = []

    for token in tokens[idx:]:
        if token.startswith('[') and token.endswith(']'):
            status.append(token[1:-1])
        elif '=' in token:
            key, value = token.split('=', 1)
            fields.append((key, value))
        else:
            return None

    if not fields or fields[0][0] != _first_tuple_key:
        return None

    keys = [key for key, _ in fields]

    try:
        reply_start = keys.index(_first_tuple_key, 1)
    except ValueError:
        return None

    orig = fields[:reply_start]
    reply = fields[reply_start:reply_start + len(orig)]
    extra = fields[reply_start + len(orig):]

    # the reply tuple mirrors the original tuple's fields, so a different
    # sequence means the line was truncated or is not a conntrack tuple
    if [key for key, _ in reply] != keys[:len(orig)]:
        return None

    entry: Dict = {
        'event': event,
        'event_timestamp': event_timestamp,
        'family': family,
        'family_number': family_number,
        'protocol': protocol,
        'protocol_number': protocol_number,
        'timeout': timeout,
        'state': state,
        'status': status
    }

    entry.update({f'orig_{key}': value for key, value in orig})
    entry.update({f'reply_{key}': value for key, value in reply})
    entry.update({key: value for key, value in extra})

    return entry


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

    if jc.utils.has_data(data):
        for line in data.splitlines():
            entry = _parse_line(line)

            if entry is not None:
                raw_output.append(entry)

    return raw_output if raw else _process(raw_output)
