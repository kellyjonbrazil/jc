r"""jc - JSON Convert `~/.ssh/known_hosts`, `ssh-keygen -F`, and `ssh-keyscan` parser

Parses OpenSSH `known_hosts` files as well as the output of `ssh-keygen -F`
and `ssh-keyscan`.

When `ssh-keygen -F` headers (`# Host <host> found: line <N> ...`) are
present, `matched_host` is populated with the matched host from the header
and remains active for consecutive key lines until the next `#` comment line
or blank line. Other comment lines (including `ssh-keyscan` `# host:22 ...`
banners) and blank lines are ignored and reset `matched_host` to `null`.
Note: `ssh-keygen -F -l` fingerprint output is not supported.

Usage (cli):

    $ ssh-keygen -F example.com | jc --known-hosts

or

    $ jc ssh-keygen -F example.com

or

    $ ssh-keyscan example.com | jc --known-hosts

or

    $ cat ~/.ssh/known_hosts | jc --known-hosts

Usage (module):

    import jc
    result = jc.parse('known_hosts', known_hosts_output)

Schema:

    [
      {
        "matched_host":    string/null,
        "hosts": [
                           string
        ],
        "hashed":          boolean,
        "marker":          string/null,
        "type":            string,
        "key":             string,
        "comment":         string/null
      }
    ]

Examples:

    $ cat ~/.ssh/known_hosts | jc --known-hosts -p
    [
      {
        "matched_host": null,
        "hosts": [
          "github.com",
          "140.82.121.3"
        ],
        "hashed": false,
        "marker": null,
        "type": "ssh-ed25519",
        "key": "AAAAC3NzaC1lZDI1NTE5AAAAIOMqqnkVzrm0SdG6UOoqKLsabgH5C9okWi0dh2l9GKJl",
        "comment": "deploy@ci"
      },
      {
        "matched_host": null,
        "hosts": [
          "|1|abc123=|def456="
        ],
        "hashed": true,
        "marker": "@cert-authority",
        "type": "ssh-rsa",
        "key": "AAAAB3NzaC1yc2EAAAADAQABAAABAQC...",
        "comment": null
      }
    ]

    $ cat ~/.ssh/known_hosts | jc --known-hosts -p -r
    [
      {
        "matched_host": null,
        "hosts": "github.com,140.82.121.3",
        "marker": null,
        "type": "ssh-ed25519",
        "key": "AAAAC3NzaC1lZDI1NTE5AAAAIOMqqnkVzrm0SdG6UOoqKLsabgH5C9okWi0dh2l9GKJl",
        "comment": "deploy@ci"
      },
      {
        "matched_host": null,
        "hosts": "|1|abc123=|def456=",
        "marker": "@cert-authority",
        "type": "ssh-rsa",
        "key": "AAAAB3NzaC1yc2EAAAADAQABAAABAQC...",
        "comment": null
      }
    ]
"""
import re
from typing import List, Optional
from jc.jc_types import JSONDictType
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`~/.ssh/known_hosts`, `ssh-keygen -F`, and `ssh-keyscan` parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    magic_commands = ['ssh-keygen -F', 'ssh-keyscan']
    tags = ['command', 'file']


__version__ = info.version

_ASCII_WS_RE = re.compile(r'[ \t]+')
_FOUND_HEADER_RE = re.compile(
    r'^#[ \t]+Host[ \t]+([^ \t]+)[ \t]+found:[ \t]+line[ \t]+[0-9]+(?:[ \t]+.*)?$'
)
_VALID_MARKERS = {'@cert-authority', '@revoked'}


def _process(proc_data: List[JSONDictType]) -> List[JSONDictType]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    processed: List[JSONDictType] = []

    for entry in proc_data:
        hosts_str: str = entry['hosts']
        processed.append({
            'matched_host': entry['matched_host'],
            'hosts': [h for h in hosts_str.split(',') if h],
            'hashed': hosts_str.startswith('|'),
            'marker': entry['marker'],
            'type': entry['type'],
            'key': entry['key'],
            'comment': entry['comment'],
        })

    return processed


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

    raw_output: List[JSONDictType] = []

    if not jc.utils.has_data(data):
        return raw_output

    current_matched_host: Optional[str] = None

    for line in jc.utils.splitlines(data):
        stripped = line.strip(' \t')

        if not stripped:
            current_matched_host = None
            continue

        if stripped.startswith('#'):
            match = _FOUND_HEADER_RE.match(stripped)
            if match:
                current_matched_host = match.group(1)
            else:
                current_matched_host = None
            continue

        parts = _ASCII_WS_RE.split(stripped, maxsplit=1)
        if parts[0] in _VALID_MARKERS:
            marker: Optional[str] = parts[0]
            rest = parts[1] if len(parts) > 1 else ''
        elif parts[0].startswith('@'):
            if not quiet:
                jc.utils.warning_message([f'Skipping line with unrecognized marker: {stripped}'])
            current_matched_host = None
            continue
        else:
            marker = None
            rest = stripped

        fields = _ASCII_WS_RE.split(rest, maxsplit=3)
        if len(fields) < 3 or fields[0].startswith('@') or not fields[0].strip(','):
            if not quiet:
                jc.utils.warning_message([f'Skipping malformed line: {stripped}'])
            current_matched_host = None
            continue

        hosts_str = fields[0]
        key_type = fields[1]
        key = fields[2]
        comment = fields[3] if len(fields) > 3 and fields[3] else None

        raw_output.append({
            'matched_host': current_matched_host,
            'hosts': hosts_str,
            'marker': marker,
            'type': key_type,
            'key': key,
            'comment': comment,
        })

    return raw_output if raw else _process(raw_output)
