r"""jc - JSON Convert `ics` file parser

Parses iCalendar (RFC 5545) files.

- `VEVENT`, `VTODO` and `VJOURNAL` components are converted; other components
  are ignored.
- `VALARM` blocks are read as part of the component they belong to.
- Folded lines (a line continued with a leading space or tab) are unfolded,
  `TEXT` escapes (`\n`, `\,`, `\;`, `\\`) are resolved, and the `VALUE=DATE`,
  `VALUE=DATE-TIME` and `TZID` forms of the date properties are supported.
- `RRULE` is passed through, not expanded into occurrences, and properties
  that are not in the schema are dropped.

> Note: Date and time values are normalized to ISO 8601 in the output. Use the
> `-r` command-line argument or the `raw=True` argument in `parse()` to keep
> the original iCalendar values.

Usage (cli):

    $ cat calendar.ics | jc --ics

or

    $ jc calendar.ics

Usage (module):

    import jc
    result = jc.parse('ics', ics_file_output)

Schema:

    [
      {
        "type":             string,   # VEVENT, VTODO or VJOURNAL
        "uid":              string,
        "summary":          string,
        "description":      string,
        "location":         string,
        "url":              string,
        "status":           string,
        "dtstart":          string,   # ISO 8601
        "dtend":            string,
        "due":              string,
        "duration":         string,
        "dtstamp":          string,
        "created":          string,
        "last_modified":    string,
        "sequence":         integer,
        "categories":       [
                              string
                            ],
        "organizer":        string,   # [CN] <address>
        "attendees":        [
                              string
                            ],
        "rrule":            string,
        "rdate":            [
                              string
                            ],
        "exdate":           [
                              string
                            ],
        "alarms":           [
                              {
                                "action":       string,
                                "trigger":      string,
                                "description":  string
                              }
                            ]
      }
    ]

Examples:

    $ cat example.ics
    BEGIN:VCALENDAR
    BEGIN:VEVENT
    UID:42
    SUMMARY:Standup
    DTSTART:20261015T090000Z
    END:VEVENT
    END:VCALENDAR

    $ cat example.ics | jc --ics -p
    [
      {
        "type": "VEVENT",
        "uid": "42",
        "summary": "Standup",
        "dtstart": "2026-10-15T09:00:00Z"
      }
    ]
"""
import re
from typing import Any, Dict, List, Optional, Tuple

from jc.jc_types import JSONDictType
import jc.utils

_ENTITIES = ('VEVENT', 'VTODO', 'VJOURNAL')
_ALARM = 'VALARM'

# Properties copied as-is but for the TEXT escaping.
_TEXT_PROPS = {
    'UID': 'uid',
    'SUMMARY': 'summary',
    'DESCRIPTION': 'description',
    'LOCATION': 'location',
    'URL': 'url',
    'STATUS': 'status',
    'DURATION': 'duration',
}

# Dates and times, kept as strings in the output.
_DATE_PROPS = {
    'DTSTART': 'dtstart',
    'DTEND': 'dtend',
    'DUE': 'due',
    'DTSTAMP': 'dtstamp',
    'CREATED': 'created',
    'LAST-MODIFIED': 'last_modified',
}

_DATE_KEYS = tuple(_DATE_PROPS.values())

_ESCAPES = {'n': '\n', 'N': '\n', ',': ',', ';': ';', '\\': '\\'}

_DATE_RE = re.compile(r'^(\d{4})(\d{2})(\d{2})$')
_DATETIME_RE = re.compile(r'^(\d{4})(\d{2})(\d{2})T(\d{2})(\d{2})(\d{2})(Z|[+-]\d{4})?$')


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = 'iCalendar (.ics) file parser'
    author = 'Paolo Valletta'
    author_email = 'paolovalletta@hotmail.it'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['standard', 'file', 'string']


__version__ = info.version


def _unescape_text(value: str) -> str:
    """
    Resolve the TEXT escapes of RFC 5545 section 3.3.11.
    """
    out: List[str] = []
    i = 0
    while i < len(value):
        char = value[i]
        if char == '\\' and i + 1 < len(value):
            out.append(_ESCAPES.get(value[i + 1], value[i + 1]))
            i += 2
            continue
        out.append(char)
        i += 1

    return ''.join(out)


def _split_list(value: str) -> List[str]:
    """
    Split a comma-separated list on the commas that are not escaped.
    """
    items: List[str] = []
    current: List[str] = []
    i = 0
    while i < len(value):
        char = value[i]
        if char == '\\' and i + 1 < len(value):
            current.append(char)
            current.append(value[i + 1])
            i += 2
            continue
        if char == ',':
            items.append(''.join(current))
            current = []
            i += 1
            continue
        current.append(char)
        i += 1
    items.append(''.join(current))

    return [item for item in items if item]


def _address(params: Dict[str, str], value: str) -> str:
    """
    Return a calendar address as `address` or `CN <address>`.
    """
    address = value[7:] if value.upper().startswith('MAILTO:') else value
    cn = params.get('CN')

    return f'{cn} <{address}>' if cn else address


def _iso(value: str) -> str:
    """
    Normalize an iCalendar `DATE` or `DATE-TIME` value to ISO 8601.
    """
    if match := _DATE_RE.match(value):
        return f'{match[1]}-{match[2]}-{match[3]}'

    if match := _DATETIME_RE.match(value):
        result = f'{match[1]}-{match[2]}-{match[3]}T{match[4]}:{match[5]}:{match[6]}'
        tz = match[7]
        if tz == 'Z':
            return result + 'Z'
        if tz:
            return f'{result}{tz[:3]}:{tz[3:]}'
        return result

    return value


