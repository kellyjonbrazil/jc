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
        "dtstart_epoch":            integer,  # [7]
        "dtstart_epoch_utc":        integer,  # [8]
        "dtend":                    string,   # [1]
        "dtend_tzid":               string,   # [2]
        "dtend_epoch":              integer,  # [7]
        "dtend_epoch_utc":          integer,  # [8]
        "due":                      string,   # [1]
        "due_tzid":                 string,   # [2]
        "due_epoch":                integer,  # [7]
        "due_epoch_utc":            integer,  # [8]
        "recurrence_id":            string,   # [1]
        "recurrence_id_tzid":       string,   # [2]
        "recurrence_id_epoch":      integer,  # [7]
        "recurrence_id_epoch_utc":  integer,  # [8]
        "dtstamp":                  string,   # [1]
        "dtstamp_epoch":            integer,  # [7]
        "dtstamp_epoch_utc":        integer,  # [8]
        "created":                  string,   # [1]
        "created_epoch":            integer,  # [7]
        "created_epoch_utc":        integer,  # [8]
        "last_modified":            string,   # [1]
        "last_modified_epoch":      integer,  # [7]
        "last_modified_epoch_utc":  integer,  # [8]
        "completed":                string,   # [1]
        "completed_epoch":          integer,  # [7]
        "completed_epoch_utc":      integer,  # [8]
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
    [7] calculated naive timestamp (based on the local time zone of the
        system jc runs on) of a floating time or a `DATE` value, otherwise
        `null`. Not in the `raw=True` output
    [8] calculated timezone-aware timestamp of a UTC time, a time with a UTC
        offset, or a time with a `TZID`, otherwise `null`. A `TZID` is
        resolved with the `VTIMEZONE` component of the same name in the file,
        so the timestamp is `null` when that component is missing (except
        for `UTC` and `GMT`) or uses an `RRULE` other than a yearly rule by
        month and day. Not in the `raw=True` output

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
        "dtstart": "2026-10-15T09:00:00Z",
        "dtstart_epoch": null,
        "dtstart_epoch_utc": 1792054800
      }
    ]
