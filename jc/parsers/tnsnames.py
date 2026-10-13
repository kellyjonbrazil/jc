r"""jc - JSON Convert Oracle `tnsnames.ora` file parser

Parses `tnsnames.ora` files into one item per net service name. `name` is the
first name in a comma-separated alias list and `aliases` holds every name, with
the connect descriptor containers kept from the file and parameter names
lower-cased. `IFILE` includes become items with the path in `ifile`; they keep
their position in the file and the included files are not read, so you can
resolve the includes yourself.

`#` starts a comment, and a `#` inside quotation marks is part of the value.
The quotation marks around a value are removed. `address`, an `address_list`,
and a `description` under a `DESCRIPTION_LIST` are always lists, since each can
repeat. When a container has a `source_route` parameter its addresses are also
collected in a `hops` list in file order, including addresses inside a nested
`ADDRESS_LIST`, because that order is the route. A top-level scalar that is not
an `IFILE` include has no connect descriptor, so it is not a net service: the
parser skips it and warns instead of turning its left-hand side into a key. A
container that is never closed also ends the parse with a warning.

Usage (cli):

    $ cat tnsnames.ora | jc --tnsnames

Usage (module):

    import jc
    result = jc.parse('tnsnames', tnsnames_file_output)

Schema:

    [
      {
        "name":                       string/null,
        "aliases": [
                                      string        # [0]
        ],
        "description": {                            # [1]
          "source_route":             string,
          "hops": [                                 # [1]
                                      { ... }
          ],
          "load_balance":             string,       # [2]
          "failover":                 string,       # [2]
          "address_list": [                         # [1]
            {
              "load_balance":         string,       # [2]
              "failover":             string,       # [2]
              "address": [
                {
                  "protocol":         string,       # [3]
                  "host":             string,       # [3]
                  "port":             integer,      # [3]
                  "key":              string        # [3]
                }
              ]
            }
          ],
          "connect_data": { ... },                  # [1]
          "security": { ... },                      # [1]
          ...
        },
        "description_list": {                       # [1]
          "description": [
                                      { ... }       # [1]
          ]
        },
        "ifile":                      string        # [4]
      }
    ]

    [0] `name` is the first name in a comma-separated alias list and `aliases`
        holds every name.
    [1] Connect descriptor containers keep the names and nesting from the file.
        `address`, `address_list`, and a `description` under a
        `DESCRIPTION_LIST` are always lists, since each can repeat. `hops` is
        only present when `source_route` is, and holds the addresses in file
        order.
    [2] `load_balance` and `failover` can appear directly under `description`
        as well as under an `address_list`.
    [3] TCP addresses have `protocol`, `host`, and `port`; an IPC address has
        `key` instead. `port` is an integer in processed output and a string in
        raw output.
    [4] `IFILE` items have no net service name, so `name` is null and `aliases`
        is empty. Only the parameters that hold a number are converted to
        integers: `port`, `sdu`, `recv_buf_size`, `send_buf_size`,
        `queuesize`, `retry_count`, `transport_connect_timeout`,
        `connect_timeout`, `retries`, `delay`, and `server_wait_timeout`.

Examples:

    $ cat tnsnames.ora | jc --tnsnames -p
    [
      {
        "name": "SALES",
        "aliases": [
          "SALES"
        ],
        "description": {
          "address_list": [
            {
              "load_balance": "on",
              "failover": "on",
              "address": [
                {
                  "protocol": "tcp",
                  "host": "sales1-svr",
                  "port": 1521
                },
                {
                  "protocol": "tcp",
                  "host": "sales2-svr",
                  "port": 1521
                }
              ]
            }
          ],
          "connect_data": {
            "service_name": "sales.us.example.com",
            "server": "DEDICATED",
            "failover_mode": {
              "type": "SELECT",
              "method": "BASIC",
              "retries": 180,
              "delay": 5
            }
          }
        }
      }
    ]

    Raw output (`-r`) is the same, but numeric parameters such as `port` stay
    strings.
"""
import re
from typing import Any, Dict, List, Tuple
from jc.jc_types import JSONDictType
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = 'Oracle `tnsnames.ora` file parser'
    author = 'Tung Lam'
    author_email = '53996158+tunglambk@users.noreply.github.com'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['file']


__version__ = info.version

