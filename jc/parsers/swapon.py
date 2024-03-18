r"""jc - JSON Convert `swapon` command output parser

Usage (cli):

    $ swapon | jc --swapon

or

    $ jc swapon

Usage (module):

    import jc
    result = jc.parse('swapon', swapon_command_output)

Schema:

    [
      {
        "name":             string,
        "type":             string,
        "size":             integer,
        "used":             integer,
        "priority":         integer
      }
    ]

Example:

    $ swapon | jc --swapon
    [
      {
        "name": "/swapfile",
        "type": "file",
        "size": 1073741824,
        "used": 0,
        "priority": -2
      }
    ]
"""
from enum import Enum
from jc.exceptions import ParseError
import jc.utils
from typing import List, Dict, Union


class info:
    """Provides parser metadata (version, author, etc.)"""
    version = "1.0"
    description = "`swapon` command parser"
    author = "Roey Darwish Dror"
    author_email = "roey.ghost@gmail.com"
    compatible = ["linux", "freebsd"]
    magic_commands = ["swapon"]
    tags = ["command"]


__version__ = info.version

_Value = Union[str, int]
_Entry = Dict[str, _Value]


class _Column(Enum):
    NAME = "name"
    TYPE = "type"
    SIZE = "size"
    USED = "used"
    PRIO = "priority"
    LABEL = "label"
    UUID = "uuid"

    @classmethod
    def from_header(cls, header: str) -> "_Column":
        if (header == "NAME") or (header == "Filename"):
            return cls.NAME
        elif (header == "TYPE") or (header == "Type"):
            return cls.TYPE
        elif (header == "SIZE") or (header == "Size"):
            return cls.SIZE
        elif (header == "USED") or (header == "Used"):
            return cls.USED
        elif (header == "PRIO") or (header == "Priority"):
            return cls.PRIO
        elif header == "LABEL":
            return cls.LABEL
        elif header == "UUID":
            return cls.UUID
        else:
            raise ParseError(f"Unknown header: {header}")


def _parse_size(size: str) -> int:
    power = None
    if size[-1] == "B":
        power = 0
    if size[-1] == "K":
        power = 1
    elif size[-1] == "M":
        power = 2
    elif size[-1] == "G":
        power = 3
    elif size[-1] == "T":
        power = 4

    multiplier = 1024**power if power is not None else 1024

    return (int(size[:-1]) if power is not None else int(size)) * multiplier


def _value(value: str, column: _Column) -> _Value:
    if column == _Column.SIZE or column == _Column.USED:
        return _parse_size(value)
    elif column == _Column.PRIO:
        return int(value)
    else:
        return value


def _process(proc_data: List[Dict]) -> List[Dict]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    return proc_data


def parse(data: str, raw: bool = False, quiet: bool = False) -> List[_Entry]:
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[dict] = []

    if jc.utils.has_data(data):
        lines = iter(data.splitlines())
        headers = next(lines)
        columns = headers.split()
        for each_line in lines:
            line = each_line.split()
            diff = len(columns) - len(line)
            if not 0 <= diff <= 2:
                raise ParseError(
                    f"Number of columns ({len(line)}) in line does not match number of headers ({len(columns)})"
                )

            document: _Entry = {}
            for each_column, value in zip(columns, line):
                column = _Column.from_header(each_column)
                document[column.value] = _value(value, column)

            raw_output.append(document)

    return raw_output if raw else _process(raw_output)
