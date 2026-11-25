r"""jc - JSON Convert Prometheus and OpenMetrics text format parser

Usage (cli):

    $ curl -s http://localhost:9100/metrics | jc --prometheus

or

    $ cat metrics.txt | jc --prometheus

Usage (module):

    import jc
    result = jc.parse('prometheus', prometheus_metrics_text)

Schema:

    [
      {
        "name":                     string,
        "labels": {
          "<label>":                string
        },
        "value":                    string,
        "value_float":              float,
        "timestamp":                string,
        "timestamp_float":          float,
        "help":                     string,
        "type":                     string,
        "unit":                     string,
        "exemplar": {
          "labels": {
            "<label>":              string
          },
          "value":                  string,
          "value_float":            float,
          "timestamp":              string,
          "timestamp_float":        float
        }
      }
    ]

Examples:

    $ cat metrics.txt | jc --prometheus -p
    [
      {
        "name": "http_requests_total",
        "labels": {
          "method": "post",
          "code": "200"
        },
        "value": "1027",
        "timestamp": "1395066363000",
        "help": "The total number of HTTP requests.",
        "type": "counter",
        "unit": null,
        "exemplar": null,
        "value_float": 1027.0,
        "timestamp_float": 1395066363000.0
      },
      {
        "name": "something_weird",
        "labels": {
          "problem": "division by zero"
        },
        "value": "+Inf",
        "timestamp": "-3982045",
        "help": null,
        "type": null,
        "unit": null,
        "exemplar": null,
        "value_float": null,
        "timestamp_float": -3982045.0
      },
      {
        "name": "http_request_duration_seconds_bucket",
        "labels": {
          "le": "0.05"
        },
        "value": "24054",
        "timestamp": null,
        "help": "A histogram of the request duration.",
        "type": "histogram",
        "unit": null,
        "exemplar": null,
        "value_float": 24054.0,
        "timestamp_float": null
      },
      ...
    ]

    $ cat metrics.txt | jc --prometheus -p -r
    [
      {
        "name": "http_requests_total",
        "labels": {
          "method": "post",
          "code": "200"
        },
        "value": "1027",
        "timestamp": "1395066363000",
        "help": "The total number of HTTP requests.",
        "type": "counter",
        "unit": null,
        "exemplar": null
      },
      {
        "name": "something_weird",
        "labels": {
          "problem": "division by zero"
        },
        "value": "+Inf",
        "timestamp": "-3982045",
        "help": null,
        "type": null,
        "unit": null,
        "exemplar": null
      },
      {
        "name": "http_request_duration_seconds_bucket",
        "labels": {
          "le": "0.05"
        },
        "value": "24054",
        "timestamp": null,
        "help": "A histogram of the request duration.",
        "type": "histogram",
        "unit": null,
        "exemplar": null
      },
      ...
    ]
"""
import re
from typing import List, Dict, Optional, Tuple
from jc.jc_types import JSONDictType
from jc.exceptions import ParseError
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = 'Prometheus and OpenMetrics text format parser'
    author = 'chensimian'
    author_email = 'chensimian@users.noreply.github.com'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['file', 'string']


__version__ = info.version


_IDENTIFIER = re.compile(r'[a-zA-Z_:][a-zA-Z0-9_:]*')
_QUOTED = re.compile(r'"((?:[^"\\]|\\.)*)"')
_METADATA = re.compile(r'#\s*(HELP|TYPE|UNIT)\s+([a-zA-Z_:][a-zA-Z0-9_:]*|"(?:[^"\\]|\\.)*")(?:\s+(.*))?')
_UNESCAPE = re.compile(r'\\(.)')

# sample name suffixes of each metric type. A sample gets the HELP, TYPE, and
# UNIT of the metric family whose name it has, with one of these suffixes.
_TYPE_SUFFIXES = {
    'counter': ('_total', '_created'),
    'histogram': ('_bucket', '_sum', '_count', '_created'),
    'gaugehistogram': ('_bucket', '_gsum', '_gcount'),
    'summary': ('_sum', '_count', '_created'),
    'info': ('_info',)
}
_ALL_SUFFIXES = {x for suffixes in _TYPE_SUFFIXES.values() for x in suffixes}


def _unescape(value: str) -> str:
    """Decode the `\\n`, `\\"`, and `\\\\` escapes, keeping other backslashes"""
    return _UNESCAPE.sub(lambda m: {'n': '\n', '"': '"', '\\': '\\'}.get(m.group(1), m.group(0)), value)