# Oracle Net parameters that hold a number. Everything else stays a string so
# a numeric-looking `sid` or `service_name` is not converted.
_int_keys = {
    'port', 'sdu', 'recv_buf_size', 'send_buf_size', 'queuesize',
    'retry_count', 'transport_connect_timeout', 'connect_timeout',
    'retries', 'delay', 'server_wait_timeout'
}

_int_re = re.compile(r'[+-]?\d+')


def _add(node: Dict[str, Any], key: str, value: Any) -> None:
    """Add a parameter to a container, promoting a repeat to a list."""
    if key in node:
        existing = node[key]

        if isinstance(existing, list):
            existing.append(value)
        else:
            node[key] = [existing, value]
    else:
        node[key] = value


def _merge(node: Dict[str, Any], other: Dict[str, Any]) -> None:
    """Merge a container's parameters into the enclosing container."""
    for key, value in other.items():
        if isinstance(node.get(key), list) and isinstance(value, list):
            node[key].extend(value)
        else:
            _add(node, key, value)


def _strip_comments(data: str) -> str:
    """Remove `#` comments, leaving `#` inside quotation marks alone."""
    lines = []

    for line in data.splitlines():
        quote = ''

        for index, char in enumerate(line):
            if quote:
                if char == quote:
                    quote = ''
            elif char in ('"', "'"):
                quote = char
            elif char == '#':
                line = line[:index]
                break

        lines.append(line)

    return '\n'.join(lines)


def _normalize_lists(value: Any, key: str = '') -> None:
    """Make the repeatable `address`, `address_list`, and `description`
    parameters lists.

    `address` can repeat anywhere in a connect descriptor, `address_list` can
    repeat under a `DESCRIPTION`, and `description` repeats under a
    `DESCRIPTION_LIST`. All are lists even when a file only has one, so jq
    paths don't change from one file to the next.
    """
    if isinstance(value, dict):
        for child_key, child_value in value.items():
            repeatable = child_key in ('address', 'address_list') \
                or (child_key == 'description' and key == 'description_list')

            if repeatable and not isinstance(child_value, list):
                child_value = [child_value]
                value[child_key] = child_value

            _normalize_lists(child_value, child_key)
    elif isinstance(value, list):
        for item in value:
            _normalize_lists(item, key)