"""
import bisect
import calendar
import re
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

from jc.jc_types import JSONDictType
import jc.utils

_ENTITIES = ('VEVENT', 'VTODO', 'VJOURNAL')
_ALARM = 'VALARM'
_TIMEZONE = 'VTIMEZONE'
_OBSERVANCES = ('STANDARD', 'DAYLIGHT')

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
_OFFSET_RE = re.compile(
    r'^(?P<sign>[+-])(?P<hour>\d{2})(?P<minute>\d{2})(?P<second>\d{2})?$'
)
_BYDAY_RE = re.compile(r'^(?P<nth>[+-]?\d{1,2})?(?P<day>MO|TU|WE|TH|FR|SA|SU)$')
_WEEKDAYS = {'MO': 0, 'TU': 1, 'WE': 2, 'TH': 3, 'FR': 4, 'SA': 5, 'SU': 6}

# real time zones change their offset at most a few times a year and have
# a few dozen yearly rules at most, so more transitions than this within a
# day of a time, or more yearly rules than this, leave it unresolved
_MAX_NEARBY = 16
_MAX_RULES = 64

# TZIDs that mean UTC even without a VTIMEZONE component
_UTC_TZIDS = {'UTC', 'Etc/UTC', 'GMT', 'Etc/GMT'}

# RRULE parts a VTIMEZONE observance may use here; any other rule leaves the
# time zone unresolved
_RULE_PARTS = {'FREQ', 'INTERVAL', 'BYMONTH', 'BYDAY', 'BYMONTHDAY', 'UNTIL', 'WKST'}


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.2'
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


def _local(value: str) -> Optional[datetime]:
    """
    Return the date and time of a `DATE-TIME` value, ignoring its UTC
    designator or offset.
    """
    match = _DATETIME_RE.match(value)
    if not match:
        return None

    try:
        return datetime(
            int(match.group('year')), int(match.group('month')), int(match.group('day')),
            int(match.group('hour')), int(match.group('minute')), int(match.group('second'))
        )
    except ValueError:
        return None


def _offset(value: str) -> Optional[int]:
    """
    Return a UTC offset such as `-0800` or `+053000` in seconds.
    """
    match = _OFFSET_RE.match(value.strip())
    if not match:
        return None

    hour, minute = int(match.group('hour')), int(match.group('minute'))
    second = int(match.group('second') or 0)
    if hour > 23 or minute > 59 or second > 59:
        return None

    seconds = hour * 3600 + minute * 60 + second

    return -seconds if match.group('sign') == '-' else seconds


def _yearly_rule(rrule: str, start: datetime) -> Optional[Dict[str, Any]]:
    """
    Read the yearly RRULE of a VTIMEZONE observance, such as
    `FREQ=YEARLY;BYMONTH=3;BYDAY=2SU`. Returns None for other rules.
    """
    parts: Dict[str, str] = {}
    for part in rrule.split(';'):
        key, _, value = part.partition('=')
        parts[key.strip().upper()] = value.strip().upper()

    if (parts.get('FREQ') != 'YEARLY' or parts.get('INTERVAL', '1') != '1'
            or set(parts) - _RULE_PARTS):
        return None

    rule: Dict[str, Any] = {
        'month': start.month, 'weekday': None, 'nth': None,
        'monthdays': [start.day], 'until': None, 'until_utc': False
    }

    try:
        if 'BYMONTH' in parts:
            rule['month'] = int(parts['BYMONTH'])
            if not 1 <= rule['month'] <= 12:
                return None

        if 'BYDAY' in parts:
            match = _BYDAY_RE.match(parts['BYDAY'])
            if not match:
                return None
            rule['weekday'] = _WEEKDAYS[match.group('day')]
            if match.group('nth'):
                rule['nth'] = int(match.group('nth'))
                if rule['nth'] == 0 or not -5 <= rule['nth'] <= 5:
                    return None
            else:
                rule['monthdays'] = list(range(1, 32))

        if 'BYMONTHDAY' in parts:
            rule['monthdays'] = sorted(int(day) for day in parts['BYMONTHDAY'].split(','))
            if not all(1 <= day <= 31 for day in rule['monthdays']):
                return None

    except ValueError:
        return None

    if 'UNTIL' in parts:
        match = _DATE_RE.match(parts['UNTIL'])
        if match:
            try:
                rule['until'] = datetime(int(match.group('year')), int(match.group('month')),
                                         int(match.group('day')), 23, 59, 59)
            except ValueError:
                return None
        else:
            rule['until'] = _local(parts['UNTIL'])
            if rule['until'] is None:
                return None
            rule['until_utc'] = parts['UNTIL'].endswith('Z')

    return rule


def _rule_day(rule: Dict[str, Any], year: int) -> Optional[int]:
    """
    Return the day of the month a yearly rule falls on in the given year.
    """
    days = calendar.monthrange(year, rule['month'])[1]
    weekday = rule['weekday']
    nth = rule['nth']

    if nth is not None:
        if nth > 0:
            first = calendar.weekday(year, rule['month'], 1)
            day = 1 + (weekday - first) % 7 + (nth - 1) * 7
        else:
            last = calendar.weekday(year, rule['month'], days)
            day = days - (last - weekday) % 7 - (-nth - 1) * 7
        return day if 1 <= day <= days else None

    for day in rule['monthdays']:
        if day <= days and (weekday is None or calendar.weekday(year, rule['month'], day) == weekday):
            return day

    return None


def _timezone(component: Dict[str, Any]) -> Tuple[Optional[str], Optional[Dict[str, Any]]]:
    """
    Read a VTIMEZONE component. Returns its TZID and its UTC offset
    transitions, or None for the transitions when they can't be read.
    """
    tzid = None
    for name, params, value in component['lines']:
        if name == 'TZID':
            tzid = value

    fixed: List[Tuple[datetime, int, int]] = []
    rules: List[Tuple[Dict[str, Any], datetime, int, int]] = []

    for observance in component['observances']:
        start = before = after = rrule = None
        onsets: List[Optional[datetime]] = []
        for name, params, value in observance['lines']:
            if name == 'DTSTART':
                start = _local(value)
            elif name == 'TZOFFSETFROM':
                before = _offset(value)
            elif name == 'TZOFFSETTO':
                after = _offset(value)
            elif name == 'RRULE':
                rrule = value
            elif name == 'RDATE':
                onsets.extend(_local(item) for item in _split_list(value))

        if start is None or before is None or after is None or None in onsets:
            return tzid, None

        onsets.append(start)

        try:
            for onset in onsets:
                fixed.append((onset - timedelta(seconds=before), before, after))
        except OverflowError:
            return tzid, None

        if rrule is not None:
            rule = _yearly_rule(rrule, start)
            if rule is None:
                return tzid, None
            rules.append((rule, start, before, after))

    if not fixed or len(rules) > _MAX_RULES:
        return tzid, None

    fixed = sorted(set(fixed), key=lambda transition: transition[0])

    return tzid, {'fixed': fixed, 'fixed_utc': [t[0] for t in fixed], 'rules': rules, 'years': {}}


def _rule_transitions(zone: Dict[str, Any], year: int) -> Tuple[List[Tuple[datetime, int, int]], List[datetime]]:
    """
    Return the transitions of the yearly rules of a time zone from the year
    before to the year after the given year, plus the last transition of
    each rule that ended earlier, sorted, with their UTC times. Cached per
    year.
    """
    if year in zone['years']:
        return zone['years'][year]

    transitions: List[Tuple[datetime, int, int]] = []
    for rule, start, before, after in zone['rules']:
        years = set(range(max(start.year, year - 1), min(9999, year + 1) + 1))
        if rule['until'] is not None and rule['until'].year < year - 1:
            years.update(range(max(start.year, rule['until'].year - 1), rule['until'].year + 1))

        for rule_year in sorted(years):
            day = _rule_day(rule, rule_year)
            if day is None:
                continue
            onset = datetime(rule_year, rule['month'], day, start.hour, start.minute, start.second)
            if onset < start:
                continue
            try:
                utc = onset - timedelta(seconds=before)
            except OverflowError:
                continue
            if rule['until'] is not None and (utc if rule['until_utc'] else onset) > rule['until']:
                continue
            transitions.append((utc, before, after))

    transitions.sort(key=lambda transition: transition[0])
    zone['years'][year] = (transitions, [t[0] for t in transitions])
    return zone['years'][year]


def _offset_at(zone: Dict[str, Any], rules: Tuple[List[Tuple[datetime, int, int]], List[datetime]], utc: datetime) -> int:
    """
    Return the UTC offset of a time zone at a UTC date and time.
    """
    latest = None
    index = bisect.bisect_right(zone['fixed_utc'], utc) - 1
    if index >= 0:
        latest = zone['fixed'][index]

    index = bisect.bisect_right(rules[1], utc) - 1
    if index >= 0 and (latest is None or rules[0][index][0] >= latest[0]):
        latest = rules[0][index]

    if latest is None:
        return zone['fixed'][0][1]

    return latest[2]


def _zone_offset(zone: Dict[str, Any], local: datetime) -> Optional[int]:
    """
    Return the UTC offset of a local date and time in a time zone. A time
    that occurs twice takes its first occurrence, and a time skipped by a
    transition takes the offset from before the transition (RFC 5545 section
    3.3.5).
    """
    rules = _rule_transitions(zone, local.year)
    day = timedelta(days=1)

    try:
        # offsets are under a day, so only the transitions within a day of
        # the local time and the offset in effect before them can apply
        nearby: List[Tuple[datetime, int, int]] = []
        for transitions, utcs in ((zone['fixed'], zone['fixed_utc']), rules):
            first = bisect.bisect_left(utcs, local - day)
            last = bisect.bisect_right(utcs, local + day)
            if last - first > _MAX_NEARBY:
                return None
            nearby.extend(transitions[first:last])

        offsets = {_offset_at(zone, rules, local - day)}
        offsets.update(offset for transition in nearby for offset in transition[1:])

        # a larger offset is the earlier of two occurrences
        for offset in sorted(offsets, reverse=True):
            if _offset_at(zone, rules, local - timedelta(seconds=offset)) == offset:
                return offset

        for utc, before, after in nearby:
            if utc + timedelta(seconds=before) <= local < utc + timedelta(seconds=after):
                return before

    except OverflowError:
        return None

    return None


def _epochs(
    value: str,
    tzid: Optional[str],
    zones: Dict[str, Optional[Dict[str, Any]]]
) -> Tuple[Optional[int], Optional[int]]:
    """
    Return the naive and the UTC epoch timestamps of a `DATE` or
    `DATE-TIME` value. Only one of them is set, or neither when the value
    can't be converted.
    """
    try:
        match = _DATE_RE.match(value)
        if match:
            day = datetime(int(match.group('year')), int(match.group('month')), int(match.group('day')))
            return int(day.timestamp()), None

        match = _DATETIME_RE.match(value)
        local = _local(value)
        if match is None or local is None:
            return None, None

        tz = match.group('tz')
        if tz == 'Z':
            return None, calendar.timegm(local.timetuple())

        if tz:
            offset = _offset(tz)
            if offset is None:
                return None, None
            return None, calendar.timegm(local.timetuple()) - offset

        if tzid is None:
            return int(local.timestamp()), None

        if tzid in _UTC_TZIDS and tzid not in zones:
            return None, calendar.timegm(local.timetuple())

        zone = zones.get(tzid)
        offset = _zone_offset(zone, local) if zone else None
        if offset is None:
            return None, None

        return None, calendar.timegm(local.timetuple()) - offset

    except (ValueError, OverflowError, OSError):
        return None, None


def _add_epochs(
    components: List[JSONDictType],
    zones: Dict[str, Optional[Dict[str, Any]]]
) -> List[JSONDictType]:
    """
    Add the calculated epoch timestamps after each date and time (and its
    TZID) of the components.
    """
    for i, component in enumerate(components):
        out: JSONDictType = {}
        for key, value in component.items():
            out[key] = value
            base = key[:-5] if key.endswith('_tzid') else key
            if base in _DATE_KEYS and (key != base or f'{base}_tzid' not in component):
                naive, utc = _epochs(component[base], component.get(f'{base}_tzid'), zones)
                out[f'{base}_epoch'] = naive
                out[f'{base}_epoch_utc'] = utc
        components[i] = out

    return components


def _unfold(data: str) -> List[str]:
    """
    Unfold the continuation lines of RFC 5545 section 3.1.
    """
    # a lone CR is only a line break in files that have no LF at all
    # (CR-only line endings); otherwise it is part of the value
    if '\n' not in data:
        data = data.replace('\r', '\n')

    # pieces of each logical line are joined once, after all are collected
    pieces: List[List[str]] = []
    for line in data.replace('\r\n', '\n').split('\n'):
        if line[:1] in (' ', '\t') and pieces:
            pieces[-1].append(line[1:])
            continue
        pieces.append([line])

    return [''.join(piece) for piece in pieces]


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


def _components(
    lines: List[str],
    quiet: bool = False
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Collect the components of the calendar, with their alarms, and the
    VTIMEZONE components with their observances.
    """
    components: List[Dict[str, Any]] = []
    timezones: List[Dict[str, Any]] = []
    stack: List[Dict[str, Any]] = []
    open_kinds: Dict[str, int] = {}  # number of open components of each kind
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
            stack.append({'kind': kind, 'lines': [], 'alarms': [], 'observances': []})
            open_kinds[kind] = open_kinds.get(kind, 0) + 1
            continue

        if name == 'END':
            kind = value.upper()
            if not open_kinds.get(kind):
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
                open_kinds[above['kind']] -= 1
                if above['kind'] == _ALARM:
                    if stack:
                        stack[-1]['alarms'].append(above)
                elif above['kind'] in _ENTITIES and not quiet:
                    jc.utils.warning_message([
                        f'Unterminated BEGIN:{above["kind"]}: no END for the component'])
            component = stack.pop()
            open_kinds[kind] -= 1
            if component['kind'] == _ALARM:
                if stack:
                    stack[-1]['alarms'].append(component)
            elif component['kind'] in _OBSERVANCES:
                if stack:
                    stack[-1]['observances'].append(component)
            elif component['kind'] == _TIMEZONE:
                timezones.append(component)
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

    return components, timezones


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
    zones: Dict[str, Optional[Dict[str, Any]]] = {}

    if jc.utils.has_data(data):
        components, timezones = _components(_unfold(data), quiet)
        raw_output = [_component(component) for component in components]
        for timezone in timezones:
            tzid, zone = _timezone(timezone)
            if tzid is not None:
                zones[tzid] = zone

    return raw_output if raw else _process(_add_epochs(raw_output, zones))
