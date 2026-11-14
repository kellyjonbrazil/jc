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
from typing import List, Dict, Optional, Union


class info:
    """Provides parser metadata (version, author, etc.)"""
    version = "1.2"
    description = "`swapon` command parser"
    author = "Roey Darwish Dror"
    author_email = "roey.ghost@gmail.com"
    compatible = ["linux", "freebsd"]
    magic_commands = ["swapon"]
    tags = ["command"]


__version__ = info.version

_Value = Union[str, int, None]
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


def _parse_size(size: str, kib: bool) -> Optional[int]:
    # `swapon -s` (and /proc/swaps) print sizes in KiB with no unit. `swapon
    # --show` prints sizes with binary one-letter units, or bytes with --bytes.
    if kib and size.isdigit():
        return int(size) * 1024

    return jc.utils.convert_size_to_int(size, posix_mode=True)


def _value(value: str, column: _Column, kib: bool) -> _Value:
    if column == _Column.SIZE or column == _Column.USED:
        return _parse_size(value, kib)
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
        lines = iter(jc.utils.splitlines(data))
        headers = next(lines)
        columns = headers.split()
        kib = "Size" in columns
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
                document[column.value] = _value(value, column, kib)

            raw_output.append(document)

    return raw_output if raw else _process(raw_output)
