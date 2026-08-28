r"""jc - JSON Convert `~/.ssh/authorized_keys` file parser

Comment lines (starting with `#`) and blank lines are ignored. The
leading `options` field (e.g. `command="...",no-port-forwarding`) is
optional, as is the trailing `comment` field. Each entry in `options`
is left unparsed (not split into key/value) since values may contain
quoted commas and spaces.

Usage (cli):

    $ cat ~/.ssh/authorized_keys | jc --authorized-keys

Usage (module):

    import jc
    result = jc.parse('authorized_keys', authorized_keys_file_output)

Schema:

    [
      {
        "options": [
                      string
        ],
        "type":     string,
        "key":      string,
        "comment":  string/null
      }
    ]

Examples:

    $ cat ~/.ssh/authorized_keys | jc --authorized-keys -p
    [
      {
        "options": [],
        "type": "ssh-ed25519",
        "key": "AAAAC3NzaC1lZDI1NTE5AAAAIHghxye3Vq/KsZ0sFBplo+n3lp/BWBJyDG2VzlIqynfX",
        "comment": "bob@laptop"
      },
      {
        "options": [
          "command=\"/usr/bin/rsync --server\"",
          "no-port-forwarding"
        ],
        "type": "ssh-rsa",
        "key": "AAAAB3NzaC1yc2EAAAADAQABAAABAQDg0BAJ5uRurdBc7//UY1w4p7cuc8w...",
        "comment": null
      }
    ]
"""
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`~/.ssh/authorized_keys` file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['file']


__version__ = info.version

# the boundary between the optional leading `options` field and the key
# `type` field is the first unquoted whitespace character, so any token
# that doesn't look like a known key type must be the `options` field
_KEY_TYPE_PREFIXES = ('ssh-', 'ecdsa-sha2-', 'sk-ecdsa-sha2-', 'sk-ssh-')


def _quote_aware_split(text, is_delimiter):
    """
    Split text on characters accepted by `is_delimiter`, leaving
    double-quoted spans (which may contain delimiters and
    backslash-escaped quotes) intact.
    """
    tokens = []
    current = []
    in_quotes = False
    escaped = False

    for char in text:
        if escaped:
            current.append(char)
            escaped = False
            continue

        if char == '\\':
            current.append(char)
            escaped = True
            continue

        if char == '"':
            in_quotes = not in_quotes
            current.append(char)
            continue

        if is_delimiter(char) and not in_quotes:
            if current:
                tokens.append(''.join(current))
                current = []
            continue

        current.append(char)

    if current:
        tokens.append(''.join(current))

    return tokens


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured data to conform to the schema.
    """
    # no additional processing needed
    return proc_data


def parse(data, raw=False, quiet=False):
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

    raw_output = []

    if jc.utils.has_data(data):
        for line in data.splitlines():
            line = line.strip()

            if not line or line.startswith('#'):
                continue

            tokens = _quote_aware_split(line, str.isspace)

            if tokens[0].startswith(_KEY_TYPE_PREFIXES):
                options = []
                key_type = tokens[0]
                remaining = tokens[1:]
            else:
                options = _quote_aware_split(tokens[0], lambda c: c == ',')
                key_type = tokens[1] if len(tokens) > 1 else None
                remaining = tokens[2:]

            if not key_type or not remaining:
                continue

            key = remaining[0]
            comment = ' '.join(remaining[1:]) or None

            raw_output.append({
                'options': options,
                'type': key_type,
                'key': key,
                'comment': comment,
            })

    return raw_output if raw else _process(raw_output)
