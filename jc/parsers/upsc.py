"""jc - JSON Convert `upsc` command output parser

Usage (cli):

    $ upsc ups@localhost | jc --upsc

or

    $ jc upsc ups@localhost

Usage (module):

    import jc
    result = jc.parse('upsc', upsc_command_output)

Schema:

    {
      "battery_charge": integer,
      "battery_voltage": float,
      "device_model": string,
      "ups_status": string
    }

NUT variable names are dynamic. Dots and other non-alphanumeric characters
are converted to underscores and keys are converted to lowercase. In raw mode,
keys are still normalized but all values remain strings. In normal mode,
numeric values are converted to integers or floats, except identifiers, dates,
and version values.
"""
import re
from typing import Any, Dict, Union


class info:
    """Provides parser metadata."""
    version = '1.0'
    description = 'NUT upsc command parser'
    author = 'JC Contributors'
    author_email = 'https://github.com/kellyjonbrazil/jc'
    details = 'https://github.com/kellyjonbrazil/jc/issues/556'
    compatible = ['linux', 'freebsd', 'darwin']
    magic_commands = ['upsc']
    tags = ['command']


_INTEGER_RE = re.compile(r'^[+-]?\d+$')
_FLOAT_RE = re.compile(
    r'^[+-]?(?:\d+\.\d*|\.\d+|\d+[eE][+-]?\d+|'
    r'\d+\.\d*[eE][+-]?\d+|\.\d+[eE][+-]?\d+)$'
)
_STRING_SUFFIXES = (
    'date',
    'model',
    'productid',
    'serial',
    'vendorid',
)


def _normalize_key(key: str) -> str:
    """Return a JSON-friendly representation of a NUT variable name."""
    return re.sub(r'[^a-z0-9_]+', '_', key.lower()).strip('_')


def _convert_value(key: str, value: str) -> Any:
    """Convert measurement values while preserving textual identifiers."""
    key_parts = key.split('.')

    if 'version' in key_parts or key_parts[-1] in _STRING_SUFFIXES:
        return value

    if _INTEGER_RE.fullmatch(value):
        return int(value)

    if _FLOAT_RE.fullmatch(value):
        return float(value)

    return value


def parse(
    data: Union[str, bytes],
    raw: bool = False,
    quiet: bool = False
) -> Dict[str, Any]:
    """Parse `upsc` command output."""
    if isinstance(data, bytes):
        data = data.decode('utf-8')

    result: Dict[str, Any] = {}

    for line in data.splitlines():
        if ':' not in line:
            continue

        source_key, value = line.split(':', 1)
        source_key = source_key.strip()
        normalized_key = _normalize_key(source_key)

        if not normalized_key:
            continue

        value = value.strip()
        result[normalized_key] = (
            value if raw else _convert_value(source_key.lower(), value)
        )

    return result