def _parse_label_set(line: str, pos: int, allow_name: bool) -> Tuple[Optional[str], Dict[str, str], int]:
    """
    Parse the `{...}` label set that starts at line[pos]. With allow_name, the
    first item can be a quoted metric name. Returns the metric name (or None),
    the labels, and the position after the closing brace.
    """
    name: Optional[str] = None
    labels: Dict[str, str] = {}
    pos += 1
    first = True

    while True:
        while pos < len(line) and line[pos] in ' \t':
            pos += 1

        if pos < len(line) and line[pos] == '}':
            return name, labels, pos + 1

        quoted = _QUOTED.match(line, pos)
        bare = None if quoted else _IDENTIFIER.match(line, pos)
        token = quoted or bare
        if not token:
            raise ParseError('invalid label set')

        key = _unescape(quoted.group(1)) if quoted else token.group(0)
        pos = token.end()
        while pos < len(line) and line[pos] in ' \t':
            pos += 1

        if pos < len(line) and line[pos] == '=':
            value = _QUOTED.match(line, pos + 1)
            if not value:
                raise ParseError('invalid label value')
            if key in labels:
                raise ParseError(f'duplicate label: {key}')
            labels[key] = _unescape(value.group(1))
            pos = value.end()
        elif quoted and first and allow_name:
            # {"my.dotted.metric", ...}
            name = key
        else:
            raise ParseError('invalid label set')

        first = False
        while pos < len(line) and line[pos] in ' \t':
            pos += 1

        if pos < len(line) and line[pos] == ',':
            pos += 1
        elif pos >= len(line) or line[pos] != '}':
            raise ParseError('invalid label set')


def _parse_sample(line: str) -> Dict:
    """Parse a sample line: name, labels, value, timestamp, and exemplar"""
    name: Optional[str] = None
    labels: Dict[str, str] = {}
    pos = 0

    bare = _IDENTIFIER.match(line)
    if bare:
        name = bare.group(0)
        pos = bare.end()

    if pos < len(line) and line[pos] == '{':
        quoted_name, labels, pos = _parse_label_set(line, pos, allow_name=name is None)
        name = name or quoted_name

    if not name or (pos < len(line) and line[pos] not in ' \t'):
        raise ParseError('invalid metric name')

    rest, _, exemplar_text = line[pos:].partition('#')
    fields = rest.split()
    if len(fields) not in (1, 2):
        raise ParseError('a sample needs a value and an optional timestamp')

    exemplar = None
    if exemplar_text.strip():
        exemplar_text = exemplar_text.strip()
        if not exemplar_text.startswith('{'):
            raise ParseError('invalid exemplar')
        _, exemplar_labels, end = _parse_label_set(exemplar_text, 0, allow_name=False)
        exemplar_fields = exemplar_text[end:].split()
        if len(exemplar_fields) not in (1, 2):
            raise ParseError('invalid exemplar')
        exemplar = {
            'labels': exemplar_labels,
            'value': exemplar_fields[0],
            'timestamp': exemplar_fields[1] if len(exemplar_fields) == 2 else None
        }

    return {
        'name': name,
        'labels': labels,
        'value': fields[0],
        'timestamp': fields[1] if len(fields) == 2 else None,
        'help': None,
        'type': None,
        'unit': None,
        'exemplar': exemplar
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
        for item in (entry, entry['exemplar']):
            if item:
                item['value_float'] = jc.utils.convert_to_float(item['value'])
                item['timestamp_float'] = jc.utils.convert_to_float(item['timestamp'])

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

    raw_output: List[Dict] = []
    metadata: Dict[str, Dict[str, str]] = {}

    if jc.utils.has_data(data):

        for line_num, line in enumerate(jc.utils.splitlines(data), 1):
            line = line.strip()
            if not line:
                continue

            if line.startswith('#'):
                # HELP, TYPE, and UNIT lines. Other comments (and # EOF) are skipped.
                meta = _METADATA.fullmatch(line)
                if meta:
                    kind, name, text = meta.groups()
                    if name.startswith('"'):
                        name = _unescape(name[1:-1])
                    metadata.setdefault(name, {})[kind.lower()] = _unescape(text or '')
                continue

            try:
                raw_output.append(_parse_sample(line))
            except ParseError as e:
                raise ParseError(f'Line {line_num}: {e}: {line}')

        # add the HELP, TYPE, and UNIT of each sample's metric family
        for entry in raw_output:
            name = entry['name']
            family = metadata.get(name)
            if family is None:
                for suffix in _ALL_SUFFIXES:
                    if name.endswith(suffix):
                        meta = metadata.get(name[:-len(suffix)], {})
                        if suffix in _TYPE_SUFFIXES.get(meta.get('type', ''), ()):
                            family = meta
                            break

            if family:
                for key in ('help', 'type', 'unit'):
                    entry[key] = family.get(key)

    return raw_output if raw else _process(raw_output)
