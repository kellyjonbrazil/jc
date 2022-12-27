"""jc - JSON Convert `cbt` command output parser (Google Bigtable)

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
"""
from itertools import groupby
from typing import List, Dict
from jc.jc_types import JSONDictType
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`cbt` (Google Bigtable) command parser'
    author = 'Andreas Weiden'
    author_email = 'andreas.weiden@gmail.com'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    magic_commands = ['cbt']
    tags = ['command']


__version__ = info.version


def _process(proc_data: List[JSONDictType]) -> List[JSONDictType]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    out_data = []
    for row in proc_data:
        cells: Dict = {}
        key_func = lambda cell: (cell["column_family"], cell["column"])
        all_cells = sorted(row["cells"], key=key_func)
        for (column_family, column), group in groupby(all_cells, key=key_func):
            group_list = sorted(group, key=lambda cell: cell["timestamp_iso"], reverse=True)
            if column_family not in cells:
                cells[column_family] = {}
            cells[column_family][column] = group_list[0]["value"]
        row["cells"] = cells
        out_data.append(row)
    return out_data


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

    if jc.utils.has_data(data):
        for line in filter(None, data.split("-" * 40)):
            key = None
            cells = []
            column_name = ""
            timestamp = ""
            value_next = False
            for field in line.splitlines():
                if not field.strip():
                    continue
                if field.startswith(" " * 4):
                    value = field.strip(' "')
                    if value_next:
                        dt = jc.utils.timestamp(timestamp, format_hint=(1750, 1755))
                        cells.append({
                            "column_family": column_name.split(":", 1)[0],
                            "column": column_name.split(":", 1)[1],
                            "value": value,
                            "timestamp_iso": dt.iso,
                            "timestamp_epoch": dt.naive,
                            "timestamp_epoch_utc": dt.utc
                        })
                elif field.startswith(" " * 2):
                    column_name, timestamp = map(str.strip, field.split("@"))
                    value_next = True
                else:
                    key = field
            if key is not None:
                raw_output.append({"key": key, "cells": cells})

    return raw_output if raw else _process(raw_output)