class _Parser():
    """Recursive-descent parser over the parenthesized file."""

    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.warnings: List[str] = []

    def _warn(self, message: str) -> None:
        if message not in self.warnings:
            self.warnings.append(message)

    def _skip_ws(self) -> None:
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self.pos += 1

    def _skip_line(self) -> str:
        """Read the rest of the current line."""
        start = self.pos

        while self.pos < len(self.text) and self.text[self.pos] != '\n':
            self.pos += 1

        return self.text[start:self.pos]

    def _keyword(self) -> str:
        start = self.pos

        while self.pos < len(self.text) \
                and self.text[self.pos] not in '=()' \
                and not self.text[self.pos].isspace():
            self.pos += 1

        return self.text[start:self.pos]

    def _names(self) -> List[str]:
        """Read the comma-separated net service names up to the `=`."""
        names: List[str] = []

        while True:
            self._skip_ws()
            start = self.pos

            while self.pos < len(self.text) \
                    and self.text[self.pos] not in '=,()' \
                    and not self.text[self.pos].isspace():
                self.pos += 1

            name = self._clean(self.text[start:self.pos])

            if name:
                names.append(name)

            self._skip_ws()

            if self.pos < len(self.text) and self.text[self.pos] == ',':
                self.pos += 1
                continue

            break

        return names

    def _scalar(self) -> str:
        """Read a value up to the closing parenthesis of the current container."""
        start = self.pos

        while self.pos < len(self.text) and self.text[self.pos] != ')':
            self.pos += 1

        return self._clean(self.text[start:self.pos])

    @staticmethod
    def _clean(value: str) -> str:
        value = value.strip()

        if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
            value = value[1:-1].strip()

        return value

    def groups(self) -> Tuple[Dict[str, Any], List[JSONDictType]]:
        """Parse consecutive `( ... )` containers into a single node.

        A value can be spread over several containers, so
        `(ADDRESS = (PROTOCOL = tcp)(HOST = sales-svr))` gives the value of
        `ADDRESS` three parameters rather than one. The addresses found are
        also returned in file order.
        """
        node: Dict[str, Any] = {}
        addresses: List[JSONDictType] = []

        while True:
            self._skip_ws()

            if self.pos >= len(self.text) or self.text[self.pos] != '(':
                break

            child, child_addresses = self.group()
            _merge(node, child)
            addresses.extend(child_addresses)

        if addresses and 'source_route' in node:
            node['hops'] = addresses

        return node, addresses

    def group(self) -> Tuple[Dict[str, Any], List[JSONDictType]]:
        """Parse a `( ... )` container. The position is on the opening `(`."""
        self.pos += 1
        node: Dict[str, Any] = {}
        addresses: List[JSONDictType] = []
        closed = False

        while True:
            self._skip_ws()

            if self.pos >= len(self.text):
                break

            char = self.text[self.pos]

            if char == ')':
                self.pos += 1
                closed = True
                break

            if char == '(':
                # a container with no parameter of its own; its contents belong
                # to the enclosing container
                child, child_addresses = self.groups()
                _merge(node, child)
                addresses.extend(child_addresses)
                continue

            key = self._keyword()
            self._skip_ws()

            if not key or self.pos >= len(self.text) or self.text[self.pos] != '=':
                # not a parameter; step over it so a stray token cannot loop
                if not key:
                    self.pos += 1
                self._warn('Skipped input that is not a `KEY = value` parameter.')
                continue

            self.pos += 1
            self._skip_ws()

            if self.pos < len(self.text) and self.text[self.pos] == '(':
                value, value_addresses = self.groups()
                _add(node, key.lower(), value)

                if key.lower() == 'address':
                    addresses.append(value)
                else:
                    addresses.extend(value_addresses)
            else:
                _add(node, key.lower(), self._scalar())

        if not closed:
            self._warn('A container was not closed before the end of the input. '
                       'The last entry may be incomplete.')

        return node, addresses

    def entries(self) -> List[JSONDictType]:
        """Parse the top-level `name = value` assignments."""
        found: List[JSONDictType] = []

        while True:
            self._skip_ws()

            if self.pos >= len(self.text):
                break

            if self.text[self.pos] == '(':
                # a container with no net service name; nothing to attach it to
                self.group()
                self._warn('Skipped a top-level container that has no net service name.')
                continue

            start = self.pos
            names = self._names()
            self._skip_ws()

            if not names or self.pos >= len(self.text) or self.text[self.pos] != '=':
                # not a parameter; skip the rest of the line so a stray token
                # cannot loop
                self.pos = start
                skipped = self._skip_line().strip()

                if skipped:
                    self._warn(f'Skipped input that is not a net service entry: {skipped!r}')

                continue

            self.pos += 1
            self._skip_ws()

            if names[0].lower() == 'ifile':
                found.append({
                    'name': None,
                    'aliases': [],
                    'ifile': self._clean(self._skip_line())
                })
                continue

            if self.pos < len(self.text) and self.text[self.pos] == '(':
                descriptor, _ = self.groups()
                found.append({'name': names[0], 'aliases': names, **descriptor})
                continue

            # a top-level scalar that is not IFILE; it has no connect
            # descriptor, so keep it out of the schema and warn instead
            value = self._clean(self._skip_line())
            self._warn(f'Skipped top-level scalar `{names[0]} = {value}`. '
                       'It is not a net service entry or IFILE.')

        if not found and not self.warnings:
            self._warn('No net service names found in the input.')

        return found


def _convert(value: Any, key: str = '') -> Any:
    """Recursively convert the numeric parameters of a parsed container."""
    if isinstance(value, dict):
        for child_key, child_value in value.items():
            value[child_key] = _convert(child_value, child_key)
        return value

    if isinstance(value, list):
        return [_convert(item, key) for item in value]

    if key in _int_keys and isinstance(value, str) and _int_re.fullmatch(value):
        return int(value)

    return value


def _process(proc_data: List[JSONDictType]) -> List[JSONDictType]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    for entry in proc_data:
        _convert(entry)

    return proc_data


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
    warnings: List[str] = []

    if jc.utils.has_data(data):
        parser = _Parser(_strip_comments(data))
        raw_output = parser.entries()
        _normalize_lists(raw_output)
        warnings = parser.warnings

    if warnings and not quiet:
        jc.utils.warning_message(warnings)

    return raw_output if raw else _process(raw_output)
