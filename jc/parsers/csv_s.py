r"""jc - JSON Convert `csv` file streaming parser

> This streaming parser outputs JSON Lines (cli) or returns an Iterable of
> Dictionaries (module)

The `csv` streaming parser will attempt to automatically detect the
delimiter character. If the delimiter cannot be detected it will default
to comma. The first row of the file must be a header row.

> Note: The first 100 rows are read into memory to enable delimiter
> detection, then the rest of the rows are loaded lazily.

Usage (cli):

    $ cat file.csv | jc --csv-s

Usage (module):

    import jc

    result = jc.parse('csv_s', csv_output.split('\n'))
    for item in result:
        # do something

Schema:

CSV file converted to a Dictionary:
https://docs.python.org/3/library/csv.html

    {
      "column_name1":     string,
      "column_name2":     string,

      # below object only exists if using -qq or ignore_exceptions=True
      "_jc_meta": {
        "success":        boolean,     # false if error parsing
        "error":          string,      # exists if "success" is false
        "line":           string       # exists if "success" is false
      }
    }

Examples:

    $ cat homes.csv
    "Sell", "List", "Living", "Rooms", "Beds", "Baths", "Age", "Acres"...
    142, 160, 28, 10, 5, 3,  60, 0.28,  3167
    175, 180, 18,  8, 4, 1,  12, 0.43,  4033
    129, 132, 13,  6, 3, 1,  41, 0.33,  1471
    ...

    $ cat homes.csv | jc --csv-s
    {"Sell":"142","List":"160","Living":"28","Rooms":"10","Beds":"5"...}
    {"Sell":"175","List":"180","Living":"18","Rooms":"8","Beds":"4"...}
    {"Sell":"129","List":"132","Living":"13","Rooms":"6","Beds":"3"...}
    ...
"""
import csv
import itertools
from typing import Iterable, Iterator, List, Union, Type
import jc.utils
from jc.streaming import streaming_input_type_check, add_jc_meta, raise_or_yield
from jc.jc_types import StreamingOutputType
from jc.exceptions import ParseError
from jc.parsers.csv import _sniff


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.6'
    description = 'CSV file streaming parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    details = 'Using the python standard csv library'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['standard', 'file', 'string']
    streaming = True


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Each Dictionary represents a row in the csv
        file.
    """
    # No further processing
    return proc_data


def _with_line_endings(data: Iterable[str]) -> Iterator[str]:
    """
    Yield the lines with a line ending, so line breaks inside quoted fields
    are kept by the csv module. A line ending in a lone CR (from splitting
    CRLF text on LF) gets its LF back.
    """
    for line in data:
        if isinstance(line, str) and not line.endswith('\n'):
            line += '\n'
        yield line


class _RecordLines():
    """Iterator over lines that keeps the lines read for the current record"""
    def __init__(self, lines: Iterator[str]) -> None:
        self.lines = lines
        self.record: List[str] = []

    def __iter__(self) -> '_RecordLines':
        return self

    def __next__(self) -> str:
        line = next(self.lines)
        self.record.append(line)
        return line


_OPEN_STATES = ('quoted', 'quoted_escape', 'escape')


def _quote_state(
    text: str,
    dialect: Union[str, Type[csv.Dialect]],
    state: str = 'start'
) -> str:
    """
    Return the state of the csv module's reader after reading `text`,
    starting from `state`. A record continues on the next line if the
    state is in `_OPEN_STATES` (inside a quoted field or after an escape
    character).
    """
    d = csv.get_dialect(dialect) if isinstance(dialect, str) else dialect
    quotechar = d.quotechar if d.quoting != csv.QUOTE_NONE else None
    for c in text:
        if state == 'escape':
            state = 'field'
        elif state == 'quoted_escape':
            state = 'quoted'
        elif state == 'quoted':
            if c == d.escapechar:
                state = 'quoted_escape'
            elif c == quotechar:
                state = 'quote_in_quoted' if d.doublequote else 'field'
        elif c in '\r\n':
            state = 'start'
        elif c == d.delimiter:
            state = 'start'
        elif state == 'quote_in_quoted' and c == quotechar:
            state = 'quoted'
        elif c == d.escapechar:
            state = 'escape'
        elif state == 'start' and c == quotechar:
            state = 'quoted'
        elif state == 'start' and c == ' ' and d.skipinitialspace:
            pass
        else:
            state = 'field'

    return state


@add_jc_meta
def parse(
    data: Iterable[str],
    raw: bool = False,
    quiet: bool = False,
    ignore_exceptions: bool = False,
    implicit_header: bool = False,
    tsv: bool = False,
) -> StreamingOutputType:
    """
    Main text parsing generator function. Returns an iterable object.

    Parameters:

        data:              (iterable)  line-based text data to parse
                                       (e.g. sys.stdin or str.split('\\n'))

        raw:               (boolean)   unprocessed output if True
        quiet:             (boolean)   suppress warning messages if True
        ignore_exceptions: (boolean)   ignore parsing exceptions if True

    Returns:

        Iterable of Dictionaries
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    streaming_input_type_check(data)

    # convert data to an iterator in case a sequence like a list is used as input.
    # this allows the exhaustion of the input so we don't double-process later.
    # the lines keep their line endings for the csv module.
    data = _with_line_endings(data)
    temp_list = []

    # first, load the first 100 lines into a list to detect the CSV dialect
    for line in itertools.islice(data, 100):
        temp_list.append(line)

    # check for Python bug that does not split on `\r` newlines from sys.stdin correctly
    # https://bugs.python.org/issue45617
    if len(temp_list) == 1 and temp_list[0].rstrip():
        raise ParseError('Unable to detect line endings. Please try the non-streaming CSV parser instead.')

    # remove BOM bytes from first row, if present
    if temp_list:
        if isinstance(temp_list[0], str):
            temp_list[0] = temp_list[0].encode('utf-8')

        temp_list[0] = temp_list[0].decode('utf-8-sig')

    sniffdata = '\r\n'.join(line.rstrip() for line in temp_list)
    dialect: Union[str, Type[csv.Dialect]] = (
            'excel-tab' if tsv
            else 'excel'  # default in csv module
        )

    try:
        dialect = _sniff(sniffdata)
        if tsv:
            dialect.delimiter = '\t'
    except Exception:
        pass

    # chain `temp_list` and `data` together to lazy load the rest of the CSV data
    new_data = _RecordLines(itertools.chain(temp_list, data))
    reader = csv.DictReader(
            new_data,
            dialect=dialect,
            # In implicit mode Python will skip the header
            # and put all fields in `restkey` (`None`).
            fieldnames=[] if implicit_header else None
        )

    # read the header row first, so a header error is not ignored and the
    # next row is not taken as the header
    try:
        reader.fieldnames
    except csv.Error as e:
        raise ParseError(f'Unable to parse the header row: {e}')

    while True:
        new_data.record = []

        try:
            row = next(reader)

        except StopIteration:
            return

        except Exception as e:
            text = ''.join(new_data.record)
            error = raise_or_yield(ignore_exceptions, e, text.strip('\r\n'))

            # the csv reader starts again at the next input line, so skip the
            # rest of a quoted field that continues on the next lines
            state = _quote_state(text, dialect)
            if state in _OPEN_STATES:
                for line in new_data.lines:
                    state = _quote_state(line, dialect, state)
                    if state not in _OPEN_STATES:
                        break

            yield error
            continue

        try:
            if implicit_header:
                row = { f"c{idx}": col for idx, col in enumerate(row[None]) }
            yield row if raw else _process(row)
        except Exception as e:
            yield raise_or_yield(ignore_exceptions, e, str(row))