def _unfold(data: str) -> List[str]:
    """
    Unfold the continuation lines of RFC 5545 section 3.1.
    """
    lines: List[str] = []
    for line in data.replace('\r\n', '\n').replace('\r', '\n').split('\n'):
        if line[:1] in (' ', '\t') and lines:
            lines[-1] += line[1:]
            continue
        lines.append(line)

    return lines


def _split_property(line: str) -> Optional[Tuple[str, Dict[str, str], str]]:
    """
    Split `NAME;PARAM=VALUE:VALUE` into its name, parameters and value.
    """
    colon = None
    in_quotes = False
    for i, char in enumerate(line):
        if char == '"':
            in_quotes = not in_quotes
        elif char == ':' and not in_quotes:
            colon = i
            break

    if colon is None:
        return None

    head, value = line[:colon], line[colon + 1:]
    parts: List[str] = []
    current: List[str] = []
    in_quotes = False
    for char in head:
        if char == '"':
            in_quotes = not in_quotes
        if char == ';' and not in_quotes:
            parts.append(''.join(current))
            current = []
            continue
        current.append(char)
    parts.append(''.join(current))

    name = parts[0].upper()
    params: Dict[str, str] = {}
    for part in parts[1:]:
        key, _, param_value = part.partition('=')
        if param_value:
            params[key.upper()] = param_value.strip('"')

    return name, params, value


def _components(lines: List[str]) -> List[Dict[str, Any]]:
    """
    Collect the components of the calendar, with their alarms.
    """
    components: List[Dict[str, Any]] = []
    stack: List[Dict[str, Any]] = []

    for line in lines:
        prop = _split_property(line)
        if prop is None:
            continue

        name, params, value = prop

        if name == 'BEGIN':
            stack.append({'kind': value.upper(), 'lines': [], 'alarms': []})
            continue

        if name == 'END':
            if not stack:
                continue
            component = stack.pop()
            if component['kind'] == _ALARM:
                if stack:
                    stack[-1]['alarms'].append(component)
            elif component['kind'] in _ENTITIES:
                components.append(component)
            continue

        if stack:
            stack[-1]['lines'].append((name, params, value))

    return components


def _alarm(component: Dict[str, Any]) -> JSONDictType:
    """
    Convert a VALARM component to the schema.
    """
    alarm: JSONDictType = {}

    for name, params, value in component['lines']:
        if name == 'ACTION':
            alarm['action'] = _unescape_text(value)
        elif name == 'TRIGGER':
            alarm['trigger'] = value
        elif name == 'DESCRIPTION':
            alarm['description'] = _unescape_text(value)

    return alarm


def _component(component: Dict[str, Any]) -> JSONDictType:
    """
    Convert a calendar component to the schema, before processing.
    """
    text: Dict[str, str] = {}
    dates: Dict[str, str] = {}
    lists: Dict[str, List[str]] = {
        'categories': [], 'attendees': [], 'rdate': [], 'exdate': []}
    sequence: Optional[str] = None
    organizer: Optional[str] = None
    rrule: Optional[str] = None

    for name, params, value in component['lines']:
        if name in _TEXT_PROPS:
            text[_TEXT_PROPS[name]] = _unescape_text(value)
        elif name in _DATE_PROPS:
            dates[_DATE_PROPS[name]] = value
        elif name == 'SEQUENCE':
            sequence = value
        elif name == 'CATEGORIES':
            lists['categories'].extend(
                _unescape_text(item) for item in _split_list(value)
            )
        elif name == 'ORGANIZER':
            organizer = _address(params, value)
        elif name == 'ATTENDEE':
            lists['attendees'].append(_address(params, value))
        elif name == 'RDATE':
            lists['rdate'].extend(_split_list(value))
        elif name == 'EXDATE':
            lists['exdate'].extend(_split_list(value))
        elif name == 'RRULE':
            rrule = value

    out: JSONDictType = {'type': component['kind']}

    for key in ('uid', 'summary', 'description', 'location', 'url', 'status'):
        if key in text:
            out[key] = text[key]

    for key in _DATE_KEYS:
        if key in dates:
            out[key] = dates[key]

    if 'duration' in text:
        out['duration'] = text['duration']

    if sequence is not None:
        out['sequence'] = sequence

    if lists['categories']:
        out['categories'] = lists['categories']

    if organizer is not None:
        out['organizer'] = organizer

    if lists['attendees']:
        out['attendees'] = lists['attendees']

    if rrule is not None:
        out['rrule'] = rrule

    for key in ('rdate', 'exdate'):
        if lists[key]:
            out[key] = lists[key]

    alarms = [_alarm(alarm) for alarm in component['alarms']]
    if alarms:
        out['alarms'] = alarms

    return out


def _process(proc_data: List[JSONDictType]) -> List[JSONDictType]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    for component in proc_data:
        if 'sequence' in component:
            component['sequence'] = jc.utils.convert_to_int(component['sequence'])

        for key in _DATE_KEYS + ('rdate', 'exdate'):
            if key not in component:
                continue
            if isinstance(component[key], list):
                component[key] = [_iso(value) for value in component[key]]
            else:
                component[key] = _iso(component[key])

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
        raw_output = [_component(component) for component in _components(_unfold(data))]

    return raw_output if raw else _process(raw_output)
