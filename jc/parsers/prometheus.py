"""jc - JSON Convert Prometheus and OpenMetrics parser

This parser converts the Prometheus text exposition format and OpenMetrics
text format into a list of metric samples. Prometheus metadata is added to
each associated sample when available.

Usage (cli):

    $ cat metrics.txt | jc --prometheus

Usage (module):

    >>> import jc
    >>> jc.parse('prometheus', metrics_data)

Schema:

    [
      {
        "name":             string,
        "labels":           object,
        "value":            integer, float, or string,
        "timestamp":        integer or float,
        "help":             string,
        "type":             string,
        "unit":             string,
        "exemplar": {
          "labels":         object,
          "value":          integer, float, or string,
          "timestamp":      integer or float
        }
      }
    ]

The ``timestamp``, metadata, and ``exemplar`` fields are omitted when they
are not present. ``NaN``, ``+Inf``, and ``-Inf`` values are retained as
strings so generated JSON remains standards compliant. With ``raw=True``,
values and timestamps are not converted to numbers.

Examples:

    $ cat metrics.txt | jc --prometheus -p
    [
      {
        "name": "http_requests_total",
        "labels": {
          "method": "post",
          "code": "200"
        },
        "value": 1027,
        "timestamp": 1395066363000,
        "help": "The total number of HTTP requests.",
        "type": "counter"
      }
    ]
"""
import re
from typing import Any, Dict, List, Optional, Tuple, Union


class info:
    """Provides parser metadata."""
    magic_commands = []
    type = 'file'
    arguments = None
    version = '1.0'
    description = 'Prometheus metrics and OpenMetrics text parser'
    author = 'JC Maintainers'
    author_email = None
    compatible = ['linux', 'aix', 'freebsd', 'darwin', 'win32']
    tags = ['file']


_METRIC_NAME = r'[a-zA-Z_:][a-zA-Z0-9_:]*'
_LABEL_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
_NUMBER = re.compile(r'^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?$')
_INTEGER = re.compile(r'^[+-]?\d+$')
_METADATA = re.compile(
    r'^#\s*(HELP|TYPE|UNIT)\s+(' + _METRIC_NAME + r')(?:\s+(.*))?$'
)
_NAME = re.compile(r'^(' + _METRIC_NAME + r')')
_LABEL = re.compile(
    r'\s*(' + _LABEL_NAME + r')\s*=\s*"((?:\\.|[^"\\])*)"\s*'
)
_FAMILY_SUFFIXES = ('_total', '_created', '_bucket', '_sum', '_count', '_info')


def _unescape(value: str) -> str:
    """Unescape the sequences supported by the exposition formats."""
    output: List[str] = []
    index = 0

    while index < len(value):
        if value[index] != '\\' or index + 1 == len(value):
            output.append(value[index])
            index += 1
            continue

        escaped = value[index + 1]
        if escaped == 'n':
            output.append('\n')
        elif escaped in ('\\', '"'):
            output.append(escaped)
        else:
            output.extend(('\\', escaped))
        index += 2

    return ''.join(output)


def _convert_number(value: str, raw: bool) -> Union[str, int, float]:
    if raw or value in ('NaN', '+Inf', '-Inf', 'Inf'):
        return value

    if not _NUMBER.match(value):
        raise ValueError('invalid numeric value: {}'.format(value))

    if _INTEGER.match(value):
        return int(value)

    return float(value)


def _find_closing_brace(value: str, start: int) -> int:
    quoted = False
    escaped = False

    for index in range(start + 1, len(value)):
        character = value[index]
        if escaped:
            escaped = False
        elif character == '\\' and quoted:
            escaped = True
        elif character == '"':
            quoted = not quoted
        elif character == '}' and not quoted:
            return index

    raise ValueError('unterminated label set')


