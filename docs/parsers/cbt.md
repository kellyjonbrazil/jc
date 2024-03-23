[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.cbt"></a>

# jc.parsers.cbt

jc - JSON Convert `cbt` command output parser (Google Bigtable)

Parses the human-, but not machine-, friendly output of the cbt command (for
Google's Bigtable).

No effort is made to convert the data types of the values in the cells.

The `timestamp_epoch` calculated timestamp field is naive. (i.e. based on
the local time of the system the parser is run on)

The `timestamp_epoch_utc` calculated timestamp field is timezone-aware and
is only available if the timestamp has a UTC timezone.

The `timestamp_iso` calculated timestamp field will only include UTC
timezone information if the timestamp has a UTC timezone.

Raw output contains all cells for each column (including timestamps), while
the normal output contains only the latest value for each column.

Usage (cli):

    $ cbt | jc --cbt

or

    $ jc cbt

Usage (module):

    import jc
    result = jc.parse('cbt', cbt_command_output)

Schema:

    [
      {
        "key":                      string,
        "cells": {
          <string>: {                         # column family
            <string>:               string    # column: value
          }
        }
      }
    ]

Schema (raw):

    [
      {
        "key":                      string,
        "cells": [
          {
            "column_family":        string,
            "column":               string,
            "value":                string,
            "timestamp_iso":        string,
            "timestamp_epoch":      integer,
            "timestamp_epoch_utc":  integer
          }
        ]
      }
    ]

Examples:

    $ cbt -project=$PROJECT -instance=$INSTANCE lookup $TABLE foo | jc --cbt -p
    [
      {
        "key": "foo",
        "cells": {
          "foo": {
            "bar": "baz"
          }
        }
      }
    ]

    $ cbt -project=$PROJECT -instance=$INSTANCE lookup $TABLE foo | jc --cbt -p -r
    [
      {
        "key": "foo",
        "cells": [
          {
            "column_family": "foo",
            "column": "bar",
            "value": "baz1",
            "timestamp_iso": "1970-01-01T01:00:00",
            "timestamp_epoch": 32400,
            "timestamp_epoch_utc": null
          }
        ]
      }
    ]

<a id="jc.parsers.cbt.parse"></a>

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

Source: [`jc/parsers/cbt.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/cbt.py)

Version 1.0 by Andreas Weiden (andreas.weiden@gmail.com)
