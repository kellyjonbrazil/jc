[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.ics"></a>

# jc.parsers.ics

jc - JSON Convert `ics` file parser

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

<a id="jc.parsers.ics.parse"></a>

### parse

```python
def parse(data: str,
          raw: bool = False,
          quiet: bool = False) -> List[Dict[str, Any]]
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) unprocessed output if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    List of Dictionaries. Raw or processed structured data.

### Parser Information
Compatibility:  linux, darwin, cygwin, win32, aix, freebsd

Source: [`jc/parsers/ics.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/ics.py)

Version 1.1 by Paolo Valletta (paolovalletta@hotmail.it)