def _parse_labels(value: str) -> Dict[str, str]:
    labels: Dict[str, str] = {}
    position = 0

    while position < len(value):
        match = _LABEL.match(value, position)
        if not match:
            raise ValueError('invalid label set')

        name, label_value = match.groups()
        if name in labels:
            raise ValueError('duplicate label: {}'.format(name))
        labels[name] = _unescape(label_value)
        position = match.end()

        if position == len(value):
            break
        if value[position] != ',':
            raise ValueError('invalid label separator')
        position += 1
        if not value[position:].strip():
            break

    return labels


def _parse_identifier(value: str) -> Tuple[str, Dict[str, str], str]:
    match = _NAME.match(value)
    if not match:
        raise ValueError('invalid metric name')

    name = match.group(1)
    position = match.end()
    labels: Dict[str, str] = {}

    if position < len(value) and value[position] == '{':
        end = _find_closing_brace(value, position)
        labels = _parse_labels(value[position + 1:end])
        position = end + 1

    if position < len(value) and not value[position].isspace():
        raise ValueError('invalid character after metric identifier')

    return name, labels, value[position:].strip()


def _parse_exemplar(value: str, raw: bool) -> Dict[str, Any]:
    value = value.strip()
    if not value.startswith('{'):
        raise ValueError('invalid exemplar')

    end = _find_closing_brace(value, 0)
    labels = _parse_labels(value[1:end])
    fields = value[end + 1:].split()
    if len(fields) not in (1, 2):
        raise ValueError('invalid exemplar fields')

    exemplar: Dict[str, Any] = {
        'labels': labels,
        'value': _convert_number(fields[0], raw)
    }
    if len(fields) == 2:
        exemplar['timestamp'] = _convert_number(fields[1], raw)

    return exemplar


def _parse_sample(line: str, raw: bool) -> Dict[str, Any]:
    name, labels, remainder = _parse_identifier(line)
    exemplar_text: Optional[str] = None

    if '#' in remainder:
        remainder, marker, exemplar_text = remainder.partition('#')
        if marker != '#' or not exemplar_text.strip():
            raise ValueError('invalid exemplar')

    fields = remainder.split()
    if len(fields) not in (1, 2):
        raise ValueError('sample must contain a value and optional timestamp')

    sample: Dict[str, Any] = {
        'name': name,
        'labels': labels,
        'value': _convert_number(fields[0], raw)
    }
    if len(fields) == 2:
        sample['timestamp'] = _convert_number(fields[1], raw)
    if exemplar_text is not None:
        sample['exemplar'] = _parse_exemplar(exemplar_text, raw)

    return sample


def _metadata_for(
    name: str,
    metadata: Dict[str, Dict[str, str]]
) -> Optional[Dict[str, str]]:
    if name in metadata:
        return metadata[name]

    for suffix in _FAMILY_SUFFIXES:
        if name.endswith(suffix) and name[:-len(suffix)] in metadata:
            return metadata[name[:-len(suffix)]]

    return None


def parse(
    data: Union[str, bytes],
    quiet: bool = False,
    raw: bool = False
) -> List[Dict[str, Any]]:
    """Parse Prometheus or OpenMetrics text exposition data."""
    del quiet
    if isinstance(data, bytes):
        data = data.decode('utf-8')
    if not isinstance(data, str):
        raise TypeError('data must be a string or bytes')

    metadata: Dict[str, Dict[str, str]] = {}
    samples: List[Dict[str, Any]] = []

    for line_number, original_line in enumerate(data.splitlines(), 1):
        line = original_line.strip()
        if not line:
            continue

        metadata_match = _METADATA.match(line)
        if metadata_match:
            kind, name, value = metadata_match.groups()
            key = kind.lower()
            metadata.setdefault(name, {})[key] = _unescape(value or '')
            continue

        if line.startswith('#'):
            continue

        try:
            samples.append(_parse_sample(line, raw))
        except ValueError as error:
            raise ValueError('line {}: {}'.format(line_number, error))

    for sample in samples:
        sample_metadata = _metadata_for(sample['name'], metadata)
        if sample_metadata:
            sample.update(sample_metadata)

    return samples
