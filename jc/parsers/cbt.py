"""jc - JSON Convert `cbt` command output parser

Parses the human-, but not machine-, friendly output of the cbt command (for Google's BigTable).

No effort is made to convert the data types of the values in the cells.

The timestamps of the cells are converted to Python's isoformat.

Raw output contains all cells for each column (including timestamps in converted to Python's isoformat),
while the normal output contains only the latest value for each column.

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
        "key":     string,
        "cells": {
            string: {
                string: string
            }
        }
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
"""
import datetime
from itertools import groupby
from typing import List, Dict
from jc.jc_types import JSONDictType
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`cbt` command parser'
    author = 'Andreas Weiden'
    author_email = 'andreas.weiden@gmail.com'
    # details = 'enter any other details here'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    magic_commands = ['cbt']


__version__ = info.version


def _process(proc_data: List[JSONDictType]) -> List[JSONDictType]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """

    # process the data here
    # rebuild output for added semantic information
    # use helper functions in jc.utils for int, float, bool
    # conversions and timestamps
    out_data = []
    for row in proc_data:
        cells = {}
        key_func = lambda cell: (cell["column_family"], cell["column"])
        all_cells = sorted(row["cells"], key=key_func)
        for (column_family, column), group in groupby(all_cells, key=key_func):
            group = sorted(group, key=lambda cell: cell["timestamp"], reverse=True)
            if column_family not in cells:
                cells[column_family] = {}
            cells[column_family][column] = group[0]["value"]
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
            # parse the content here
            # check out helper functions in jc.utils
            # and jc.parsers.universal
            key = None
            cells = []
            column_name = ""
            timestamp = None
            value_next = False
            for field in line.splitlines():
                if not field.strip():
                    continue
                if field.startswith(" " * 4):
                    value = field.strip(' "')
                    if value_next:
                        cells.append({
                            "column_family": column_name.split(":", 1)[0],
                            "column": column_name.split(":", 1)[1],
                            "timestamp": datetime.datetime.strptime(timestamp, "%Y/%m/%d-%H:%M:%S.%f").isoformat(),
                            "value": value
                        })
                elif field.startswith(" " * 2):
                    column_name, timestamp = map(str.strip, field.split("@"))
                    value_next = True
                else:
                    key = field
            if key is not None:
                raw_output.append({"key": key, "cells": cells})

    return raw_output if raw else _process(raw_output)
