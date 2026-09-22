r"""jc - JSON Convert Oracle `tnsnames.ora` file parser

The `tnsnames.ora` file maps net service names to connect descriptors. Each
top-level `name = (DESCRIPTION = ...)` assignment becomes one item, with the
net service name in `name` and the connect descriptor merged in beside it.
`IFILE` includes become items with the path in `ifile` and `name` set to
null. Included files are not read, since the parser only sees the file it is
given.

Container names and nesting stay as written and parameter names are
lower-cased. Values keep the case they are written in. A parameter that
appears more than once in the same container becomes a list, so a container
such as `address` is an object when it holds one protocol address and a list
when it holds several. A container with no parameter of its own, such as the
`((SHARDING_KEY=...)(SUPER_SHARDING_KEY=...))` form, has its contents merged
into the enclosing container.

`#` starts a comment that runs to the end of the line unless it is inside
quotation marks, and the quotation marks around a value are removed. Only the
parameters that hold a number (`port`, `sdu`, `recv_buf_size`, ...) are
converted to integers, so a numeric-looking `sid` or `service_name` stays a
string. Values that contain a closing parenthesis, such as a `SHARDING_KEY_B64`
value, are not handled.

Usage (cli):

    $ cat tnsnames.ora | jc --tnsnames

Usage (module):

    import jc
    result = jc.parse('tnsnames', tnsnames_file_output)

Schema:

    [
      {
        "name":                       string,
        "description": {                            # [0]
          "address_list": {                         # [0]
            "load_balance":           string,
            "failover":               string,
            "address": [
                                      { ... }       # [0]
            ]
          },
          "connect_data": { ... },                  # [0]
          ...                                       # [0]
        },
        "ifile":                      string        # [1]
      }
    ]

    [0] Connect descriptor containers keep the names and nesting from the
        file. A parameter that appears more than once becomes a list.
    [1] `IFILE` items have no net service name, so `name` is null.

Examples:

    $ cat tnsnames.ora | jc --tnsnames -p
    [
      {
        "name": "SALES",
        "description": {
          "address_list": {
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
          },
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

    $ cat tnsnames.ora | jc --tnsnames -p -r
    [
      {
        "name": "SALES",
        "description": {
          "address_list": {
            "load_balance": "on",
            "failover": "on",
            "address": [
              {
                "protocol": "tcp",
                "host": "sales1-svr",
                "port": "1521"
              },
              {
                "protocol": "tcp",
                "host": "sales2-svr",
                "port": "1521"
              }
            ]
          },
          "connect_data": {
            "service_name": "sales.us.example.com",
            "server": "DEDICATED",
            "failover_mode": {
              "type": "SELECT",
              "method": "BASIC",
              "retries": "180",
              "delay": "5"
            }
          }
        }
      }
    ]
"""
import re
from typing import Any, Dict, List
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


class _Parser():
    """Recursive-descent parser over the parenthesized file."""

    def __init__(self, text: str):
        self.text = text
        self.pos = 0

    def _skip_ws(self) -> None:
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self.pos += 1

    def _keyword(self) -> str:
        start = self.pos

        while self.pos < len(self.text) \
                and self.text[self.pos] not in '=()' \
                and not self.text[self.pos].isspace():
            self.pos += 1

        return self.text[start:self.pos]

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

    def groups(self) -> Dict[str, Any]:
        """Parse consecutive `( ... )` containers into a single node.

        A value can be spread over several containers, so
        `(ADDRESS = (PROTOCOL = tcp)(HOST = sales-svr))` gives the value of
        `ADDRESS` three parameters rather than one.
        """
        node: Dict[str, Any] = {}

        while True:
            self._skip_ws()

            if self.pos >= len(self.text) or self.text[self.pos] != '(':
                break

            _merge(node, self.group())

        return node

    def group(self) -> Dict[str, Any]:
        """Parse a `( ... )` container. The position is on the opening `(`."""
        self.pos += 1
        node: Dict[str, Any] = {}

        while True:
            self._skip_ws()

            if self.pos >= len(self.text):
                break

            char = self.text[self.pos]

            if char == ')':
                self.pos += 1
                break

            if char == '(':
                # a container with no parameter of its own; its contents belong
                # to the enclosing container
                _merge(node, self.groups())
                continue

            key = self._keyword()
            self._skip_ws()

            if not key or self.pos >= len(self.text) or self.text[self.pos] != '=':
                # not a parameter; step over it so a stray token cannot loop
                self.pos += 1
                continue

            self.pos += 1
            self._skip_ws()

            if self.pos < len(self.text) and self.text[self.pos] == '(':
                _add(node, key.lower(), self.groups())
            else:
                _add(node, key.lower(), self._scalar())

        return node

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
                continue

            key = self._keyword()
            self._skip_ws()

            if not key or self.pos >= len(self.text) or self.text[self.pos] != '=':
                self.pos += 1
                continue

            self.pos += 1
            self._skip_ws()

            if key.lower() == 'ifile':
                start = self.pos

                while self.pos < len(self.text) and self.text[self.pos] != '\n':
                    self.pos += 1

                found.append({'name': None, 'ifile': self._clean(self.text[start:self.pos])})
                continue

            if self.pos < len(self.text) and self.text[self.pos] == '(':
                found.append({'name': key, **self.groups()})
                continue

            # a top-level scalar that is not IFILE; keep it under its own name
            start = self.pos

            while self.pos < len(self.text) and self.text[self.pos] != '\n':
                self.pos += 1

            found.append({'name': None, key.lower(): self._clean(self.text[start:self.pos])})

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

    if jc.utils.has_data(data):
        raw_output = _Parser(_strip_comments(data)).entries()

    return raw_output if raw else _process(raw_output)
