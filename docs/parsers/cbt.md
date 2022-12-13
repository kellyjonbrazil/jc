[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.cbt"></a>

# jc.parsers.cbt

jc - JSON Convert `cbt` command output parser (Google Big Table)

Parses the human-, but not machine-, friendly output of the cbt command (for
Google's BigTable).

No effort is made to convert the data types of the values in the cells.

The timestamps of the cells are converted to Python's isoformat.

Raw output contains all cells for each column (including timestamps in
converted to Python's isoformat), while the normal output contains only the
latest value for each column.

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
          string: {
            string:                 string
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
            "timestamp":            string,
            "value":                string
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
            "timestamp": "1970-01-01T01:00:00",
            "value": "baz"
          }
        ]
      }
    ]

<a id="jc.parsers.cbt.parse"></a>

### parse

```python
def parse(data: str,
          raw: bool = False,
          quiet: bool = False) -> List[JSONDictType]
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

Version 1.0 by Andreas Weiden (andreas.weiden@gmail.com)
