r"""jc - JSON Convert `ics` file parser

Usage (cli):

    $ cat calendar.ics | jc --ics

Usage (module):

    import jc
    result = jc.parse('ics', ics_file_output)

Schema:

    [
      {
        "type":                     string,   # [0]
        "uid":                      string,
        "summary":                  string,
        "description":              string,
        "location":                 string,
        "url":                      string,
        "status":                   string,
        "class":                    string,
        "transp":                   string,
        "geo":                      string,
        "dtstart":                  string,   # [1]
        "dtstart_tzid":             string,   # [2]
        "dtend":                    string,   # [1]
        "dtend_tzid":               string,   # [2]
        "due":                      string,   # [1]
        "due_tzid":                 string,   # [2]
        "recurrence_id":            string,   # [1]
        "recurrence_id_tzid":       string,   # [2]
        "dtstamp":                  string,   # [1]
        "created":                  string,   # [1]
        "last_modified":            string,   # [1]
        "completed":                string,   # [1]
        "duration":                 string,
        "sequence":                 integer,
        "priority":                 integer,
        "percent_complete":         integer,
        "categories": [
                                    string
        ],
        "organizer": {
          "name":                   string,   # [3]
          "address":                string,
          "role":                   string,   # [3]
          "partstat":               string,   # [3]
          "rsvp":                   boolean   # [5]
        },
        "attendees": [
          {
            "name":                 string,   # [3]
            "address":              string,
            "role":                 string,   # [3]
            "partstat":             string,   # [3]
            "rsvp":                 boolean   # [5]
          }
        ],
        "rrule":                    string,   # [6]
        "rdate": [
                                    string    # [1]
        ],
        "rdate_tzid":               string,   # [2]
        "exdate": [
                                    string    # [1]
        ],
        "exdate_tzid":              string,   # [2]
        "alarms": [
          {
            "action":               string,
            "trigger":              string,   # [4]
            "description":          string
          }
        ]
      }
    ]

    [0] one of `VEVENT`, `VTODO` or `VJOURNAL`
    [1] normalized to ISO 8601 in the processed output; `raw=True` keeps the
        original iCalendar value
    [2] only when the property carries a `TZID` parameter. `rdate_tzid` and
        `exdate_tzid` hold the `TZID` of the last property that carried one, so
        a `RDATE` or `EXDATE` list that mixes zones keeps only the last one
    [3] `name` only when the property carries a `CN` parameter; `role` and
        `partstat` only when those parameters are present
    [4] the `DATE-TIME` form is normalized to ISO 8601 in the processed
        output, while a duration such as `-PT15M` is passed through
    [5] only when the property carries an `RSVP` parameter. Converted to a
        boolean in the processed output, while `raw=True` keeps the
        iCalendar `TRUE`/`FALSE` value
    [6] passed through, not expanded into occurrences

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
    'CLASS': 'class',
    'TRANSP': 'transp',
    'GEO': 'geo',
    'DURATION': 'duration',
}

# Dates and times, kept as strings in the output, with their TZID.
_DATE_PROPS = {
    'DTSTART': 'dtstart',
    'DTEND': 'dtend',
    'DUE': 'due',
    'RECURRENCE-ID': 'recurrence_id',
    'DTSTAMP': 'dtstamp',
    'CREATED': 'created',
    'LAST-MODIFIED': 'last_modified',
    'COMPLETED': 'completed',
}

_DATE_KEYS = tuple(_DATE_PROPS.values())

# Properties whose value is a list of dates, with their TZID.
_DATE_LIST_PROPS = {'RDATE': 'rdate', 'EXDATE': 'exdate'}

# Integer properties.
_INT_PROPS = {
    'SEQUENCE': 'sequence',
    'PRIORITY': 'priority',
    'PERCENT-COMPLETE': 'percent_complete',
}

_INT_KEYS = tuple(_INT_PROPS.values())

# Parameters of an address that are carried into the output.
_ADDRESS_PARAMS = (('ROLE', 'role'), ('PARTSTAT', 'partstat'), ('RSVP', 'rsvp'))

_ESCAPES = {'n': '\n', 'N': '\n', ',': ',', ';': ';', '\\': '\\'}

_DATE_RE = re.compile(r'^(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})$')
_DATETIME_RE = re.compile(
    r'^(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})'
    r'T(?P<hour>\d{2})(?P<minute>\d{2})(?P<second>\d{2})'
    r'(?P<tz>Z|[+-]\d{4})?$'
)


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`ics` file parser'
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


def _address(params: Dict[str, str], value: str) -> JSONDictType:
    """
    Return a calendar address as an object with its name and parameters.
    """
    address = value[7:] if value.upper().startswith('MAILTO:') else value
    result: JSONDictType = {}

    if params.get('CN'):
        result['name'] = params['CN']

    result['address'] = address

    for param, key in _ADDRESS_PARAMS:
        if param in params:
            result[key] = params[param]

    return result


def _iso(value: str) -> str:
    """
    Normalize an iCalendar `DATE` or `DATE-TIME` value to ISO 8601.
    """
    match = _DATE_RE.match(value)
    if match:
        return f'{match.group("year")}-{match.group("month")}-{match.group("day")}'

    match = _DATETIME_RE.match(value)
    if match:
        result = (
            f'{match.group("year")}-{match.group("month")}-{match.group("day")}'
            f'T{match.group("hour")}:{match.group("minute")}:{match.group("second")}'
        )
        tz = match.group('tz')
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


def _components(lines: List[str], quiet: bool = False) -> List[Dict[str, Any]]:
    """
    Collect the components of the calendar, with their alarms.
    """
    components: List[Dict[str, Any]] = []
    stack: List[Dict[str, Any]] = []
    calendar = False
    entity = False

    for line in lines:
        if not line.strip():
            continue

        prop = _split_property(line)
        if prop is None:
            if not quiet:
                jc.utils.warning_message(
                    [f'Skipping a line with no property/value separator: {line}'])
            continue

        name, params, value = prop

        if name == 'BEGIN':
            kind = value.upper()
            calendar = calendar or kind == 'VCALENDAR'
            entity = entity or kind in _ENTITIES
            stack.append({'kind': kind, 'lines': [], 'alarms': []})
            continue

        if name == 'END':
            kind = value.upper()
            if kind not in [component['kind'] for component in stack]:
                if not quiet:
                    jc.utils.warning_message([f'END:{kind} without a matching BEGIN'])
                continue
            if stack[-1]['kind'] != kind and not quiet:
                jc.utils.warning_message([
                    f'END:{kind} does not match the open BEGIN:{stack[-1]["kind"]}'])
            # a mismatched END closes the components above the one it names;
            # one that was never closed is dropped like any unterminated
            # component, and named in a warning of its own
            while stack[-1]['kind'] != kind:
                above = stack.pop()
                if above['kind'] == _ALARM:
                    if stack:
                        stack[-1]['alarms'].append(above)
                elif above['kind'] in _ENTITIES and not quiet:
                    jc.utils.warning_message([
                        f'Unterminated BEGIN:{above["kind"]}: no END for the component'])
            component = stack.pop()
            if component['kind'] == _ALARM:
                if stack:
                    stack[-1]['alarms'].append(component)
            elif component['kind'] in _ENTITIES:
                components.append(component)
            continue

        if stack:
            stack[-1]['lines'].append((name, params, value))

    if not quiet:
        for component in stack:
            if component['kind'] in _ENTITIES:
                jc.utils.warning_message([
                    f'Unterminated BEGIN:{component["kind"]}: no END for the component'])

        # a bare component (an event pasted without its VCALENDAR wrapper)
        # parses fine, so only warn when nothing calendar-like was found
        if not calendar and not entity:
            jc.utils.warning_message([
                'No BEGIN:VCALENDAR found: the input does not look like iCalendar data'])
        elif not components and not entity:
            jc.utils.warning_message([
                'No VEVENT, VTODO or VJOURNAL components found'])

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
    tzids: Dict[str, str] = {}
    numbers: Dict[str, str] = {}
    lists: Dict[str, List[str]] = {
        'categories': [], 'attendees': [], 'rdate': [], 'exdate': []}
    organizer: Optional[JSONDictType] = None
    rrule: Optional[str] = None

    for name, params, value in component['lines']:
        if name in _TEXT_PROPS:
            text[_TEXT_PROPS[name]] = _unescape_text(value)
        elif name in _DATE_PROPS:
            key = _DATE_PROPS[name]
            dates[key] = value
            if params.get('TZID'):
                tzids[key] = params['TZID']
        elif name in _DATE_LIST_PROPS:
            key = _DATE_LIST_PROPS[name]
            lists[key].extend(_split_list(value))
            if params.get('TZID'):
                tzids[key] = params['TZID']
        elif name in _INT_PROPS:
            numbers[_INT_PROPS[name]] = value
        elif name == 'CATEGORIES':
            lists['categories'].extend(
                _unescape_text(item) for item in _split_list(value)
            )
        elif name == 'ORGANIZER':
            organizer = _address(params, value)
        elif name == 'ATTENDEE':
            lists['attendees'].append(_address(params, value))
        elif name == 'RRULE':
            rrule = value

    out: JSONDictType = {'type': component['kind']}

    for key in ('uid', 'summary', 'description', 'location', 'url', 'status',
                'class', 'transp', 'geo'):
        if key in text:
            out[key] = text[key]

    for key in _DATE_KEYS:
        if key in dates:
            out[key] = dates[key]
            if key in tzids:
                out[f'{key}_tzid'] = tzids[key]

    if 'duration' in text:
        out['duration'] = text['duration']

    for key in _INT_KEYS:
        if key in numbers:
            out[key] = numbers[key]

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
            if key in tzids:
                out[f'{key}_tzid'] = tzids[key]

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
        for key in _INT_KEYS:
            if key in component:
                component[key] = jc.utils.convert_to_int(component[key])

        for key in _DATE_KEYS + ('rdate', 'exdate'):
            if key not in component:
                continue
            if isinstance(component[key], list):
                component[key] = [_iso(value) for value in component[key]]
            else:
                component[key] = _iso(component[key])

        addresses = list(component.get('attendees', []))
        if 'organizer' in component:
            addresses.append(component['organizer'])

        for address in addresses:
            if 'rsvp' in address:
                address['rsvp'] = address['rsvp'].upper() == 'TRUE'

        for alarm in component.get('alarms', []):
            if 'trigger' in alarm:
                alarm['trigger'] = _iso(alarm['trigger'])

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
        raw_output = [
            _component(component) for component in _components(_unfold(data), quiet)
        ]

    return raw_output if raw else _process(raw_output)
